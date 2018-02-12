import os.path
file_output_path='deckard_clonepairs.txt'
file_deckard_path='/lv_scratch/scratch/mondego/local/farima/new_oreo/toolsEval/deckard/Deckard-parallel1.3/clusters/cluster_vdb_50_3_g15_1.732051_30_100000'
# file_deckard_path='D:\\PhD\\Clone\\deckard_clusters.txt'
file_output=open(file_output_path,'w')

def parseline(line):
    linesplitted=line.split(' ')
    path=linesplitted[16].split('/')
    path_to_write=path[11]+','+path[12]
    startline=linesplitted[17].split(':')[1]
    endline=int(startline)+int(linesplitted[17].split(':')[2])-1
    return (path_to_write+','+startline+','+str(endline))


def getclonepairs(cluster):
    print(len(cluster))
    for i in range(0,len(cluster)):
        line_source=parseline(cluster[i])
        for j in range(i+1,len(cluster)):
            file_output.write(line_source+','+parseline(cluster[j])+'\n')

with open(file_deckard_path,'r') as file_deckard:
    future_cluster_num=0
    current_cluster_num=0
    cluster_list=[]
    linenum=0
    for line in file_deckard:
        linenum+=1
        if linenum>9:
            if (line  in ['\n', '\r\n']):
                print('one cluster found')
                future_cluster_num+=1
                continue
            if (future_cluster_num>current_cluster_num):
                if (len(cluster_list)>0): getclonepairs(cluster_list)
                cluster_list = []
                current_cluster_num=future_cluster_num
            cluster_list.append(line)
    getclonepairs(cluster_list)

file_output.close()