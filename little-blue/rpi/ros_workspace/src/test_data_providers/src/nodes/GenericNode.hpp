#pragma once
#include <memory>
#include <ratio>
#include <rclcpp/node.hpp>
#include <rclcpp/timer.hpp>

template <typename Provider, typename MsgType>
class GenericNode : public rclcpp::Node {
  public:
    GenericNode(const std::string &nodeName, const std::string &topicName,
                std::unique_ptr<Provider> pProvider,
                std::chrono::duration<long double, std::milli> duration);

  private:
    // next time ill just use functors
    std::unique_ptr<Provider> m_pProvider;
    typename rclcpp::Publisher<MsgType>::SharedPtr m_pPublisher;
    rclcpp::TimerBase::SharedPtr m_pTimer;

    void TimerCallback();
};

template <typename Provider, typename MsgType>
GenericNode<Provider, MsgType>::GenericNode(
    const std::string &nodeName, const std::string &topicName,
    std::unique_ptr<Provider> pProvider,
    std::chrono::duration<long double, std::milli> duration)
    : Node(nodeName), m_pProvider(std::move(pProvider)) {

    m_pPublisher = create_publisher<MsgType>(topicName, 10);
    m_pTimer = create_wall_timer(duration,
                                 std::bind(&GenericNode::TimerCallback, this));
}

template <typename Provider, typename MsgType>
void GenericNode<Provider, MsgType>::TimerCallback() {
    m_pPublisher->publish(m_pProvider->Get());
}
