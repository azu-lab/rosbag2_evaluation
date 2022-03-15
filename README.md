

## Requirements
- ROS 2 galactic (Ubuntu 20.04)

## Build
1.Clone the repository
```
$git clone https://github.com/azu-lab/rosbag2_evaluation.git
```

2.Rewrite .cpp script
Rewrite script "ros2_galactic/src/ros2/rosbag2/rosbag2_transport/src/rosbag2_transport/recorder.cpp" to "rosbag2_evaluation/cpp_scripts/recorder.cpp"
Rewrite script "ros2_galactic/src/ros2/rosbag2/rosbag2_transport/src/rosbag2_transport/player.cpp" to "rosbag2_evaluation/cpp_scripts/player.cpp"


3.Set environment variables
```
$source /ros2_galactic/install/setup.bash
$source /perf_test_ws/install/setup.bash
```
4.Build
```
$cd /ros2_galactic
if build of ros2_galactic is complete, 
$colcon build --packages-select rosbag2_transport
else
$colcon build

$cd /perf_test_ws
$colcon build
```
## Evaluation
1．Set environment variables

Open a new terminal
```
```
