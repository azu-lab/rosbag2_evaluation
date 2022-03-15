import matplotlib.pyplot as plt
import generate_cmd as gc
num_of_pub = gc.get_perf_test_num_of_publish()
time_output_dir = ""
prefile = "perf_test_time_for_jitter.txt"
nextfile = "record_time.txt"

def qSort(a):
    if len(a) in (0, 1):
        return a

    p = a[-1]
    l = [x for x in a[:-1] if x <= p]
    r = [x for x in a[:-1] if x >  p]

    return qSort(l) + [p] + qSort(r)


def calc_jitter(prefile,nextfile,time_output_dir):

	with open(f'{time_output_dir}/{prefile}',mode='r',encoding='UTF-8') as f:
		str_list_p = f.readlines()
	with open(f'{time_output_dir}/{nextfile}',mode='r',encoding='UTF-8') as f:
		str_list_n = f.readlines()

	#行数(データ数)を確認し、異なっているなら、エラー文を出力しexit
	num_of_p = len(str_list_p)
	num_of_n = len(str_list_n)
	# latency_ary = []
	if num_of_n <= num_of_pub*0.7 and ( prefile == "record_time.txt" or nextfile == "record_time.txt" ): #
		print(f"record_time.txtのデータ数が{int(num_of_pub*0.7)}個以下なので、ジッタ・レイテンシの計算は行わない。")
		# latency_ary.append("0")
		latency_ary = ["0"]
		with open(f'{time_output_dir}/latency_ms.txt','w') as fl, open(f'{time_output_dir}/jitter_ms.txt','w') as fj:
			for i in latency_ary:
				fl.write("%s\n" %i)
				fj.write("%s\n" %i)				
	elif num_of_p != num_of_n:
		print(f"{prefile}と{nextfile}のデータ数が異なるため、ジッタの計算が行えません")
		latency_ary = ["0"]
		with open(f'{time_output_dir}/latency_ms.txt','w') as fl, open(f'{time_output_dir}/jitter_ms.txt','w') as fj:
			for i in latency_ary:
				fl.write("%s\n" %i)
				fj.write("%s\n" %i)
	else:
		#レイテンシの計算
		latency_ary = calc_latency(str_list_p,str_list_n,time_output_dir)
		#ジッタの計算
		jitter_ary = []
		for i in range(len(latency_ary)-1):
			jitter_ary.append(round(latency_ary[i+1]-latency_ary[i],6))
		with open(f'{time_output_dir}/jitter_ms.txt','w') as f:
			for i in jitter_ary:
				f.write("%s\n" %i)

	

def calc_latency(ary_p,ary_n,time_output_dir):
	int_ary_p = []
	int_ary_n = []
	for i in range(len(ary_p)):
		int_ary_p.append(int(ary_p[i]))
	for i in range(len(ary_n)):
		int_ary_n.append(int(ary_n[i]))
	
	latency_ns = []
	for i in range(len(ary_p)):
		latency_ns.append(int_ary_n[i] - int_ary_p[i])

	#データを1000000で割ってミリ秒にする
	latency_ms = list(map(lambda x: x/1000000, latency_ns))

	with open(f'{time_output_dir}/latency_ms.txt','w') as f:
		for i in latency_ms:
			f.write("%s\n" %i)
	return latency_ms

