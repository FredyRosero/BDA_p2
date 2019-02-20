#

import happybase

class HBConnection:
    tables={}
    batch_size=1000
    def __init__(self,host):
        self.connector = happybase.Connection(host)
        print ("Connecting to HBase")
        self.connector.open()
    def open(self):
        self.connector.open()
    def close(self):
        self.connector.close()  
    def table(self,tb_name):
        tb = self.connector.table(tb_name)
        batch = tb.batch(batch_size = self.batch_size)
        print ("Connect to HBase. table name: ", tb_name,", tb:", tb)
        return tb, batch
