#pragma once

#include <mutex>
#include <atomic>
#include <functional>
namespace packager {

template <typename... PkgElements> class Packager {
  public:
    using Package = std::tuple<PkgElements...>;
    using Callback = std::function<void(const Package &)>;

    Packager(): m_Flags({}) {}

    void Register(Callback cb) {
        std::unique_lock l(m_CallbackMutex);
            m_Callbacks.push_back(cb);
    }

    template <size_t index, typename PkgLike> void Set(PkgLike &&elem) {
        static_assert(index < sizeof...(PkgElements),
                      "Error, index out of bounds. Index must be smaller than "
                      "the package elements.");
        {
            std::unique_lock l(m_ElemMutex);
            std::get<index>(m_Elems) = std::move(elem);
        }
        m_Flags[index] = true;
        if (PackageReady()) {
            RunCallbacks();
        }
    }

  private:
    std::mutex m_ElemMutex;
    Package m_Elems;

    std::mutex m_FlagMutex;
    std::array<std::atomic<bool>, sizeof...(PkgElements)> m_Flags;

    std::mutex m_CallbackMutex;
    std::vector<Callback> m_Callbacks;

    // Checks if all the flags are set. Returns true if so
    bool PackageReady() {
        for (auto& f : m_Flags) {
            if (!f) {
                return false;
            }
        }
        return true;
    }
    void RunCallbacks() {
        Package pkg;
        {
            std::unique_lock l(m_ElemMutex);
            pkg = m_Elems;

            std::unique_lock l2(m_FlagMutex);
            for (auto& f : m_Flags)
                f = false;
        }

        std::unique_lock l(m_CallbackMutex);
        
        for (auto& cb : m_Callbacks) {
            cb(pkg);
        }
    }
};
} // namespace packager
