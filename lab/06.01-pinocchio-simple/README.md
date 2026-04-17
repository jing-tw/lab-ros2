# Move Robot

## Quick
```
# pull the source
git clone git@github.com:jing-tw/lab-ros2.git
cd labs/06.1-pinocchio-simple


# build image
. ./init_container.sh

# into the container
. ./start.sh

# dev
# c++ example 
cd src
mkdir build && cd build
cmake ..
make
panda_ik  # run

# python example
pip install pin
python3 panda_ik.py  # run

# clean
./clean._container.sh
```


## DEV 
```
# check the node, link, end_effector_name
ros2 run xacro xacro $(ros2 pkg prefix --share franka_description)/robots/fr3/fr3.urdf.xacro > /tmp/fr3.urdf
grep "joint name=" /tmp/fr3.urdf | head -10   # joint name
grep -E 'link name="fr3_link0"' /tmp/fr3.urdf # base link name
grep -E 'name="fr3_link[6-9]|fr3_hand|hand|flange|tcp' /tmp/fr3.urdf   # end effector name
```

# References
1. https://docs.google.com/document/d/17W982jvqyqAQ-Qc_H7OXPXbHFJvw3S9N9zEyenE1SG8/edit?usp=sharing
2. [ik, pinocchio] How to use Pinocchio in IK for Panda Robot, https://docs.google.com/document/d/1hA4pq42xYktnqphEHdOqoVa3RFcLyiuJ1hlpi4EwF_s/edit?usp=sharing

