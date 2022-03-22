import signal
import subprocess
import sys
import generate_cmd as gc
import time

def approximate_max_cache_size(topic,rate):
    """
    Calculate approximate of Max Cache Size (record size in 1 second:topic size*rate).

    Parameters
    ----------
    topic : string
    rate : string

    Returns
    ----------
    approximate_mcs : int
        Approximate size of Max Cache Size parameter.
    """
    # Create the dictionary
    mcs_dic = {"Array1k":1044,"Array4k":4116,"Array16k":16404,"Array32k":32768,"Array64k":65556,"Array256k":262164,"Array1m":1048596,"Array2m":2097172,
    "Struct256":532,"Struct4k":8468,"Struct32k":67732,"PointCloud512k":526740,"PointCloud1m":1051028,"PointCloud2m":2099604,"PointCloud4m":4196756,
    "Range":308,"NavSatFix":396,"RadarDetection":84,"RadarTrack":844}
    approximate_mcs = mcs_dic[topic]*int(rate)

    return approximate_mcs

# Get command line arguments for executing this program in eval_rosbag2.py.
nd_mcs_spp_product = list(gc.get_nd_mcs_spp_product()[int(sys.argv[1])]) # Parameters of argv[1]th nd_mcs_spp.
topic = gc.get_perf_test_topics()[int(sys.argv[2])] # Parameters of argv[2]th topic.
rate_d_r_dds_product = list(gc.get_rate_d_r_dds_product()[int(sys.argv[3])]) # Parameters of argv[3]th rate_d_r_dds.
output_path = sys.argv[4]
bagfile_path = output_path + "/bagfile" # Create bagfile in the path of argv[4].
num_of_publish = gc.get_perf_test_num_of_publish()

rate = rate_d_r_dds_product[0]
record_qos_d = rate_d_r_dds_product[1]
record_qos_r = rate_d_r_dds_product[2]
perf_qos_r = "reliable" # fixed
perf_qos_d = "transient" # fixed


no_discovery = nd_mcs_spp_product[0]
max_cache_size = nd_mcs_spp_product[1]
storage_preset_profile = nd_mcs_spp_product[2]

# Create record commands.
record_nd_cmd = ""
record_mcs_cmd = ""
base_spp_cmd = ""
record_spp_cmd = ""
record_qos_cmd = f"record_qos_override/{topic}/{record_qos_r}_{record_qos_d}.yaml"
record_cmd = ""

if no_discovery == "true":
    record_nd_cmd = "--no-discovery"

if max_cache_size == "guide": 
    approximate_mcs = approximate_max_cache_size(topic,rate)
    record_mcs_cmd = f"--max-cache-size {approximate_mcs}"
elif max_cache_size == "default":
    record_mcs_cmd = ""
else:
    record_mcs_cmd = f"--max-cache-size {max_cache_size}"

if storage_preset_profile == "resilient":
    record_spp_cmd = f"--storage-preset-profile resilient"

record_cmd =  f"ros2 bag record /test_{topic} -o {bagfile_path}" 
record_cmd_option = f" --qos-profile-overrides-path {record_qos_cmd} {record_nd_cmd} {record_mcs_cmd} {record_spp_cmd} "
record_cmd += record_cmd_option

record_process = None

class Instance:
    """perf_test process encapsulation."""

    def __init__(self):
        self.process = None

    def run(self):
        """
        Run perf_test and rosbag2 record.
        """
        global record_process
        # If no discovery is true, then perf_test is launched first and the topic is created. 
        # Start the record before publishing the message.
        if no_discovery == "true": 
            self.process = subprocess.Popen(self.perf_cmd(), shell=True)
            time.sleep(0.2) # fixed
            record_process = subprocess.Popen(record_cmd,shell=True)
        else:
            record_process = subprocess.Popen(record_cmd,shell=True)
            self.process = subprocess.Popen(self.perf_cmd(), shell=True)

    def perf_cmd(self):
        """
        Create perf_test executing command.

        Returns
        -----------
        perf_test_cmd : string
            Command to execute perf_test node.
        """
        command = 'ros2 run performance_test perf_test'
        pubs_args = ' -p 1 '

        fixed_args = ' --communication rclcpp-single-threaded-executor '

        topic_name = f'test_{topic}' #トピックの名前を逐次変更する(理由：Only topics with one type are supported)
        perf_test_qos_r = ""
        perf_test_qos_d = ""
        if perf_qos_r == "reliable":
            perf_test_qos_r = "--reliable"
        if perf_qos_d == "transient":
            perf_test_qos_d = "--transient"
        dyn_args = f" --msg {topic} --topic {topic_name} --rate {rate} -s 0 {perf_test_qos_r} {perf_test_qos_d}"

        perf_test_cmd = command + ' ' + fixed_args + dyn_args + pubs_args

        print('*********perf_test_command**********')
        print(perf_test_cmd)
        print('*********record_command**********')
        print(record_cmd)
        print('*******************')
        
        return perf_test_cmd

    def kill(self):
        """
        Kill the associated performance test process.
        """
        if self.process is not None:
            self.process.kill()

    def __del__(self):
        """
        Kill the associated performance test process.
        """
        self.kill()


def signal_handler(sig, frame):
    """
    Signal handler to handle Ctrl-C.
    """
    print('You pressed Ctrl+C! Terminating experiment')
    subprocess.Popen('killall -2 perf_test', shell=True)
    subprocess.Popen('killall -2 ros2 bag record', shell=True)
    sys.exit(0)

def evaluation_stop(sig=None, frame=None):
    """
    Stop rosbag2 evaluation.
    This method is called after experiment_length seconds.
    """
    publisher.kill()
    subprocess.Popen('killall -2 perf_test', shell=True)
    subprocess.Popen('killall -2 ros2', shell=True)
    print("perf_test,recorderをkill")
    exit(0)



# Execute perf_test and rosbag2 record for (num_of_publish/rate) + a few seconds.
experiment_length = (num_of_publish/int(rate)) + 5
interval = 3

# Kill node after experiment_length seconds.
signal.signal(signal.SIGALRM, evaluation_stop)
signal.signal(signal.SIGINT, signal_handler)
signal.setitimer(signal.ITIMER_REAL, experiment_length, interval) 

count = 1
publisher = Instance()
publisher.run()
print('Press Ctrl+C to abort experiment')

while True:
    time.sleep(1)
