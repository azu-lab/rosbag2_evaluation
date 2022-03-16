import generate_cmd as gc

num_of_pub = gc.get_perf_test_num_of_publish()
time_output_dir = ""
play_time = "perf_test_time_for_jitter.txt"
record_time = "record_time.txt"


def calc_jitter(time_output_dir,play_file_dir):

	with open(f'{play_file_dir}/play_time.txt',mode='r',encoding='UTF-8') as f:
		str_list_p = f.readlines()
	with open(f'{time_output_dir}/record_time.txt',mode='r',encoding='UTF-8') as f:
		str_list_r = f.readlines()

	#行数(データ数)を確認し、異なっているなら、エラー文を出力しexit
	num_of_p = len(str_list_p)
	num_of_r = len(str_list_r)
	# latency_ary = []
	threshold = 0.7
	if num_of_r <= num_of_pub*threshold: #
		print(f"record_time.txtのデータ数が{int(num_of_pub*threshold)}個以下なので、ジッタ・レイテンシの計算は行わない。")
		# latency_ary.append("0")
		latency_ary = ["0"]
		with open(f'{play_file_dir}/latency_ms.txt','w') as fl, open(f'{play_file_dir}/jitter_ms.txt','w') as fj:
			for i in latency_ary:
				fl.write("%s\n" %i)
				fj.write("%s\n" %i)				
	else:
		#レイテンシの計算(play - record)
		latency_ary = calc_latency(str_list_p,str_list_r,play_file_dir)
		#ジッタの計算
		jitter_ary = []
		for i in range(len(latency_ary)-1):
			jitter_ary.append(round(latency_ary[i+1]-latency_ary[i],6))
		with open(f'{play_file_dir}/jitter_ms.txt','w') as f:
			for i in jitter_ary:
				f.write("%s\n" %i)
	

def calc_latency(ary_p,ary_r,play_file_dir):
	int_ary_p = []
	int_ary_r = []
	for i in range(len(ary_p)):
		int_ary_p.append(int(ary_p[i]))
	for i in range(len(ary_r)):
		int_ary_r.append(int(ary_r[i]))
	
	latency_ns = []
	for i in range(len(ary_p)):
		latency_ns.append(int_ary_p[i] - int_ary_r[i])

	#データを1000000で割ってミリ秒にする
	latency_ms = list(map(lambda x: x/1000000, latency_ns))

	with open(f'{play_file_dir}/latency_ms.txt','w') as f:
		for i in latency_ms:
			f.write("%s\n" %i)
	return latency_ms

