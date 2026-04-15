#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from pymoveit2 import MoveIt2
from pymoveit2.robots import panda
from geometry_msgs.msg import Pose
import time

class PandaMover(Node):
    def __init__(self):
        super().__init__("panda_mover")
        
        self.moveit2 = MoveIt2(
            node=self,
            joint_names=panda.joint_names(),
            base_link_name=panda.base_link_name(),
            end_effector_name=panda.end_effector_name(),
            group_name="panda_arm",
        )
        
        # 可選：設定規劃器
        self.moveit2.planner_id = "RRTConnectkConfigDefault"
        
        self.get_logger().info("✅ Panda pymoveit2 介面已準備好！")

    def move_to_ready(self):
        """使用關節角度移動到 'ready' 姿勢（Panda 常見的初始姿勢）"""
        self.get_logger().info("移動到 'ready' 姿勢...")

        # Panda 'ready' 姿勢的典型關節角度（單位：弧度）
        ready_joints = [0.0, -0.785, 0.0, -2.356, 0.0, 1.571, 0.785]

        # self.moveit2.go_to_joint_state(ready_joints)
        self.moveit2.move_to_configuration(ready_joints)
        self.moveit2.wait_until_executed()   # 等待動作執行完成

        self.get_logger().info("✅ 已到達 ready 姿勢")

    def move_to_home(self):
        """移動到零位姿勢（所有關節為 0）"""
        self.get_logger().info("移動到 home (零位) 姿勢...")
        home_joints = [0.0] * 7
        self.moveit2.move_to_configuration(home_joints)
        self.moveit2.wait_until_executed()
        self.get_logger().info("✅ 已到達 home 姿勢")
        

def main():
    rclpy.init()
    node = PandaMover()
    
    try:
        time.sleep(2.0)          # 等待 MoveIt 完全啟動
        node.move_to_ready()     # 改成 node.move_to_home() 也可以測試
        node.move_to_home()
        time.sleep(1.0)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()