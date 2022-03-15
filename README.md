# rosbag2_evaluation

The rosbag2_evaluation package tests message loss and jitter of rosbag2.
It uses ROS 2 galactic and performance_test tool (by Apex.AI) for evaluation.

Some scripts of ROS 2 galactic and performance_test have been modified to fit this package.
Therefore, you need to rewrite from the original scripts to modified scripts.

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
1.Set evaluation parameters

Open a yaml file ("rosbag2_evaluation/src/rosbag2_evaluation_parameters.yaml") and set parameters enclosed in [].
- **fixed** : don't change these parameters.
- **free** : you can set an integer value you like.
- **"free",...** : you can set some interger values you like (for dds, you can set RMW_IMPLEMENTATION parameters. This package implements only rmw_cyclonedds_cpp and rmw_fastrtps_cpp).
 
2.Start rosbag2_evaluation


```
cd /rosbag2_evaluation/src
python3 eval_rosbag2.py
```


## Visualize
1.Message loss

2.Jitter

Jitter of rosbag2 is visualizing by R scripts (for exmaple, "rosbag2_evaluation/src/boxplot_for_thesis/basic/basic_dds_r_20.r").
If you want to run R scripts in this package, you must change output data paths refferenced in R scripts.

Output datas by rosbag2_evaluation are placed in [GoogleDrive][3].
Output datas must be placed in "rosbag2_evaluation/src/".

[1]:https://docs.ros.org/en/galactic/Installation/Ubuntu-Development-Setup.html
[2]:https://gitlab.com/ApexAI/performance_test
[3]:https://drive.google.com/file/d/1rf3QdKASaFHtoBIjgvooUg3sdyv96l7A/view?usp=sharing
