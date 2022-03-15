import sqlite3

#bagfileのtimestampを取得
def get_record_timestamp(dbpath):
    #SQL命令文（messagesテーブル内のtimestampレコードを取得）
    db = sqlite3.connect(dbpath ,isolation_level=None)
    sql = "SELECT timestamp FROM messages"
    c = db.cursor()
    c.execute(sql)
    time =[]
    for row in c:
        time.append(row)
    return time

#bagfileのdata.idを取得(perf_test専用)
def get_record_id_list(dbpath):
    #SQL命令文（messagesテーブル内のdataレコードの後ろから8個の16進数の数を取得）
    db = sqlite3.connect(dbpath ,isolation_level=None)
    sql = "SELECT hex(substr(data,-8,8)) FROM messages"
    c = db.cursor()
    c.execute(sql)
    id_list = []
    for row in c:
        str_rev_id = str(row[0]) #tupleなので、16進数のデータだけ取り出す
        str_id = ""
        for j in range(8):
            str_id += str_rev_id[14-2*j:16-2*j] #bagfileに２個ずつ逆順でidの値が保存されているので、元に戻す(UDPはビッグエンディアンだから？)
        int_id = int(str_id,16) #16進数を整数に変換
        id_list.append(int_id)
    return id_list