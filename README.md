# rosbag2_evaluation

The rosbag2_evaluation package tests message loss and jitter of rosbag2.
It uses ROS 2 galactic and performance_test tool (by Apex.AI) for evaluation.

Some scripts of ROS 2 galactic and performance_test have been modified to fit this package.
Therefore, you need to rewrite from the original scripts to modified scripts.

## Requirements

You must install the following two.
ROS 2 galactic must be installed at **source**, not binary.
- [ROS 2 galactic][1] (Ubuntu 20.04)
- [performance_test][2]

## Rewrite scripts

1.Clone the repository
```
git clone https://github.com/azu-lab/rosbag2_evaluation.git
```

2.Rewrite some scripts from original scripts

The bold text below indicates the files for each user's ROS 2 galactic and performance_test environment.

ROS 2 galactic
- "rosbag2_evaluation/rewrite_scripts/player.cpp" -> **"ros2_galactic/src/ros2/rosbag2/rosbag2_transport/src/rosbag2_transport/player.cpp"**

performance_test
- "rosbag2_evaluation/rewrite_scripts/rclcpp_communicator.hpp" -> **"perf_test_ws/src/performance_test/performance_test/src/communication_abstractions/rclcpp_communicator.hpp"**
- "rosbag2_evaluation/rewrite_scripts/stdout_output.cpp" -> **"perf_test_ws/src/performance_test/performance_test/src/outputs/stdout_output.cpp"**

## Rebuild

1.Rebuild

performance_test
```
cd perf_test_ws/
colcon build
```

ROS 2 galactic
```
cd ros2_galactic/
colcon build --packages-select rosbag2_transport
```

2.Set environment variables
```
source ros2_galactic/install/setup.bash
source perf_test_ws/install/setup.bash
```

## Evaluation
1.Set evaluation parameters (optional)

Open a yaml file ("rosbag2_evaluation/src/rosbag2_evaluation_parameters.yaml") and set parameters enclosed in commented out [].
- **fixed** : don't change these parameters.
- **free** : you can set an integer value you like.
- **"free",...** : you can set some interger values you like (for dds, you can set RMW_IMPLEMENTATION parameters. This package implements only rmw_cyclonedds_cpp and rmw_fastrtps_cpp).
 
2.Start rosbag2_evaluation

```
cd rosbag2_evaluation/src/
python3 eval_rosbag2.py
```


## Visualize
1.Message loss

Message loss results of rosbag2 record are visualizing by LaTeX table.
They are in number_of_message_loss directory.

2.Jitter

Jitter results of rosbag2 are visualizing by R scripts (for exmaple, "rosbag2_evaluation/src/boxplot_for_thesis/basic/basic_dds_r_20.r").
If you want to run R scripts in this package, you must **[install R][4] and change output data paths** refferenced in R scripts.

Output datas by rosbag2_evaluation are placed in [GoogleDrive][3].
Output datas must be placed in "rosbag2_evaluation/src/".

## Future work
It is important to be able to set A in B.
Therefore, the performance_test package should be edited to allow the number of publish to be used as a new argument.

The R script code is verbose, so this can also be done in a simplified manner.

[1]:https://docs.ros.org/en/galactic/Installation/Ubuntu-Development-Setup.html
[2]:https://gitlab.com/ApexAI/performance_test
[3]:https://drive.google.com/file/d/1rf3QdKASaFHtoBIjgvooUg3sdyv96l7A/view?usp=sharing
[4]:https://cloud.r-project.org/
