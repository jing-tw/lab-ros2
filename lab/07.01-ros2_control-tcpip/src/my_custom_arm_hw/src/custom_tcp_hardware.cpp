#include "hardware_interface/types/hardware_interface_type_values.hpp"
#include "my_custom_arm_hw/custom_tcp_hardware.hpp"
#include <rclcpp/rclcpp.hpp>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>


// using hardware_interface::standard_interfaces::HW_IF_POSITION;
// using hardware_interface::standard_interfaces::HW_IF_VELOCITY;

namespace my_custom_arm_hw
{

  hardware_interface::CallbackReturn CustomTcpHardware::on_init(
      const hardware_interface::HardwareInfo &info)
  {
    if (hardware_interface::SystemInterface::on_init(info) !=
        hardware_interface::CallbackReturn::SUCCESS)
      return hardware_interface::CallbackReturn::ERROR;

    robot_ip_ = info_.hardware_parameters["robot_ip"];
    tcp_port_ = std::stoi(info_.hardware_parameters["tcp_port"]);

    // 依照 URDF 中的 joint 數量初始化 buffer
    hw_position_commands_.resize(info_.joints.size(), 0.0);
    hw_position_states_.resize(info_.joints.size(), 0.0);
    hw_velocity_states_.resize(info_.joints.size(), 0.0);

    return hardware_interface::CallbackReturn::SUCCESS;
  }

  hardware_interface::CallbackReturn CustomTcpHardware::on_configure(
      const rclcpp_lifecycle::State & /*previous_state*/)
  {
    return connect_socket() ? hardware_interface::CallbackReturn::SUCCESS : hardware_interface::CallbackReturn::ERROR;
  }

  hardware_interface::CallbackReturn CustomTcpHardware::on_activate(
      const rclcpp_lifecycle::State & /*previous_state*/)
  {
    // 可在此送一次 home 命令
    return hardware_interface::CallbackReturn::SUCCESS;
  }

  hardware_interface::CallbackReturn CustomTcpHardware::on_deactivate(
      const rclcpp_lifecycle::State & /*previous_state*/)
  {
    disconnect_socket();
    return hardware_interface::CallbackReturn::SUCCESS;
  }

  std::vector<hardware_interface::StateInterface>
  CustomTcpHardware::export_state_interfaces()
  {
    std::vector<hardware_interface::StateInterface> state_interfaces;
    for (size_t i = 0; i < info_.joints.size(); ++i)
    {
      // state_interfaces.emplace_back(hardware_interface::StateInterface(
      //     info_.joints[i].name, hardware_interface::standard_interfaces::HW_IF_POSITION, &hw_position_states_[i]));
      // state_interfaces.emplace_back(hardware_interface::StateInterface(
      //     info_.joints[i].name, hardware_interface::standard_interfaces::HW_IF_VELOCITY, &hw_velocity_states_[i]));

      state_interfaces.emplace_back(hardware_interface::StateInterface(
          info_.joints[i].name, "position", &hw_position_states_[i]));
      
      state_interfaces.emplace_back(hardware_interface::StateInterface(
          info_.joints[i].name, "velocity", &hw_velocity_states_[i]));
    }
    return state_interfaces;
  }

  std::vector<hardware_interface::CommandInterface>
  CustomTcpHardware::export_command_interfaces()
  {
    std::vector<hardware_interface::CommandInterface> command_interfaces;
    for (size_t i = 0; i < info_.joints.size(); ++i)
    {
      command_interfaces.emplace_back(hardware_interface::CommandInterface(
          info_.joints[i].name, "position", &hw_position_commands_[i]));
      // command_interfaces.emplace_back(hardware_interface::CommandInterface(
      //     info_.joints[i].name, "velocity", &hw_velocity_states_[i]));
      // command_interfaces.emplace_back(hardware_interface::CommandInterface(
      //     info_.joints[i].name, "effort", &hw_position_commands_[i]));
    }
    return command_interfaces;
  }

  hardware_interface::return_type CustomTcpHardware::read(
      const rclcpp::Time & /*time*/, const rclcpp::Duration & /*period*/)
  {
    if (receive_joint_states())
    {
      return hardware_interface::return_type::OK;
    }
    return hardware_interface::return_type::ERROR;
  }

  hardware_interface::return_type CustomTcpHardware::write(
      const rclcpp::Time & /*time*/, const rclcpp::Duration & /*period*/)
  {
    return send_custom_protocol(hw_position_commands_) ? hardware_interface::return_type::OK : hardware_interface::return_type::ERROR;
  }

  // ==================== 你的自訂 TCP 實作 ====================
  // （把下面這幾個函數替換成你真正的 protocol）
  bool CustomTcpHardware::connect_socket() { /* socket + connect */ return true; }
  void CustomTcpHardware::disconnect_socket()
  {
    if (sock_fd_ > 0)
      close(sock_fd_);
  }
  bool CustomTcpHardware::send_custom_protocol(const std::vector<double> & /*positions*/) { /* 你的封包 */ return true; }
  bool CustomTcpHardware::receive_joint_states() { /* 接收並解析 */ return true; }

} // namespace my_custom_arm_hw

#include <pluginlib/class_list_macros.hpp>
PLUGINLIB_EXPORT_CLASS(my_custom_arm_hw::CustomTcpHardware, hardware_interface::SystemInterface)
