import sys
import networkx as nx
import random
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q
k=11
alpha=0.2
theta=0.05
nodes=[]
weights=dict()
flag=dict()
DN=1
MIL=0
path="content/drive/My Drive/BTP/0.edges"
def create_graph():
	global nodes
	global DN
	G=nx.Graph()
	x=open("facebook/facebook_combined.txt","r")
	file=x.read()
	edges=file.split("\n")
	for edge in edges:
		temp=edge.split(" ")
		if len(temp) < 2:
			continue
		u=int(temp[0])
		v=int(temp[1])
		if u > 100 or v > 100:
			continue
		G.add_edge(u,v,weight=round(random.uniform(0.2,1),2))
	nodes=G.nodes()
	for node in nodes:
		weights[node]=round(random.uniform(0.2,1),2)
		flag[node]=0
	for node in nodes:
		if G.degree(node)>DN:
			DN=G.degree(node)
	return G
IL=dict()
H_measure=dict()
max_h_measure=0
K_Shell_measure=dict()
I_U_value=dict()
que=Q.PriorityQueue()
seed=set()
def calculate_IL(G):		#local influence
	global IL
	global MIL
	for u in nodes:
		temp=1
		nbrs=G[u]
		for nbr in nbrs:
			temp+=G[u][nbr]['weight']
			for v in G[nbr]:
				if v==u:
					continue
				temp+=G[nbr][v]['weight']
		MIL=max(MIL,temp)
		IL[u]=temp
def calculate_H_measure(G):			
	global H_measure
	global max_h_measure
	for u in nodes:
		temp=0
		nbrs=G[u]
		temp1=[]
		for v in nbrs:
			temp1.append(G[v])
		temp1=sorted(temp1)
		while(1):
			cur=0
			for scr in temp1:
				if scr > temp:
					cur+=1
				if cur>=temp:
					break
			if cur>=temp:
				temp+=1
			else:
				break
		H_measure[u]=temp
		if temp>max_h_measure:
			max_h_measure=temp
def calculate_K_Shell_measure(G):		#for coreness score
	global K_Shell_measure
	global DN
	ks=1
	while True:
		temp=nx.k_shell(G,ks).nodes()
		if len(temp)==0:
			break
		for node in temp:
			K_Shell_measure[node]=ks
		ks+=1
	for node in G.nodes():
		if node not in K_Shell_measure:
			K_Shell_measure[node]=0
def calculate_Iu(G):			#calculating influenc capacity
	for node in G.nodes():
		CS=K_Shell_measure[node]*(1+G.degree(node)/float(DN))
#		IU=G.degree(node)/float(DN)+H_measure[node]/float(max_h_measure)
		IU=IL[node]/float(MIL)+H_measure[node]/float(max_h_measure)
		IU*=CS
		I_U_value[node]=IU
		que.put((-IU,node))
def calculate_CN(G,u,v):			#common neighbour cofficient
	temp1=G[u]
	temp2=G[v]
	cmn_nbrs=nx.common_neighbors(G,u,v)
	i=0
	for item in cmn_nbrs:
		i+=1
	temp3=set()
	for node in temp1:
		temp3.add(node)
	for node in temp2:
		temp3.add(node)
	return i/float(len(temp3))
def infl_btw_nodes(G,u,v):
	paths=nx.all_simple_paths(G,u,v,4)
	temp1=1
	for path in paths:
		temp=1
		for i in range(1,len(path)):
			temp*=G[path[i-1]][path[i]]['weight']
			if temp < theta:
				break
		if temp < theta:
			continue
		temp1*=(1-temp)
	return 1-temp1
def seed_infl(G,seed):
	infl=len(G.nodes())
	for v in nodes:
		if v in seed:
			continue
		temp=1
		for u in seed:
			temp*=(1-infl_btw_nodes(G,u,v));
		infl-=temp
	return infl
if __name__=="__main__":
	k=int(sys.argv[1])
	file=open("im.txt","a+")
	file.write("seed nodes: ")
	file.write(str(k))
	file.write("	")
	G=create_graph()
	calculate_IL(G)
	calculate_H_measure(G)
	calculate_K_Shell_measure(G)
	calculate_Iu(G)
	print((len(G.nodes()),len(G.edges())))
	while k > 0:
		temp=(0,-1)
		while not que.empty() and temp[1] == -1:
			temp1=que.get()
			if flag[temp1[1]]==0:
				temp=temp1
		if que.empty():
			break
		u=temp[1]
		seed.add(u)
		flag[u]=1
		for v in G[u]:
			cn=calculate_CN(G,u,v)
			if cn > alpha:
				flag[v]=1
		k-=1
	print(seed)
	infl=seed_infl(G,seed)
	print(infl)
	file.write("produced influence: ")
	file.write(str(infl))
	file.write("\n")