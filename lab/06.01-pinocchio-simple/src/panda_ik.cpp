#include <iostream>
#include "pinocchio/parsers/urdf.hpp"
#include "pinocchio/algorithm/kinematics.hpp"
#include "pinocchio/algorithm/jacobian.hpp"
#include "pinocchio/algorithm/joint-configuration.hpp"

int main() {
    // 1. 設定 URDF 路徑 (請確保路徑正確，或從 example-robot-data 取得)
    const std::string urdf_filename = "/workspace/src/panda.urdf";
    
    // 2. 載入模型
    pinocchio::Model model;
    pinocchio::urdf::buildModel(urdf_filename, model);
    pinocchio::Data data(model);

    // 3. 定義目標位姿 (SE3)
    const int JOINT_ID = model.getJointId("panda_joint7"); // 追蹤第7個關節
    pinocchio::SE3 oMdes(Eigen::Matrix3d::Identity(), Eigen::Vector3d(0.5, 0.2, 0.5));

    // 4. 初始化變數
    Eigen::VectorXd q = pinocchio::neutral(model); // 初始姿勢
    const double eps  = 1e-4;   // 容許誤差
    const int IT_MAX  = 1000;   // 最大迭代次數
    const double DT   = 0.1;    // 步長
    const double damp = 1e-6;   // 阻尼係數 (防止奇異點)

    pinocchio::Data::Matrix6x J(6, model.nv);
    J.setZero();
    bool success = false;

    // 5. 迭代求解 (CLIK 演算法)
    for (int i = 0; i < IT_MAX; i++) {
        // 更新正向運動學與雅可比矩陣
        pinocchio::forwardKinematics(model, data, q);
        const pinocchio::SE3 dMi = oMdes.actInv(data.oMi[JOINT_ID]);
        
        // 計算誤差向量 (空間速度)
        Eigen::Matrix<double, 6, 1> err = pinocchio::log6(dMi).toVector();
        if (err.norm() < eps) {
            success = true;
            break;
        }

        // 計算雅可比矩陣並求解關節速度 v
        pinocchio::computeJointJacobian(model, data, q, JOINT_ID, J);
        pinocchio::Data::Matrix6 JJt = J * J.transpose();
        JJt.diagonal().array() += damp;
        
        Eigen::VectorXd v = -J.transpose() * JJt.ldlt().solve(err);
        
        // 更新關節位置
        q = pinocchio::integrate(model, q, v * DT);
    }

    if (success) {
        std::cout << "收斂成功！最終關節角度: " << q.transpose() << std::endl;
    } else {
        std::cout << "未能收斂。" << std::endl;
    }

    return 0;
}

