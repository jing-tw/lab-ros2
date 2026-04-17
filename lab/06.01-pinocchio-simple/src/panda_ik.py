# Reference
# https://gemini.google.com/share/5c17aca257f9
import numpy as np
import pinocchio as pin
import sys

def run_ik_example():
    # 1. 載入模型
    # 建議安裝: pip install example-robot-data
    try:
        from example_robot_data import load
        robot = load('panda')
        model = robot.model
    except ImportError:
        # 如果沒有範例資料庫，則使用你的 URDF 路徑
        urdf_filename = "/workspace/src/panda.urdf"
        model = pin.buildModelFromUrdf(urdf_filename)
    
    data = model.createData()

    # 2. 定義目標位姿 (SE3)
    # 追蹤 "panda_joint7"
    joint_name = "panda_joint7"
    if not model.existJointName(joint_name):
        print(f"錯誤: 找不到關節 {joint_name}")
        return

    JOINT_ID = model.getJointId(joint_name)
    
    # 設定目標位置 [0.5, 0.2, 0.5]，旋轉矩陣為單位矩陣
    oMdes = pin.SE3(np.eye(3), np.array([0.5, 0.2, 0.5]))

    # 3. 初始化變數
    q = pin.neutral(model)  # 初始姿勢 (通常是全 0 或特定中立位)
    eps = 1e-4              # 容許誤差 (Threshold)
    IT_MAX = 1000          # 最大迭代次數
    DT = 0.1               # 步長 (Step size)
    damp = 1e-6            # 阻尼係數 (Damping for Pseudo-inverse)

    success = False

    # 4. 迭代求解 (CLIK 演算法)
    print("開始迭代計算逆向運動學...")
    
    for i in range(IT_MAX):
        # 更新正向運動學：計算各關節在世界座標系下的位置 data.oMi
        pin.forwardKinematics(model, data, q)
        
        # 計算當前位置與目標位置的偏差
        # dMi 表示從目標到當前位置的相對變換
        dMi = oMdes.actInv(data.oMi[JOINT_ID])
        
        # 使用 log6 將 SE3 誤差轉換為切線空間 (Lie Algebra) 的 6D 向量 [v, w]
        err = pin.log6(dMi).vector
        
        # 檢查是否收斂 (使用向量的 Norm)
        if np.linalg.norm(err) < eps:
            success = True
            break

        # 計算當前關節狀態下的雅可比矩陣 (Jacobian)
        # 預設是在局部坐標系下 (LOCAL)
        J = pin.computeJointJacobian(model, data, q, JOINT_ID)
        
        # 求解關節速度 v: 使用帶阻尼的最小二乘法 (Levenberg-Marquardt 風格)
        # 公式: v = - J^T * (J*J^T + damp*I)^-1 * err
        JJt = J @ J.T
        JJt.flat[::7] += damp  # 快速給 6x6 矩陣對角線加上阻尼項
        
        v = - J.T @ np.linalg.solve(JJt, err)
        
        # 更新關節位置 q
        # 注意：對於有旋轉關節的機器人，不能直接 q += v*DT，必須使用 integrate
        q = pin.integrate(model, q, v * DT)

        if i % 100 == 0:
            print(f"迭代次數: {i:4d}, 誤差值: {np.linalg.norm(err):.6f}")

    # 5. 輸出最終結果
    print("-" * 30)
    if success:
        print(f"收斂成功！")
        print(f"最終迭代次數: {i}")
        print("最終關節角度 (q):")
        print(q.round(4)) # 四捨五入到小數點後四位
    else:
        print("未能及時收斂，請檢查目標位姿是否在工作空間內。")

if __name__ == "__main__":
    run_ik_example()