import sys
import happybase
import time
import nltk
import struct
import itertools
from lib.conn import HBConnection

start_time = time.time()
clear = True if '-c' in sys.argv else False
verbose = True if '-v' in sys.argv else False
sentences_table = "t0"
connection = None
dictionary = None
rela_sent = {}


class relation:
    index = 0
    holder = []
        
def qualify_word(word):    
    row = dictionary.row(word)
    qual = row.get(b'data:polarity')
    return  float(qual) if qual is not None else "None"    

def load_setences_rows(table,batch):
    #print(">Scanning: ",table)
    setences_rows = table.scan(limit=500, filter="FamilyFilter(!=,'binaryprefix:sentence')")      
    #print(">Scanning: ",setences_rows)
    # Calificar oraciones y obtener agentes
    compute_sentences(setences_rows,table,batch)  

def compute_sentences(setences_rows,table,batch):   
    sentences = {}
    rela_sent_i = 0     
    #Por cada fila (Oración),
    #print(">Computing: ",setences_rows)    
    for k,values in setences_rows:
        key = k.decode("utf-8")   
        sentences[key] = {}           
        # Inicializar variables para esta oración
        word_count = 0
        agent_count = 0
        polarity= 0.0
        sentence_agents = []                               
        # Por cada atributo de la fila,
        for column_key,column_value in values.items():
            c_key = column_key.decode("utf-8")
            # si es un atributo de palabra
            if c_key.startswith("words:"): 
                # obtiene calificacion del dicctionario
                qual = qualify_word(c_key[6:])
                # almacena la palabra y su calificacion
                sentences[key][c_key] = str(qual) #O
                # acumula polaridad para calular mas adelante
                polarity += qual if not qual == "None" else 0.0
                word_count += 1   
            # si es un atributo de agente
            elif c_key.startswith("agents:"): 
                # Agregar agente de oraciòn
                sentence_agents.append(c_key) #O
                agent_count += 1                             
        # Calcular la polaridad de la oración actual
        sente_pola = polarity/word_count if not word_count == 0 else "None"
        # Almacenar valor de polaridad en objeto a insertar
        sentences[key]["polarity:value"] = str(sente_pola)                        
        if verbose: print(str(key),sentences[key])   
        table.put(str(key),sentences[key])                                
        # Almacenar relaciones entre agentes de la oración actual
        if agent_count>1:              
            for par_rela in itertools.combinations(sentence_agents,2):
                if par_rela[0]>par_rela[1]:  
                    rela_sent[key] = [par_rela[0]+par_rela[1],par_rela[0],par_rela[1],sente_pola]    
                else:
                    rela_sent[key] = [par_rela[1]+par_rela[0],par_rela[1],par_rela[0],sente_pola] 
    # Cometer inserccion de datos
    batch.send()

def inListListed(tg,fl):
    for el in fl:
        if tg[0] == el[0]:
            if el[3]!='None' and tg[3]!='None':
                el[3] += tg[3]
                el[4] += 1
            return True
    return False

def merge_duplicates(relations):
    origin = []    
    for k,rel in relations.items():
        origin.append(rel+[1])

    final_list = [] 
    for el in origin: 
        isInList = inListListed(el,final_list)
        if not isInList: 
            final_list.append(el) 
    for el in final_list:
        el[1]=el[1][7:]
        el[2]=el[2][7:]
        if el[3]!='None': el[3] = el[3] / el[4]
        el.pop(0)
    return final_list 

def write_sentences_agents(tb, bt, rel):
    i=0
    for dt in rel:
        data = { 'agent:a':dt[0],'agent:b':dt[1],'agent:weight':str(dt[3]),'polarity:value':str(dt[2])}
        #print(">Inserting: ",str(i),data)   
        tb.put(str(i),data)    
        bt.send()
        i+=1
    return 0

#MAIN:
connection = HBConnection("localhost")
#
dictionary, dict_batch = connection.table("dictionary")
words_tb, words_batch = connection.table(sentences_table)
rela_tb, rela_batch = connection.table("relationships")
try:
    # Escanear la tabla de oraciones 
    load_setences_rows(words_tb,words_batch)  
    #for k,v in rela_sent.items(): print(k,v) 
    # Fusionar duplicados de la lista          
    rela_sent = merge_duplicates(rela_sent) 
    if verbose: 
        for el in rela_sent: print(el)

    write_sentences_agents(rela_tb, rela_batch, rela_sent )
    
finally:
    connection.close()

duration = time.time() - start_time
print ("Done. duration: ", duration ," s")


