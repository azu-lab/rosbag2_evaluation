# rosbag2_evaluation

The rosbag2_evaluation tool tests message loss and jitter of rosbag2.
It uses ROS 2 galactic and performance_test tool for evaluation.

Some scripts have been modified to fit this tool.
Therefore, they need to be rewritten from the original scripts.

## Requirements
- [ROS 2 galactic][1] (Ubuntu 20.04)
- [performance_test][2]

## Rewrite scripts
1.Clone the repository
```
git clone https://github.com/azu-lab/rosbag2_evaluation.git
```

2.Rewrite .cpp script
- Rewrite script "ros2_galactic/src/ros2/rosbag2/rosbag2_transport/src/rosbag2_transport/player.cpp" to "rosbag2_evaluation/cpp_scripts/player.cpp"

## Build
1.Set environment variables
```
source /ros2_galactic/install/setup.bash
source /perf_test_ws/install/setup.bash
```
2.Build
```
cd /ros2_galactic
```
if build of ros2_galactic is complete, 
```
colcon build --packages-select rosbag2_transport
```
else
```
colcon build
```

```
cd /perf_test_ws
colcon build
```
## Evaluation
1.Set environment variables

Open a new terminal
```
```
[1]:https://docs.ros.org/en/galactic/Installation/Ubuntu-Development-Setup.html
[2]:https://gitlab.com/ApexAI/performance_test
