# rosbag2_evaluation

The rosbag2_evaluation tool tests message loss and jitter of rosbag2.
It uses ROS 2 galactic and performance_test tool (by Apex.AI) for evaluation.

Some scripts of ROS 2 galactic and performance_test have been modified to fit this tool.
Therefore, they need to be rewritten from the original scripts.

## Requirements
- [ROS 2 galactic][1] (Ubuntu 20.04)
- [performance_test][2]

## Rewrite scripts
1.Clone the repository
```
git clone https://github.com/azu-lab/rosbag2_evaluation.git
```

2.Rewrite some scripts from original scripts

ROS 2 galactic
- "ros2_galactic/src/ros2/rosbag2/rosbag2_transport/src/rosbag2_transport/player.cpp" -> "rosbag2_evaluation/rewrite_scripts/player.cpp" 

performance_test
- "perf_test_ws/src/performance_test/performance_test/src/communication_abstractions/rclcpp_communicator.hpp" -> "rosbag2_evaluation/rewrite_scripts/rclcpp_communicator.hpp"
- "perf_test_ws/src/performance_test/performance_test/src/outputs/stdout_output.cpp" -> "rosbag2_evaluation/rewrite_scripts/stdout_output.cpp"

## Build
1.Set environment variables
```
source /ros2_galactic/install/setup.bash
source /perf_test_ws/install/setup.bash
```
2.Build

Build the performance_test
```
cd /perf_test_ws
colcon build
```

Build ROS 2 galactic
```
cd /ros2_galactic
```
If the package build is complete except for rosbag2_transport 
```
colcon build --packages-select rosbag2_transport
```
else
```
colcon build
```

## Evaluation
1.Set environment variables

Open a new terminal
```
```
[1]:https://docs.ros.org/en/galactic/Installation/Ubuntu-Development-Setup.html
[2]:https://gitlab.com/ApexAI/performance_test
