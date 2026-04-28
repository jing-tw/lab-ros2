from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'my_custom_arm_hw'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        # 讓 ROS 2 能找到這個 package
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        
        # 安裝 package.xml
        ('share/' + package_name, ['package.xml']),
        
        # === 安裝 launch 檔案（最重要的部分）===
        (os.path.join('share', package_name, 'launch'), 
         glob('launch/*.launch.py')),
        
        # === 安裝 config 檔案 ===
        (os.path.join('share', package_name, 'config'), 
         glob('config/*.yaml')),
        
        # === 安裝 urdf / xacro 相關檔案（全部安裝）===
        (os.path.join('share', package_name, 'urdf'), 
         glob('urdf/*.xacro')),
        (os.path.join('share', package_name, 'urdf'), 
         glob('urdf/*.yaml')),
        (os.path.join('share', package_name, 'urdf'), 
         glob('urdf/*.urdf')),
        
        # 如果 urdf 裡還有子資料夾（例如 old/），可以再加：
        # (os.path.join('share', package_name, 'urdf/old'), 
        #  glob('urdf/old/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='你的名字',          # ← 請修改
    maintainer_email='你的email@example.com',  # ← 請修改
    description='Custom TCP/IP hardware interface for ros2_control',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # 如果未來有 Python node 可以加在這裡，目前留空即可
        ],
    },
)