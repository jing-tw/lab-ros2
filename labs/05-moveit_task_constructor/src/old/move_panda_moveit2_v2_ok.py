#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from pymoveit2 import MoveIt2
from pymoveit2.robots import panda
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
        
        # === 關鍵調整：大幅降低速度與加速度，讓執行更容易通過 ===
        self.moveit2.max_velocity = 0.08      # 原本 0.15 → 降到很慢
        self.moveit2.max_acceleration = 0.08
        
        self.get_logger().info("✅ Panda pymoveit2 介面已準備好！（已降低速度）")

    def move_to_safe_home(self):
        """使用非常安全的 home 姿勢（避開常見碰撞區域）"""
        self.get_logger().info("移動到安全 home 姿勢...")
        
        # 這個姿勢比較保守，不容易自碰撞
        safe_joints = [0.0, -0.3, 0.0, -1.8, 0.0, 1.8, 0.8]
        
        self.moveit2.move_to_configuration(safe_joints)
        self.moveit2.wait_until_executed()
        self.get_logger().info("✅ 安全 home 姿勢完成")

    def move_cartesian_safe(self):
        """使用笛卡爾空間移動（通常比關節空間更穩定）"""
        from geometry_msgs.msg import Pose
        self.get_logger().info("移動到安全笛卡爾位置...")
        
        pose = Pose()
        pose.position.x = 0.35
        pose.position.y = 0.0
        pose.position.z = 0.45
        pose.orientation.w = 1.0
        
        self.moveit2.move_to_pose(pose)
        self.moveit2.wait_until_executed()
        self.get_logger().info("✅ 笛卡爾安全移動完成")

    def get_current_pose(self):
        """取得目前 End-Effector 的姿勢 (使用 Forward Kinematics)"""
        self.get_logger().info("正在取得目前 End-Effector 姿勢...")

        # 方法1：使用 joint_state 計算 FK（pymoveit2 推薦方式）
        current_joints = self.moveit2.joint_state   # 這是正確屬性

        if current_joints is None or len(current_joints.position) == 0:
            self.get_logger().warn("目前還沒有 joint states")
            return None

        self.get_logger().info(f"目前關節角度: {current_joints}")

        # 方法2：如果想直接取得 Pose，可以用以下方式（較進階）
        # 但 pymoveit2 本身沒有內建 get_current_pose，我們可以用 TF 或 moveit_py 輔助

        # 簡單印出關節角度（先這樣除錯）
        self.get_logger().info("=== 目前關節狀態 ===")
        for name, pos in zip(self.moveit2.joint_names, current_joints.position):
            self.get_logger().info(f"  {name}: {pos:.4f} rad")

        # TODO: 如果你之後想取得完整 Pose，可以切換到 moveit_py
        return current_joints

    def print_current_joints(self):
        """印出目前所有關節角度（最可靠）"""
        joints = self.moveit2.joint_state
        if joints is None:
            self.get_logger().warn("Joint states 尚未可用")
            return
        
        self.get_logger().info("=== 目前關節角度 ===")
        for name, value in zip(self.moveit2.joint_names, joints.position):
            self.get_logger().info(f"  {name:15s}: {value:8.4f} rad ({value*180/3.1416:6.1f} deg)")

    def get_end_effector_pose(self):
        """如果想取得 Pose，建議改用 moveit_py（pymoveit2 較弱）"""
        self.get_logger().info("pymoveit2 沒有直接 get_current_pose()，建議使用 moveit_py")
        self.print_current_joints()

def main():
    rclpy.init()
    node = PandaMover()
    
    try:
        time.sleep(4.0)        # 多給一點時間讓 joint_states 穩定
        node.move_to_safe_home()     # 先試這個保守姿勢
        time.sleep(2.0)
        node.get_current_pose()      # 印出目前姿勢資訊
        node.print_current_joints()    # 印出目前關節角度
        #time.sleep(2.0)
        # node.move_cartesian_safe()   # 如果上面還是 abort，可以試這個
        time.sleep(2.0)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()