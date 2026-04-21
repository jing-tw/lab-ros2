#!/usr/bin/env python3

from pymoveit2 import MoveIt2
# from pymoveit2.robots import panda
from geometry_msgs.msg import Pose
from rclpy.node import Node

from moveit_msgs.msg import RobotState
from moveit_msgs.srv import GetPositionFK
from moveit_msgs.msg import RobotState
from geometry_msgs.msg import PoseStamped

import tf2_ros
import time
import math
import rclpy

class PandaMover(Node):
    # Usage:
    # Panda info: The information can be obtained from the URDF but here we hardcode it for simplicity.
    # name = "panda_mover"
    # joint_names=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']
    # base_link_name = "panda_link0"   # 注意：這裡改成 "panda_link0"（不是 world），因為我們的 FK Service 是以 link0 為參考的
    # end_effector_name = "panda_hand"   # 注意：這裡改成 "panda_hand"（不是 tcp），因為我們的 FK Service 是以 hand 為目標的
    # group_name = "panda_arm"
    # node = PandaMover(name, joint_names, base_link_name, end_effector_name, group_name)
    def __init__(self, name, joint_names, base_link_name, end_effector_name, group_name):
        super().__init__(name)

        self.moveit2 = MoveIt2(
            node=self, 
            joint_names=joint_names,
            base_link_name=base_link_name,          
            end_effector_name=end_effector_name,
            group_name=group_name
        )
        
        # === 關鍵調整：大幅降低速度與加速度，讓執行更容易通過 ===
        self.moveit2.max_velocity = 0.15 # 0.08      # 原本 0.15 → 降到很慢
        self.moveit2.max_acceleration = 0.08
        # self.moveit2.max_planning_time = 10.0          # 最大允許規劃時間（秒）
        # self.moveit2.num_planning_attempts = 10        # 規劃失敗時重試次數
        # self.moveit2.allowed_planning_time = 10.0      # 有些版本用這個屬性
                
        self.get_logger().info("✅ pymoveit2 介面已準備好！")

    def move_to_joint_positions(self, joint_positions=None):
        """使用非常安全的 home 姿勢（避開常見碰撞區域）"""
        self.get_logger().info("移動到安全 home 姿勢...")
        
        # 這個姿勢比較保守，不容易自碰撞
        # safe_joints = [0.0, -0.3, 0.0, -1.8, 0.0, 1.8, 0.8]
        
        self.moveit2.move_to_configuration(joint_positions)
        self.moveit2.wait_until_executed()
        self.get_logger().info("✅ 安全 home 姿勢完成")


    def move_cartesian_deg(self, x, y, z, roll_deg=0.0, pitch_deg=0.0, yaw_deg=0.0):
        """
        使用笛卡爾空間移動 - Euler 角度版本（度數）
        roll, pitch, yaw 單位為「度」 degrees
        """
        self.get_logger().info(f"移動到安全笛卡爾位置... "
                            f"xyz=({x:.3f}, {y:.3f}, {z:.3f}), "
                            f"rpy=({roll_deg:.3f}, {pitch_deg:.3f}, {yaw_deg:.3f})°")

        # === 度數 → 弧度 轉換 ===
        roll_rad = math.radians(roll_deg)
        pitch_rad = math.radians(pitch_deg)
        yaw_rad = math.radians(yaw_deg)

        # invoke move_cartesian_rand with radians
        self.move_cartesian_rand(x, y, z, roll_rad, pitch_rad, yaw_rad)

        # # Euler → Quaternion 轉換
        # q = self._quaternion_from_euler(roll_rad, pitch_rad, yaw_rad)
        # self.move_cartesian_q(x, y, z, q[0], q[1], q[2], q[3])
        
        self.get_logger().info("✅ 笛卡爾安全移動完成 (Degrees 版本)")

    def move_cartesian_rand(self, x, y, z, roll_rad=0.0, pitch_rad=0.0, yaw_rad=0.0):
        """
        使用笛卡爾空間移動 - Euler 角度版本
        roll, pitch, yaw 單位為「弧度」 radians
        """
        self.get_logger().info(f"移動到安全笛卡爾位置... "
                            f"xyz=({x:.3f}, {y:.3f}, {z:.3f}), "
                            f"rpy=({roll_rad:.3f}, {pitch_rad:.3f}, {yaw_rad:.3f})")

        # === Euler → Quaternion 轉換（純 Python）===
        q = self._quaternion_from_euler(roll_rad, pitch_rad, yaw_rad)
        self.move_cartesian_q(x, y, z, q[0], q[1], q[2], q[3])
        self.get_logger().info("✅ 笛卡爾安全移動完成 (Euler 版本)")
    
    def move_cartesian_q(self, x, y, z, qx, qy, qz, qw):
        
        
        self.get_logger().info(f"移動到安全笛卡爾位置... "
                            f"xyz=({x:.3f}, {y:.3f}, {z:.3f}), "
                            f"oientation=({qx:.3f}, {qy:.3f}, {qz:.3f}, {qw:.3f})")

        # 建立 Pose
        pose = Pose()
        
        # === 位置 ===
        pose.position.x = x
        pose.position.y = y
        pose.position.z = z
        pose.orientation.x = qx
        pose.orientation.y = qy
        pose.orientation.z = qz
        pose.orientation.w = qw

        # 執行移動
        # self.moveit2.move_to_pose(pose)
        self.moveit2.move_to_pose(pose, "world")   # 明確指定參考座標系（通常是 "world" 或 "panda_link0"）
        self.moveit2.wait_until_executed()
        
        self.get_logger().info("✅ 笛卡爾安全移動完成 (Euler 版本)")

    
    def _quaternion_from_euler(self, roll, pitch, yaw):
        """純 Python 版本的 Euler to Quaternion 轉換 (ZYX 順序)"""
        import math
        
        cy = math.cos(yaw * 0.5)
        sy = math.sin(yaw * 0.5)
        cp = math.cos(pitch * 0.5)
        sp = math.sin(pitch * 0.5)
        cr = math.cos(roll * 0.5)
        sr = math.sin(roll * 0.5)

        qx = cy * cp * sr - sy * sp * cr
        qy = sy * cp * sr + cy * sp * cr
        qz = sy * cp * cr - cy * sp * sr
        qw = cy * cp * cr + sy * sp * sr

        return [qx, qy, qz, qw]   # ROS 的順序是 x, y, z, w


    def get_current_joint_states(self):
        """從 pymoveit2 內部的 joint state 取得目前 Cartesian Pose（最終穩定版）"""
        # 1. Compare the python code with echo command. OK
        #    ros2 topic echo /joint_states
        try:
            self.get_logger().info("正在取得目前 End-Effector 姿勢 (使用 JointState)...")

            # 檢查是否有最新的 joint state
            if not hasattr(self.moveit2, '_MoveIt2__joint_state') or self.moveit2._MoveIt2__joint_state is None:
                self.get_logger().warning("目前還沒有收到 JointState 資料")
                return None

            joint_state = self.moveit2._MoveIt2__joint_state

            self.get_logger().info(f"已取得 {len(joint_state.position)} 個關節角度")

            # 印出目前關節角度（已經在你的程式中做了）
            # 暫時先回傳 None + 詳細 log（因為我們還沒接 FK）
            self.get_logger().info("=== Joint State 目前值 ===")
            for name, pos in zip(joint_state.name, joint_state.position):
                if "panda_joint" in name:   # 只顯示 arm 的 joint
                    deg = math.degrees(pos)
                    self.get_logger().info(f"  {name:15} : {pos:8.4f} rad ({deg:6.1f} deg)")
            return None 

        except Exception as e:
            self.get_logger().error(f"取得 Joint State 失敗: {e}")
            return None

    def get_current_cartesian_pose(self, header_frame="world", fk_link_name="panda_hand"):
        """使用 Forward Kinematics 計算目前 End-Effector Cartesian Pose"""
        try:
            self.get_logger().info("正在計算目前 End-Effector Cartesian Pose (FK)...")

            if not hasattr(self.moveit2, '_MoveIt2__joint_state') or self.moveit2._MoveIt2__joint_state is None:
                self.get_logger().warning("尚未收到 JointState")
                return None

            joint_state = self.moveit2._MoveIt2__joint_state

            # 建立 FK 請求
            fk_request = GetPositionFK.Request()
            fk_request.header.stamp = self.get_clock().now().to_msg()
            fk_request.header.frame_id = header_frame       # 明確指定參考座標系（通常是 "world" 或 "panda_link0"）
            fk_request.fk_link_names = [fk_link_name]       # 讓使用者可以指定要查哪個 link 的 pose，預設是 "panda_hand"

            # 填入目前關節狀態
            robot_state = RobotState()
            robot_state.joint_state = joint_state
            fk_request.robot_state = robot_state

            # 呼叫 FK Service
            fk_client = self.create_client(GetPositionFK, '/compute_fk')
            
            if not fk_client.wait_for_service(timeout_sec=3.0):
                self.get_logger().error("FK Service (/compute_fk) 未準備好")
                return None

            future = fk_client.call_async(fk_request)
            rclpy.spin_until_future_complete(self, future, timeout_sec=3.0)

            if future.result() is None:
                self.get_logger().error("FK 呼叫失敗")
                return None

            response = future.result()

            if response.error_code.val != 1:   # 1 = SUCCESS
                self.get_logger().error(f"FK 計算失敗，error code: {response.error_code.val}")
                return None

            # 取得 Pose
            pose_stamped = response.pose_stamped[0]

            # 印出結果
            self.get_logger().info("=== Current Cartesian Pose (FK) ===")
            self.get_logger().info(f"Frame: {pose_stamped.header.frame_id}")
            
            p = pose_stamped.pose.position
            q = pose_stamped.pose.orientation
            self.get_logger().info(f"Position: x={p.x:.4f}, y={p.y:.4f}, z={p.z:.4f}")
            self.get_logger().info(f"Orientation (xyzw): {q.x:.4f}, {q.y:.4f}, {q.z:.4f}, {q.w:.4f}")

            return pose_stamped

        except Exception as e:
            self.get_logger().error(f"Forward Kinematics 計算失敗: {e}")
            return None
