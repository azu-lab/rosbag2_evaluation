import subprocess
import os
import shutil
import time
import datetime
import signal
import statistics

import generate_cmd as gc
import get_bagfile_data as gbd  
import make_messageloss_latextable as mml  
import message_loss_distribution as mld 
import calc_record_jitter as crj 
import calc_play_jitter as cpj 

# Evaluation start time
start = datetime.datetime.now()

#-----Get lists and datas from generate_cmd.py-----
dt_str = gc.get_dt_str()
perf_test_topics = gc.get_perf_test_topics()
nd_mcs_spp_product = gc.get_nd_mcs_spp_product()
play_path_list = gc.get_play_path_list()
play_cmd_list = gc.get_play_cmd_list()
rate_d_r_dds_product = gc.get_rate_d_r_dds_product()

time_output_root_dir = gc.get_time_output_root_dir()
# time_output_root_dir = f"./time_output/{dt_str}"    
num_of_repeat = gc.get_num_of_repeat()

def exec_run_perf_test_and_rosbag2_record(nd_mcs_spp,topic,l_param):
    """
    Run run_perf_test_and_rosbag2_record.py, and launch perf_test and rosbag2 record.

    Parameters
    ----------
    nd_mcs_spp : int
        Index of nd_mcs_spp_product indicating the parameters to be executed.
    topic : int
        Index of perf_test_topics indicating the parameter to be executed.
    l_param : int
        Index of rate_d_r_dds_product indicating the parameters to be executed.
    """
    # Pass parameters to be executed and output results storage location to run_perf_test_and_rosbag2_record.py 
    # Manipulate output results with grep to output timestamps only
    experiment_cmd = f"python3 run_perf_test_and_rosbag2_record.py {nd_mcs_spp} {topic} {l_param} {time_output_dir} | grep qqq.*"
    with open(f'{time_output_dir}/pub_time_before_del.txt','w') as f:
        subprocess.run(experiment_cmd,shell=True,stdout=f,encoding='UTF-8', universal_newlines=True)

def create_perf_test_time_txt():
    """
    Remove specific strings for grep from pub_time_before_del.txt.
    """
    before_delete = []
    after_delete = []
    with open(f'{time_output_dir}/pub_time_before_del.txt','r') as f:
        before_delete = f.readlines()
        for k in range(len(before_delete)):
            after_delete.append(before_delete[k][3:-1]) # Remove specific strings (qqq).
    os.remove(f'{time_output_dir}/pub_time_before_del.txt') # Delete pub_time_before_del.txt because it has been used.
    with open(f'{time_output_dir}/perf_test_time.txt','w') as f:
        d = "\n".join(after_delete)
        f.write(d)
    print("@ perf_test_time.txt @")

def create_record_time_txt():
    """
    Get timestamps from bagfile and write them to record_time.txt.
    """
    dbpath = time_output_dir + "/bagfile/bagfile_0.db3"
    with open(f'{time_output_dir}/record_time.txt','w') as f:
        # Get timestamps from get_bagfile_data.py.
        timestamp = gbd.get_record_timestamp(dbpath)
        for i in timestamp:
            f.write("%s\n" %i)
    print("@ record_time.txt @")

def create_play_time_txt():
    """
    Launch rosbag2 play and create play_time.txt.
    Then, calculate jitter of rosbag2 play.
    """
    bagfile_path = time_output_dir + "/bagfile"
    for i in range(len(play_path_list)):
        play_cmd = f"ros2 bag play {play_cmd_list[i]} {bagfile_path}"
        play_output_dir = f"{time_output_dir}/{play_path_list[i]}"
        os.makedirs(play_output_dir, exist_ok=True)
        with open(f'{play_output_dir}/play_time.txt', 'w') as f:
            subprocess.run(play_cmd, shell=True,encoding='UTF-8', stdout=f,universal_newlines=True)
        time.sleep(1)
        # Pass the path where record_time.txt and play_time.txt are located, and caluculate jitter.
        cpj.calc_jitter(time_output_dir,play_output_dir)
    print("@ play_time.txt @")

