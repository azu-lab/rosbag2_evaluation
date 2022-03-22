import sqlite3

def get_record_timestamp(dbpath):
    """
    Get the timestamps of bagfile.

    Parameters
    ----------
    dbpath : string
        Path name of the directory where the bagfile exists.

    Retruns
    ----------
    time : list
        Timestamp datas of timestamp record. 
    """
    # Get timestamp record in the messages table.
    db = sqlite3.connect(dbpath ,isolation_level=None)
    sql = "SELECT timestamp FROM messages"
    c = db.cursor()
    c.execute(sql)
    time = []
    for row in c:
        time.append(row)
    return time

def get_record_id_list(dbpath):
    """
    Get bagfile data.id (for perf_test only).

    Parameters
    ----------
    dbpath : string
        Path name of the directory where the bagfile exists.

    Retruns
    ----------
    id_list : list
        Ids in data record. 
    """
    #Get the number of 8 hexadecimal digits from the back of the data record in the message table
    db = sqlite3.connect(dbpath ,isolation_level=None)
    sql = "SELECT hex(substr(data,-8,8)) FROM messages"
    c = db.cursor()
    c.execute(sql)
    id_list = []
    for row in c:
        str_rev_id = str(row[0]) # row is a tuple, so only the hexadecimal data is extracted.
        str_id = ""
        for j in range(8):
            # Since the id values are stored in bagfile in reverse order by two, restore the id (because UDP is big-endian?).
            str_id += str_rev_id[14-2*j:16-2*j]
        int_id = int(str_id,16) # Convert hexadecimal numbers to integers.
        id_list.append(int_id)
    return id_list