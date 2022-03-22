import generate_cmd as gc

num_of_pub = gc.get_perf_test_num_of_publish()
threshold_rate = gc.get_threshold_rate()

def calc_jitter(time_output_dir,play_file_dir):
	"""
	Calculate the jitter of rosbag2 play.

	Parameters
	----------
	time_output_dir : string
		Path name of the directory where record_time.txt is stored.
	play_file_dir : string
		Path name of the directory where you plan to store jitter_ms.txt
	"""
	with open(f'{play_file_dir}/play_time.txt',mode='r',encoding='UTF-8') as f:
		str_list_p = f.readlines()
	with open(f'{time_output_dir}/record_time.txt',mode='r',encoding='UTF-8') as f:
		str_list_r = f.readlines()

	# Check the number of data in record_time.txt and if it is below the threshold, do not calculate latency and jitter.
	threshold = int(num_of_pub*threshold_rate)
	if len(str_list_r) <= threshold: 
		print(f"Since the number of data in record_time.txt is less than {threshold}, jitter and latency are not calculated.")
		# Write 0 to latency_ms.txt and jitter_ms.txt.
		latency_ary = ["0"]
		with open(f'{play_file_dir}/latency_ms.txt','w') as fl, open(f'{play_file_dir}/jitter_ms.txt','w') as fj:
			for i in latency_ary:
				fl.write("%s\n" %i)
				fj.write("%s\n" %i)				
	else:
		# Calculate latency (play - record).
		latency_ary = calc_latency(str_list_p,str_list_r,play_file_dir)
		# Calculate jitter.
		jitter_ary = []
		for i in range(len(latency_ary)-1):
			# Round to the sixth decimal place.
			jitter_ary.append(round(latency_ary[i+1]-latency_ary[i],6))
		with open(f'{play_file_dir}/jitter_ms.txt','w') as f:
			for i in jitter_ary:
				f.write("%s\n" %i)
	

def calc_latency(ary_p,ary_r,play_file_dir):
	"""
	Calculate the latency of rosbag2 play.

	Parameters
	----------
	ary_p : string
		Timestamp datas in play_time.txt.
	ary_r : string
		Timestamp datas in record_time.txt.
	play_file_dir : string
		Path name of the directory where you plan to store latency_ms.txt.

	Returns
	----------
	latency_ms : list of float
		Latency from record_time.txt to play_time.txt (float).
	"""
	int_ary_p = []
	int_ary_r = []
	# Convert data from string to integer type.
	for i in range(len(ary_p)):
		int_ary_p.append(int(ary_p[i]))
	for i in range(len(ary_r)):
		int_ary_r.append(int(ary_r[i]))
	
	# Calculate latency.
	latency_ns = []
	for i in range(len(ary_p)):
		latency_ns.append(int_ary_p[i] - int_ary_r[i])

	# Divide latency by 1,000,000 to get milliseconds.
	latency_ms = list(map(lambda x: x/1000000, latency_ns))

	with open(f'{play_file_dir}/latency_ms.txt','w') as f:
		for i in latency_ms:
			f.write("%s\n" %i)

	return latency_ms