def create_perf_test_time_for_jitter_txt():
    """
    Write the data in the same line as the id of the data stored in bagfile to perf_test_time_for_jitter.txt.
    """
    bagfile_path = time_output_dir + "/bagfile"
    dbpath = bagfile_path + "/bagfile_0.db3"
    with open(f'{time_output_dir}/perf_test_time_for_jitter.txt','w') as ffp:
        perf_time_after_row_delete = []
        perf_time_before_row_delete = []
        with open(f'{time_output_dir}/perf_test_time.txt','r') as fp:
            perf_time_before_row_delete = fp.readlines()
            id_list = gbd.get_record_id_list(dbpath) # Get an id list of recorded messages.
            number_of_message_loss = len(perf_time_before_row_delete)-len(id_list) # Calculate message loss.
            num_of_m_loss_list.append(number_of_message_loss)
            if number_of_message_loss >= 1:
                # Calculate the number of lost for each certain number and output to m_loss_dist_output_dir.
                mld.message_loss_dist(id_list,500,m_loss_dist_output_file,topic) 
            for i in range(len(id_list)):
                # Retrieve only the rows of the elements in the id_list from perf_test_time.txt.
                perf_time_after_row_delete.append(perf_time_before_row_delete[id_list[i]-1])
        for i in perf_time_after_row_delete:
            ffp.write("%s" %i)
    print("@ perf_test_time_for_jitter.txt @")
    shutil.rmtree(bagfile_path) # Delete bagfile because it has been used.
    print("@ delete the bagfile @")
    # time.sleep(2)

def output_message_loss_result(num_of_message_loss,output_path):
    """
    Write the number of message loss to /number_of_message_loss/(topic).txt.
    """
    output_text = f"{num_of_message_loss}"
    with open(f'{output_path}','a') as f:
        print(f"{output_text}",file=f)

def signal_handler(sig, frame):
    """
    Signal handler to handle Ctrl-C.
    """
    print('@@@@@ You pressed Ctrl+C. Terminating rosbag2 experiment @@@@@')
    subprocess.Popen('killall -9 perf_test', shell=True)
    subprocess.Popen('killall -2 ros2', shell=True)
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

#----------Conduct evaluation----------

num_of_m_loss_list = [] # Array to store message loss.

for h in range(len(nd_mcs_spp_product)): # nd,mcs,spp
    nd_mcs_spp_param = list(nd_mcs_spp_product[h])
    nd = nd_mcs_spp_param[0]
    mcs = nd_mcs_spp_param[1]
    spp = nd_mcs_spp_param[2]
    for i in range(len(perf_test_topics)): #topic
        topic = perf_test_topics[i]
        for j in range(len(rate_d_r_dds_product)): #rate,durability,reliability,dds
            l_param = list(rate_d_r_dds_product[j])
            rate = l_param[0]
            durability = l_param[1]
            reliability = l_param[2]
            dds = l_param[3]
            os.environ["RMW_IMPLEMENTATION"] = dds # Change RMW_IMPLEMENTATION.

            #----------Path setting to output data----------
            # Path to output timestamps data.
            time_output_dir = f"{time_output_root_dir}/nd={nd}_mcs={mcs}_spp={spp}/{topic}_rate={rate}/QoS={durability},{reliability}_DDS={dds}"
            os.makedirs(time_output_dir,exist_ok=True)
            # Paths to output message loss data.
            m_loss_output_dir = f'{time_output_root_dir}/nd={nd}_mcs={mcs}_spp={spp}/number_of_message_loss'
            m_loss_output_path = f"{m_loss_output_dir}/{topic}.txt"
            os.makedirs(m_loss_output_dir,exist_ok=True)
            m_loss_dist_output_dir = f"{m_loss_output_dir}/dist/{dds},{rate},{reliability},{durability}"
            os.makedirs(m_loss_dist_output_dir,exist_ok=True)
            m_loss_dist_output_file = f"{m_loss_dist_output_dir}/{topic}.txt"

            for k in range(num_of_repeat): # Repeat the same parameter (for message loss).
                #----------Execute evaluation methods----------
                print(f"-----Parameter execution ({k+1})-----\ncommunication:[{dds},{reliability},{durability}]\nperf_test:[{rate},{topic}]\nrosbag2 record:{nd_mcs_spp_param}")
                print("-----Execute perf_test,rosbag2 record-----")
                exec_run_perf_test_and_rosbag2_record(h,i,j)
                print("-----Create a file containing timestamps.-----")
                create_perf_test_time_txt()
                create_record_time_txt()
                create_play_time_txt() # Comment out if you only want to measure rosbag2 record.
                create_perf_test_time_for_jitter_txt()
                
            print("-----Calculate message loss and jitter-----")
            crj.calc_jitter(time_output_dir)
            # Take average of message loss (rounding) and output to m_loss_output_path.
            ave_of_m_loss = round(statistics.mean(num_of_m_loss_list))
            num_of_m_loss_list = []
            output_message_loss_result(ave_of_m_loss,m_loss_output_path)
    # Create a message loss table (latex).
    mml.make_latextable(nd_mcs_spp_param,m_loss_output_dir)
    print("Create message loss table")

# Output the time taken for evaluation.
end = datetime.datetime.now()
evaluation_time = end - start
print(f"Evaluation time is {evaluation_time}")