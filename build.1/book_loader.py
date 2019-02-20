import sys
import happybase
import time
import nltk

verbose = True if '-v' in sys.argv else False
row_count = 0
batch_size = 1000
start_time = time.time()
table_name = "t0"
file_path = sys.argv[1]
tags_comp = ['NN',  #Noun, singular or mass
             'NNS', #Noun, plural
             'JJ',  #Adjective
             'JJR', #Adjective, comparative
             'JJS', #Adjective, superlative
             'RB',  #Adverb
             'RBR', #Adverb, comparative
             'RBS', #Adverb, superlative
            ]
tags_pn =   ['NNP', #Proper noun, singular
             'NNPS' #Proper noun, plural
            ]

def connect_to_hbase(tb):
    conn = happybase.Connection(host = "localhost")
    conn.open()
    
    ts = conn.tables()
    if (bytes(tb, 'utf-8') in ts):
        conn.delete_table( tb, True )
        
    conn.create_table( tb, {'sentence': dict(), 
                            'words': dict(max_versions=1), 
                            'agents': dict(max_versions=1), 
                            'polarity': dict(max_versions=1),
                            'hierarchy': dict(max_versions=1)})    
    table = conn.table(tb)
    batch = table.batch(batch_size = batch_size)
    return conn, batch

def insert_row(s, batch, data, tile):
    row_key = str(s)
    data_text = { "sentence:text":data[0] }
    data_words = {'words:'+el:'0' for el in data[1]}
    data_agents = {'agents:'+el:'0' for el in data[2]}
    data_hierarchy = { 'hierarchy:book':file_path ,'hierarchy:tile': str(tile)}
    data_dict = {**data_text, **data_words, **data_agents, **data_hierarchy}
    #print(row_key, data[0] )
    batch.put( row_key, data_dict)

print ("Conectando a HBase y creando la tabla: ", table_name)
conn, batch = connect_to_hbase(table_name)
print ("Conactadoa HBase. Tabla: ", table_name,", batch size:", batch_size)
try:
    with open(file_path, "r") as file:
        text = file.read()
        print ("Conectado a archivo. Nombre: ", file_path)
        print ("Texto tokenizado en párrafos")
        for p,paragraph in enumerate(text.split("\n\n")):
            if verbose: print("Tokenizando párrado #",p,":\n", paragraph[:20]+"...")
            sent_text = nltk.sent_tokenize(paragraph) 
            for s,sentence in enumerate(sent_text):   
                if verbose: print("Analizando oración #",s,":\n",sentence)                   
                tokens = nltk.word_tokenize(sentence) 
                tagged = nltk.pos_tag(tokens)
                agents = [s[0] for s in tagged if s[1] in tags_pn]          
                tagged = [s[0] for s in tagged if s[1] in tags_comp]
                insert_row(s, batch, [ sentence, tagged, agents ], p)
                row_count += 1
         
        batch.send()    
finally:
    # No matter what happens, close the file handle.
    conn.close()

duration = time.time() - start_time
print ("Done. Row count, ", row_count , ", duration: ", duration ," s")


