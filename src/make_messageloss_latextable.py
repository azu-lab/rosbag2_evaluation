import generate_cmd as gc
import os

topics = gc.get_perf_test_topics()
num_of_publish = gc.get_perf_test_num_of_publish()

rate_d_r_dds_ary = gc.get_rate_d_r_dds_ary()
rate_ary = rate_d_r_dds_ary[0]
durability_ary = rate_d_r_dds_ary[1]
reliability_ary = rate_d_r_dds_ary[2]
dds_ary = rate_d_r_dds_ary[3]


rate_d_r_dds_ary_length = len(rate_ary)*len(durability_ary)*len(reliability_ary)*len(dds_ary)

def tabular_def_cmd():
    cmd = "\\begin{tabular}{|l||"
    for i in range(rate_d_r_dds_ary_length):
        cmd += "c|"
    cmd += "}\\hline\n"
    return cmd

def rate_table():
    cmd = "\\multicolumn{1}{|c||}{rate} "
    for i in range(len(rate_ary)):
        cmd += f"& \\multicolumn{{{len(durability_ary)*len(reliability_ary)*len(dds_ary)}}}{{c|}}{{{rate_ary[i]}}} "
    cmd += "\\\\\\hline\n"
    return cmd

def durability_table():
    cmd = "\\multicolumn{1}{|c||}{Durability} "
    if len(durability_ary) == 1:
        cmd += f"& \\multicolumn{{{rate_d_r_dds_ary_length}}}{{c|}}{{{durability_ary[0]}}} "
    else:
        for i in range(len(rate_ary)):
            for j in range(len(durability_ary)):
                cmd += f"& \\multicolumn{{{len(reliability_ary)*len(dds_ary)}}}{{c|}}{{{durability_ary[j]}}} "
    cmd += "\\\\\\hline\n"
    return cmd

def reliability_table():
    cmd = "\\multicolumn{1}{|c||}{Reliability} "
    if len(reliability_ary) == 1:
        cmd += f"& \\multicolumn{{{rate_d_r_dds_ary_length}}}{{c|}}{{{reliability_ary[0]}}} "
    else:
        for i in range(len(rate_ary)*len(durability_ary)):
            for j in range(len(reliability_ary)):
                cmd += f"& \\multicolumn{{{len(dds_ary)}}}{{c|}}{{{reliability_ary[j]}}} "
    cmd = cmd.replace('_','\\_')
    cmd += "\\\\\\hline\n"
    return cmd

def dds_table():
    cmd = "\\multicolumn{1}{|c||}{DDS} "
    if len(dds_ary) == 1:
        cmd += f"& \\multicolumn{{{rate_d_r_dds_ary_length}}}{{c}}{{{dds_ary[0]}}}"
    else:
        for i in range(len(rate_ary)*len(durability_ary)*len(reliability_ary)):
            for j in range(len(dds_ary)):
                cmd += f"& {dds_ary[j]}"
    cmd = cmd.replace('rmw_cyclonedds_cpp','cyclone').replace('rmw_fastrtps_cpp','fast')
    cmd += "\\\\\\hline\\hline\n"
    return cmd

def make_latextable(nd_mcs_spp_param,m_path): #m_path=./time_output/number_of_lost_message/nd,mcs,spp
    nd = nd_mcs_spp_param[0]
    mcs = nd_mcs_spp_param[1]
    spp = nd_mcs_spp_param[2]
    header_code = header_table(nd,mcs,spp)
    body_code = body_table(nd,mcs,spp,m_path)
    end_code = "\\end{tabular}\n\\end{table*}\n\n"
    #./time_output/時刻/number_of_message_lossのトピックごとのファイルから値を代入
    with open(f'{m_path}/all_latex_table_code', 'a') as f:
        for i in header_code:
            f.write("%s" %i)
        for i in body_code:
            f.write("%s" %i)
        f.write(end_code)
        # print(i)


def header_table(nd,mcs,spp): #
    header_code = []
    #table
    begin_table = "\\begin{table*}\n\\centering\n"
    header_code.append(begin_table)
    #キャプション
    caption = "\\caption{The number of message loss."
    caption += f" No Discovery is \\textit{{{nd}}}, Max Cache Size is \\textit{{{mcs}}}, and Storage Preset Profile is \\textit{{{spp}}}"
    caption += "}\n"
    header_code.append(caption)
    #ラベル
    label = "\\label{Messageloss:"
    label += f"{nd},{mcs},{spp}"
    label += "}\n"
    header_code.append(label)
    #tabular
    header_code.append(tabular_def_cmd())
    #パラメータテーブル(上からdurability,reliablity,ddsの順番)
    # header_code.append(rate_table())
    header_code.append(durability_table())
    header_code.append(reliability_table())
    header_code.append(dds_table())

    return header_code

def body_table(nd,mcs,spp,m_path):#m_path=./time_output/number_of_lost_message/nd,mcs,spp
    body_code = [] 
    for i in range(len(topics)):
        topic_table = f"{topics[i]} "
        m_filename =  m_path + f"/{topics[i]}.txt"
        with open(f'{m_filename}','r') as f:
            loss_result = f.readlines()
            # while loss_result:
            for j in range(rate_d_r_dds_ary_length):
                if f"{num_of_publish}" in loss_result[j]: #全部ロストしていたら(ロスト数が、パブリッシュ回数と同じ)、そもそもレコードが上手くいってないのでfail
                    topic_table += f"& fail "
                else:
                    loss = loss_result[j].replace('\n','')
                    topic_table += f"& {loss} "
        topic_table += "\\\\\\hline\n"
        body_code.append(topic_table)
    return body_code
    #例:Array1k & 0 & 0 ... \\\hline
    #   Array4k & 0 & 0 ... \\\hline