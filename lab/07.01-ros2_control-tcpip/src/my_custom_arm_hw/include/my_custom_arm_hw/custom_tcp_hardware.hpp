#pragma once
#include "hardware_interface/system_interface.hpp"
#include "rclcpp_lifecycle/state.hpp"
#include <vector>
#include <string>

namespace my_custom_arm_hw
{

  class CustomTcpHardware : public hardware_interface::SystemInterface
  {
  public:
    hardware_interface::CallbackReturn on_init(
        const hardware_interface::HardwareInfo &info) override;

    hardware_interface::CallbackReturn on_configure(
        const rclcpp_lifecycle::State &previous_state) override;

    hardware_interface::CallbackReturn on_activate(
        const rclcpp_lifecycle::State &previous_state) override;

    hardware_interface::CallbackReturn on_deactivate(
        const rclcpp_lifecycle::State &previous_state) override;

    std::vector<hardware_interface::StateInterface> export_state_interfaces() override;
    std::vector<hardware_interface::CommandInterface> export_command_interfaces() override;

    hardware_interface::return_type read(
        const rclcpp::Time &time, const rclcpp::Duration &period) override;

    hardware_interface::return_type write(
        const rclcpp::Time &time, const rclcpp::Duration &period) override;

  private:
    std::string robot_ip_;
    int tcp_port_;
    int sock_fd_ = -1;

    // 硬體 buffer（必須預先分配，realtime safe）
    std::vector<double> hw_position_commands_;
    std::vector<double> hw_position_states_;
    std::vector<double> hw_velocity_states_;

    // 你自己的 TCP protocol 相關函數（請自行實作）
    bool connect_socket();
    void disconnect_socket();
    bool send_custom_protocol(const std::vector<double> &positions);
    bool receive_joint_states();
  };

} // namespace my_custom_arm_hw
