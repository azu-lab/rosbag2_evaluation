import itertools
import yaml
import datetime

# Current time.
dt_now = datetime.datetime.now()
dt_str = dt_now.strftime('%m%d_%H:%M:%S')

#パラメータが設定してあるyamlを読み込む
with open('rosbag2_evaluation_parameters.yaml', 'r') as yaml_file:
    eval_cfg_yaml = yaml.load(yaml_file, Loader=yaml.FullLoader)
    eval_cfg = (eval_cfg_yaml['rosbag2_evaluation']
                                ['ros__parameters'])

#-----ddsのパラメータを変数に格納-----
dds_of_eval = eval_cfg['dds']
#１回のパラメータの繰り返し回数を取得
num_of_repeat = eval_cfg['repeat']
#-----perf_testのパラメータを変数に格納-----
perf_test_params = eval_cfg['perf_test_parameters']
#perf_testのコマンド
perf_test_topics = perf_test_params['topics']
perf_test_rate = perf_test_params['rate']
perf_test_num_subs = ['0'] #評価には関係ないので基本的に０
perf_test_reliability = perf_test_params['reliability']
perf_test_durability = perf_test_params['durability']
perf_test_num_of_publish = perf_test_params['number_of_publish']

#perf_testコマンドの直積を取る
perf_test_product = list(itertools.product(perf_test_topics, 
    perf_test_rate,perf_test_num_subs, perf_test_reliability, perf_test_durability))


#-----rosbag2のパラメータ-----
rosbag2_params = eval_cfg['rosbag2_parameters']

#-----recordのパラメータを変数に格納-----
record_params = rosbag2_params['record']
#recordのオプション
record_qos_params = record_params['qos']
record_qos_reliability = record_qos_params['reliability']
record_qos_durability = record_qos_params['durability']
no_discovery = record_params['no_discovery']
max_cache_size = record_params['max_cache_size']
storage_preset_profile = record_params['storage_preset_profile']

#rosbag2 recordコマンドの直積を取る
# record_product = list(itertools.product(record_qos_reliability, 
#     record_qos_durability,no_discovery, max_cache_size, storage_preset_profile))


#-----playのパラメータを変数に格納-----
play_params = rosbag2_params['play']
#playのオプション
play_qos_params = play_params['qos']
play_qos_reliability = play_qos_params['reliability']
play_qos_durability = play_qos_params['durability']
read_ahead_queue_size = play_params['read_ahead_queue_size']
play_rate = play_params['rate']

#rosbag2 playコマンドの直積を取る
play_product = list(itertools.product(play_qos_reliability, 
    play_qos_durability, read_ahead_queue_size, play_rate))

#rosbag2 playのコマンド、パス(rate=int/queue_size=int)
play_path_list = []
play_cmd_list = []
for i in range(len(play_product)):
    play_cfg_path = ""
    play_cfg_cmd = ""
    c = list(play_product[i])
    #パスを作成
    play_cfg_path = f"raqs={c[2]}:rate={c[3]}"
    play_path_list.append(play_cfg_path)
    #コマンドを作成
    if c[3] != "default":
        play_cfg_cmd = f" --rate {c[3]}"
    if c[2] != "default":
        play_cfg_cmd += f" --read-ahead-queue-size {c[2]}"
    play_cmd_list.append(play_cfg_cmd)

#-----Make product lists for latex table-----
# label parameter 
nd_mcs_spp_product = list(itertools.product(no_discovery, max_cache_size, storage_preset_profile)) 
# table parameter
rate_d_r_dds_product = list(itertools.product(perf_test_rate,record_qos_durability,record_qos_reliability,dds_of_eval))
rate_d_r_dds_ary = []
rate_d_r_dds_ary.append(perf_test_rate)
rate_d_r_dds_ary.append(record_qos_durability)
rate_d_r_dds_ary.append(record_qos_reliability)
rate_d_r_dds_ary.append(dds_of_eval)




def get_dt_str():
    return dt_str

def get_num_of_repeat():
    return num_of_repeat

#-----perf_testに関する変数-----

# def get_perf_test_product():
#     return perf_test_product

def get_perf_test_topics():
    return perf_test_topics

def get_perf_test_num_of_publish():
    return perf_test_num_of_publish

#-----rosbag2 recordに関する変数-----

# def get_record_product():
#     return record_product

def get_nd_mcs_spp_product():
    return nd_mcs_spp_product

#-----rosbag2 playに関する変数-----

def get_play_path_list():
    return play_path_list

def get_play_cmd_list():
    return play_cmd_list

#latexに出力用のパラメータの直積
def get_rate_d_r_dds_product():
    return rate_d_r_dds_product

def get_rate_d_r_dds_ary():
    return rate_d_r_dds_ary