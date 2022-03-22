import generate_cmd as gc

num_of_publish = gc.get_perf_test_num_of_publish()

def message_loss_dist(id_list,dist,output_file,topic):
    """
    Find the number of message loss per dist.

    Parameters
    ----------
    id_list : list
        list of id in data.
    dist : int
        Threshold for determining the distribution of message loss.
    output_file : string
        File name where information of message loss distribution is output.
    topic : string
        Topic parameter.
    """
    with open(f"{output_file}",'a') as f:
        if id_list == []:
            print(f"{topic}:Lost all {num_of_publish}",file=f)
        else:
            # Divide by dist and round up.
            id_devided_by_num_of_pub = list(map(lambda x: -(-x//dist), id_list)) 
            message_loss_count = []
            # Count the number of i+1 values in id_devided_by_num_of_pub by dividing the number of times published by dist.
            # And add it to the list pulled from dist.
            for i in range(int(num_of_publish/dist)): 
                message_loss_count.append(dist - id_devided_by_num_of_pub.count(i+1))
            print(f"{topic}:The number of message loss per {dist} in {num_of_publish} is {message_loss_count}.",file=f)