def main():
    rclpy.init()
    # Panda info: The information can be obtained from the URDF, but here we hardcode it for simplicity.
    name = "panda_mover"
    joint_names=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']
    base_link_name = "panda_link0"   # 注意：這裡改成 "panda_link0"（不是 world），因為我們的 FK Service 是以 link0 為參考的
    end_effector_name = "panda_hand"   # 注意：這裡改成 "panda_hand"（不是 tcp），因為我們的 FK Service 是以 hand 為目標的
    group_name = "panda_arm"
    node = PandaMover(name, joint_names, base_link_name, end_effector_name, group_name)
    
    try:
        #time.sleep(4.0)        # 多給一點時間讓 joint_states 穩定
        ## Test: move_to_joint_positions: OK
        # time.sleep(2.0)
        # node.move_to_joint_positions([0.0, -0.3, 0.0, -1.8, 0.0, 1.8, 0.8])     # 先試這個保守姿勢
        # node.get_current_joint_states()     # print current joint states (for debugging)
        # node.get_current_cartesian_pose("world", "panda_hand")   # print cartesian pose using FK
   

        # Test: move_cartesian_q: OK
        # time.sleep(2.0)
        # node.move_cartesian_q(0.4786, -0.0005, 0.6933, 0.9886, -0.0075, 0.1502, -0.0014)
        # node.get_current_joint_states()     # print current joint states (for debugging)
        # node.get_current_cartesian_pose("world", "panda_hand")   # print cartesian pose using FK

        # Test: move_cartesian_deg: step 3: OK
        # time.sleep(2.0)
        # node.move_cartesian_deg(0.4786, -0.0005, 0.6933, roll_deg=0.0, pitch_deg=0.0, yaw_deg=360.0)
        # node.get_current_joint_states()     # print current joint states (for debugging)
        # node.get_current_cartesian_pose("world", "panda_hand")   # print cartesian pose using FK

        # Test: move_cartesian_deg:  OK
        # step 1: roll 0 度，其他不變
        time.sleep(2.0)
        node.move_cartesian_deg(0.4786, -0.0005, 0.6933, roll_deg=0.0, pitch_deg=0.0, yaw_deg=0.0)
        node.get_current_joint_states()     # print current joint states (for debugging)
        node.get_current_cartesian_pose("world", "panda_hand")   # print cartesian pose using FK
       
        # step 2: roll 180 度，其他不變
        time.sleep(5.0)
        node.move_cartesian_deg(0.4786, -0.0005, 0.6933, roll_deg=180.0, pitch_deg=0.0, yaw_deg=0.0)
        node.get_current_joint_states()     # print current joint states (for debugging)
        node.get_current_cartesian_pose("world", "panda_hand")   # print cartesian pose using FK

        # TODO Test: Get Joint name from moveit_commander
        
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()