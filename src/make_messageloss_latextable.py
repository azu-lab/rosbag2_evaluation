import generate_cmd as gc

topics = gc.get_perf_test_topics()
num_of_publish = gc.get_perf_test_num_of_publish()

rate_d_r_dds_ary = gc.get_rate_d_r_dds_ary()
rate_ary = rate_d_r_dds_ary[0]
durability_ary = rate_d_r_dds_ary[1]
reliability_ary = rate_d_r_dds_ary[2]
dds_ary = rate_d_r_dds_ary[3]

rate_d_r_dds_ary_length = len(rate_ary)*len(durability_ary)*len(reliability_ary)*len(dds_ary)

def make_latextable(nd_mcs_spp_param,m_path): #m_path=.'{time_output_root_dir}/nd={nd}_mcs={mcs}_spp={spp}/number_of_message_loss'
    """
    Make latex table. 
    Caption consists of No Discvoery, Max Cache Size, and Storage Preset Profile.
    Horizontal axis consists of Rate, Durability, Reliability, and DDS.
    Vertical axis consists of Topics.

    Parameters
    ----------
    nd_mcs_spp_param : list
        Parameter list consisting of No Discvoery, Max Cache Size, and Storage Preset Profile.
    m_path : string
        Path name where message loss latex table exists.
    """
    nd = nd_mcs_spp_param[0]
    mcs = nd_mcs_spp_param[1]
    spp = nd_mcs_spp_param[2]

    header_code = header_table(nd,mcs,spp)
    body_code = body_table(m_path)
    end_code = "\\end{tabular}\n\\end{table*}\n\n"

    # Output latex table code to all_latex_table_code.txt.
    with open(f'{m_path}/all_latex_table_code.txt', 'a') as f:
        for i in header_code:
            f.write("%s" %i)
        for i in body_code:
            f.write("%s" %i)
        f.write(end_code)


def header_table(nd,mcs,spp):
    """
    Make header code of latex table (begin table, caption, label, and tabular).

    Parameters
    ----------
    nd : string
        No Discovery parameter.
    mcs : string
        Mac Cache Size parameter.
    spp : string
        Storage Preset Profile parameter.
    
    Retruns
    ----------
    header_code : list
        list of latex table header code.
    """
    header_code = []
    # Table
    begin_table = "\\begin{table*}\n\\centering\n"
    header_code.append(begin_table)
    # Caption
    caption = "\\caption{The number of message loss."
    caption += f" No Discovery is \\textit{{{nd}}}, Max Cache Size is \\textit{{{mcs}}}, and Storage Preset Profile is \\textit{{{spp}}}"
    caption += "}\n"
    header_code.append(caption)
    # Label
    label = "\\label{Messageloss:"
    label += f"{nd},{mcs},{spp}"
    label += "}\n"
    header_code.append(label)
    # Tabular
    header_code.append(tabular_def_cmd())
    # Parameter table (order of durability, reliablity, and dds from top to bottom).
    # header_code.append(rate_table())
    header_code.append(durability_table())
    header_code.append(reliability_table())
    header_code.append(dds_table())

    return header_code

def tabular_def_cmd():
    """
    Increase elements on the horizontal axis by the number of rate_d_r_dds_ary_length.

    Returns
    ----------
    cmd : string
        Command of begin tabular.
    """
    cmd = "\\begin{tabular}{|l||"
    for i in range(rate_d_r_dds_ary_length):
        cmd += "c|"
    cmd += "}\\hline\n"
    return cmd

#-----Below four functions makes multicolumn-----
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



def body_table(m_path):#m_path=./time_output/number_of_lost_message/nd,mcs,spp
    """
    Make body code of latex table (each topics).

    Parameters
    ----------
    m_path : string
        Path name where message loss latex table exists.

    Retruns
    ----------
    body_code : list
        list of latex table body code.
    """
    body_code = [] 
    for i in range(len(topics)):
        topic_table = f"{topics[i]} "
        m_filename =  m_path + f"/{topics[i]}.txt"
        with open(f'{m_filename}','r') as f:
            loss_result = f.readlines()
            for j in range(rate_d_r_dds_ary_length):
                #If all the records are lost (the number of lost records is the same as the number of publish), the record is not working, so fail.
                if f"{num_of_publish}" in loss_result[j]: 
                    topic_table += f"& fail "
                else:
                    loss = loss_result[j].replace('\n','')
                    topic_table += f"& {loss} "
        topic_table += "\\\\\\hline\n"
        body_code.append(topic_table)
    return body_code
    #For example:Array1k & 0 & 0 ... \\\hline
    #            Array4k & 0 & 0 ... \\\hline