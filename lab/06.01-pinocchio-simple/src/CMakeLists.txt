cmake_minimum_required(VERSION 3.10)

# 專案名稱
project(PandaIKExample)

# 設定 C++ 標準 (Pinocchio 至少需要 C++11，建議使用 14 或 17)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 1. 尋找必要的套件
# pinocchio 會自動尋找相關依賴 (如 Eigen3, Boost)
find_package(pinocchio REQUIRED)
find_package(Eigen3 REQUIRED)

# 2. 加入執行檔
add_executable(panda_ik panda_ik.cpp)

# 3. 設定標頭檔路徑 (Include Directories)
target_include_directories(panda_ik PRIVATE ${EIGEN3_INCLUDE_DIR})

# 4. 連結函式庫 (Link Libraries)
# Pinocchio 使用現代 CMake 標靶 (Target)，會自動處理依賴關係
target_link_libraries(panda_ik PUBLIC pinocchio::pinocchio)

# 如果你的系統中 Pinocchio 需要額外的 Boost 支援，可以解開下方註解
# find_package(Boost REQUIRED)
# target_link_libraries(panda_ik PUBLIC ${Boost_LIBRARIES})

