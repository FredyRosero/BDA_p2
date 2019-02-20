import sys
import happybase
import time

batch_size = 1000
host = "localhost"
file_path = "src/dictionary.txt"
row_count = 0
start_time = time.time()
table_name = "dictionary"

def connect_to_hbase():
    """ Connect to HBase server.
    This will use the host, namespace, table name, and batch size as defined in
    the global variables above.
    """
    conn = happybase.Connection(host = host)
    conn.open()
    table = conn.table(table_name)
    batch = table.batch(batch_size = batch_size)
    return conn, batch


def insert_row(batch, row):
    """ Insert a row into HBase.
    Write the row to the batch. When the batch size is reached, rows will be
    sent to the database.
    Rows have the following schema:
        [ id, keyword, subcategory, type, township, city, zip, council_district,
          opened, closed, status, origin, location ]
    """
    row = row.rstrip()
    line = row.split("\t");
    word = line[0].split("#");    
    #print(word[0],line[1])
    batch.put(word[0], {"data:polarity":line[1]})


# After everything has been defined, run the script.
conn, batch = connect_to_hbase()
print ("Connect to HBase. table name: ", table_name,", batch size:", batch_size)
f = open(file_path, "r")
print ("Connected to file. name: ", file_path)

try:
    # Loop through the rows. The first row contains column headers, so skip that
    # row. Insert all remaining rows into the database.
    for row in f:
        row_count += 1
        if row_count == 1:
            pass
        else:
            insert_row(batch, row)

    # If there are any leftover rows in the batch, send them now.
    batch.send()
finally:
    # No matter what happens, close the file handle.
    conn.close()

duration = time.time() - start_time
print ("Done. row count: ", row_count ,", duration: ", duration ," s")
