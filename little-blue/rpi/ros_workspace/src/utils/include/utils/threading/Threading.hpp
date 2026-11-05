#include "type_traits"
#include <functional>
#include <memory>
#include <mutex>
#include <optional>
#include <queue>
#include <thread>

namespace igvc {
template <typename T> class ThreadSafeQueue {
  public:
    ThreadSafeQueue() : m_Queue() {}

    ThreadSafeQueue(const ThreadSafeQueue &) = delete;

    template <typename TLike> void Push(TLike &&val) {
        static_assert(std::is_constructible<T, TLike &&>::value,
                      "Cannot construct T from given type");
        std::unique_lock l(m_Mutex);
        m_Queue.push(std::forward<TLike>(val));
    }

    template <typename TLike> bool TryPush(TLike &&val) {
        static_assert(std::is_constructible<T, TLike &&>::value,
                      "Cannot construct T from given type");
        std::unique_lock l(m_Mutex, std::defer_lock);
        bool ret;
        if ((ret = l.try_lock())) {
            m_Queue.push(std::forward<TLike>(val));
        }
        return ret;
    }

    T Pop() {
        static_assert(std::is_move_constructible_v<T>,
                      "T must be move constructible");
        std::unique_lock l(m_Mutex);
        if (m_Queue.empty()) {
            return {};
        }
        T temp = std::move(m_Queue.front());
        m_Queue.pop();
        return temp;
    }

    std::optional<T> TryPop() {
        static_assert(std::is_move_constructible_v<T>,
                      "T must be move constructible");
        std::unique_lock l(m_Mutex, std::defer_lock);
        if (l.try_lock()) {
            if (!m_Queue.empty()) {
                T temp = std::move(m_Queue.front());
                m_Queue.pop();
                return temp;
            }
        }
        return std::nullopt;
    }

    template <typename A, typename B>
    std::optional<T> TryPopFor(std::chrono::duration<A, B> d) {
        static_assert(std::is_move_constructible_v<T>,
                      "T must be move constructible");
        std::unique_lock l(m_Mutex, std::defer_lock);
        if (l.try_lock_for(d)) {
            if (!m_Queue.empty()) {
                T temp = std::move(m_Queue.front());
                m_Queue.pop();
                return temp;
            }
        }
        return std::nullopt;
    }

  private:
    std::queue<T> m_Queue;
    std::timed_mutex m_Mutex;
};

class JobData {
  private:
    JobData(const std::type_info *type, void *data,
            std::function<void(void *)> deleter)
        : m_Type(type), m_Data({data, deleter}) {}

    JobData(const JobData &) = delete;

    const std::type_info *m_Type;
    std::unique_ptr<void, std::function<void(void *)>> m_Data;

  public:
    JobData(JobData &&o) : m_Type(o.m_Type), m_Data(std::move(o.m_Data)) {}

    template <typename T> T &as() {
        if (!m_Type || *m_Type != typeid(T)) {
            throw std::bad_cast();
        }
        return *static_cast<T *>(m_Data.get());
    }

    template <typename TLike> static JobData from(TLike &&val) {
        using T = std::decay_t<TLike>;
        const std::type_info *type = &typeid(T);
        void *ptr = new T(std::forward<TLike>(val));
        std::function<void(void *)> deleter = [](void *ptr) {
            delete static_cast<T *>(ptr);
        };
        JobData job(type, ptr, deleter);
        return job;
    }
};

typedef std::function<void(JobData &)> ThreadPoolJob;
struct Job {
    Job(Job &&j) : job(j.job), data(std::move(j.data)) {}
    Job(const Job &) = delete;
    Job() = delete;

    template <typename Data>
    Job(Data &&dat, ThreadPoolJob j) : job(j), data(JobData::from(dat)) {}

    ThreadPoolJob job;
    JobData data;
};

template <size_t Threads> class ThreadPool {
  public:
    ThreadPool() : m_Run(false) {}
    ~ThreadPool() { Stop(); }

    void Submit(Job &&job) { m_Jobs.Push(std::move(job)); }

    void Run() {
        m_Run = true;
        for (auto &t : m_Threads) {
            t = std::thread(std::bind(&ThreadPool::ThreadMain, this));
        }
    }

    void Stop() {
        m_Run = false;
        for (std::thread &t : m_Threads) {
            t.join();
        }
    }

  private:
    std::array<std::thread, Threads> m_Threads;
    bool m_Run;
    ThreadSafeQueue<Job> m_Jobs;

    void ThreadMain() {
        using namespace std::chrono_literals;
        while (m_Run) {
            auto job = m_Jobs.TryPopFor(10ms);
            if (job.has_value()) {
                job->job(job->data);
            }
        }
    };
};
};
