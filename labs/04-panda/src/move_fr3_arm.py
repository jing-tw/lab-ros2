#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from pymoveit2 import MoveIt2
from pymoveit2.robots import panda  # not sutited for FR3, but we can still use the same interface
import geometry_msgs.msg   # 如果還沒 import，請加上這行

import tf2_ros
from geometry_msgs.msg import PoseStamped

import time
import math

class PandaMover(Node):
    def __init__(self):
        super().__init__("pfr3_mover")

         # check the names from the robot model
        self.get_logger().info(f"Joint names: {panda.joint_names()}")
        self.get_logger().info(f"base_link names: {panda.base_link_name()}")
        self.get_logger().info(f"end_effector names: {panda.end_effector_name()}")

        # self.moveit2 = MoveIt2(
        #     node=self,
        #     joint_names=panda.joint_names(),
        #     base_link_name=panda.base_link_name(),
        #     end_effector_name=panda.end_effector_name(),
        #     group_name="fr3_arm",
        # )
        

        self.moveit2 = MoveIt2(
            node=self,
            joint_names=[
                "fr3_joint1", "fr3_joint2", "fr3_joint3", "fr3_joint4",
                "fr3_joint5", "fr3_joint6", "fr3_joint7"
            ],
            base_link_name="fr3_link0",      # 通常是 fr3_link0 或 link0，請確認你的 URDF
            end_effector_name="fr3_hand",   # 常見是 fr3_link7 或 fr3_hand
            group_name="fr3_arm",
        )

        
        # === 關鍵調整：大幅降低速度與加速度，讓執行更容易通過 ===
        self.moveit2.max_velocity = 1.0 #0.08      # 原本 0.15 → 降到很慢
        self.moveit2.max_acceleration = 1.0 # 0.08

        # TF2 用於取得 Cartesian pose
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        
        self.get_logger().info("✅ Robot pymoveit2 介面已準備好！")

    def move_to_safe_home(self):
        """使用非常安全的 home 姿勢（避開常見碰撞區域）"""
        self.get_logger().info("移動到安全 home 姿勢...")
        
        # 多等一點時間讓 MoveIt2 完全同步
        self.get_logger().info("等待 MoveIt2 同步 joint states...")
        for i in range(15):   # 最多等約 1.5 秒
            if self.moveit2.joint_state is not None:
                self.get_logger().info("✅ Joint states 已就緒")
                break
            rclpy.spin_once(self, timeout_sec=0.1)

        # 這個姿勢比較保守，不容易自碰撞
        safe_joints_deg = [11.0, 59.0, 18.0, -73.0, -20.0, 130.0, 78.0]
        safe_joints = [math.radians(deg) for deg in safe_joints_deg]
        self.get_logger().info(" ==================================================== ")
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

    # def get_current_pose(self):
    #     """取得目前 End-Effector 的姿勢 (使用 Forward Kinematics)"""
    #     self.get_logger().info("正在取得目前 End-Effector 姿勢...")

    #     # 方法1：使用 joint_state 計算 FK（pymoveit2 推薦方式）
    #     current_joints = self.moveit2.joint_state   # 這是正確屬性

    #     if current_joints is None or len(current_joints.position) == 0:
    #         self.get_logger().warn("目前還沒有 joint states")
    #         return None

    #     self.get_logger().info(f"目前關節角度: {current_joints}")

    #     # 方法2：如果想直接取得 Pose，可以用以下方式（較進階）
    #     # 但 pymoveit2 本身沒有內建 get_current_pose，我們可以用 TF 或 moveit_py 輔助

    #     # 簡單印出關節角度（先這樣除錯）
    #     self.get_logger().info("=== 目前關節狀態 ===")
    #     for name, pos in zip(self.moveit2.joint_names, current_joints.position):
    #         self.get_logger().info(f"  {name}: {pos:.4f} rad")

    #     # TODO: 如果你之後想取得完整 Pose，可以切換到 moveit_py
    #     return current_joints

    def print_current_joints(self):
        """印出目前所有關節角度（最可靠）"""
        joints = self.moveit2.joint_state
        if joints is None:
            self.get_logger().warn("Joint states 尚未可用")
            return
        
        self.get_logger().info("=== 目前關節角度 ===")
        for name, value in zip(self.moveit2.joint_names, joints.position):
            self.get_logger().info(f"  {name:15s}: {value:8.4f} rad ({value*180/3.1416:6.1f} deg)")

   

    # def get_current_cartesian_pose(self):
    #     """取得目前 end-effector 的笛卡爾座標 (position + orientation)"""
    #     try:
    #         # 取得目前 Pose (PoseStamped)
    #         current_pose = self.moveit2.get_current_pose()
            
    #         if current_pose is None:
    #             self.get_logger().warn("無法取得目前 Cartesian pose (回傳 None)")
    #             return None

    #         pose = current_pose.pose   # geometry_msgs.msg.Pose
            
    #         # 印出易讀的資訊
    #         self.get_logger().info("=== 当前 Cartesian Pose (TCP) ===")
    #         self.get_logger().info(f"Reference Frame: {current_pose.header.frame_id}")
    #         self.get_logger().info(f"Position (x, y, z): "
    #                              f"{pose.position.x:.4f}, {pose.position.y:.4f}, {pose.position.z:.4f}")
    #         self.get_logger().info(f"Orientation (qx, qy, qz, qw): "
    #                              f"{pose.orientation.x:.4f}, {pose.orientation.y:.4f}, "
    #                              f"{pose.orientation.z:.4f}, {pose.orientation.w:.4f}")
            
    #         return current_pose   # 回傳完整的 PoseStamped
            
    #     except Exception as e:
    #         self.get_logger().error(f"取得 Cartesian pose 時發生錯誤: {e}")
    #         return None
    def get_current_cartesian_pose(self):
        """使用 TF2 取得目前 end-effector 的 Cartesian pose"""
        try:
            # 建立 TF2 buffer（建議在 __init__ 中建立一次 self.tf_buffer）
            if not hasattr(self, 'tf_buffer'):
                self.tf_buffer = tf2_ros.Buffer()
                self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

            # 等待 transform 可用（最多等 2 秒）
            transform = self.tf_buffer.lookup_transform(
                target_frame="fr3_link0",           # base frame
                source_frame=self.moveit2.end_effector_link if hasattr(self.moveit2, 'end_effector_link') else "fr3_hand",
                time=rclpy.time.Time(),             # 最新時間
                timeout=rclpy.duration.Duration(seconds=2.0)
            )

            # 轉成 PoseStamped
            pose_stamped = PoseStamped()
            pose_stamped.header = transform.header
            pose_stamped.pose.position.x = transform.transform.translation.x
            pose_stamped.pose.position.y = transform.transform.translation.y
            pose_stamped.pose.position.z = transform.transform.translation.z
            pose_stamped.pose.orientation = transform.transform.rotation

            # 印出資訊
            self.get_logger().info("=== Current Cartesian Pose (TF2) ===")
            self.get_logger().info(f"Frame: {pose_stamped.header.frame_id}")
            p = pose_stamped.pose.position
            q = pose_stamped.pose.orientation
            self.get_logger().info(f"Position: x={p.x:.4f}, y={p.y:.4f}, z={p.z:.4f}")
            self.get_logger().info(f"Orientation (xyzw): {q.x:.4f}, {q.y:.4f}, {q.z:.4f}, {q.w:.4f}")

            return pose_stamped

        except tf2_ros.LookupException as e:
            self.get_logger().warn(f"TF2 Lookup 失敗 (可能還沒 broadcast): {e}")
        except tf2_ros.TransformException as e:
            self.get_logger().warn(f"TF2 Transform 錯誤: {e}")
        except Exception as e:
            self.get_logger().error(f"取得 Cartesian pose 時發生錯誤: {e}")

        return None

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


        # node.get_current_pose()      # 印出目前姿勢資訊
        node.get_current_cartesian_pose()  # 印出目前笛卡爾位姿資訊
        node.print_current_joints()    # 印出目前關節角度
       # time.sleep(2.0)
       # node.move_cartesian_safe()   # 如果上面還是 abort，可以試這個
        #time.sleep(2.0)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()