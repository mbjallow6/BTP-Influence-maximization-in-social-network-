import networkx as nx
import sys
import random
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q
k=10
m=5
global mx
alpha=0.2
theta=0.05
global nodes
nodes=[]
global score
score=[]
weights=dict()
flag=dict()
flags=[]
status=dict()
DN=[]
MIL=1
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
		if u > 200 or v > 200:# or u <2 or v<2:
			continue
		G.add_edge(u,v,weight=round(random.uniform(0.2,1),2))
	nodes=G.nodes()
	for node in nodes:
		status[node]=0
		flag[node]=0
		weights[node]=round(random.uniform(0.2,1),2)
	return G
def create_mul_graph(G):
	Graphs=[]
	for i in range(m):
		g=nx.Graph()
		for edge in G.edges():
#			if random.randint(1,10) >5 :
#				continue
			g.add_edge(edge[0],edge[1],weight=round(random.uniform(0.2,1),2))	
#		for u in G.nodes():
#			for v in G.nodes():
#				if u==v:
#					continue
#				if random.randint(1,1000) < 985:
#					continue
#				g.add_edge(u,v,weight=round(random.uniform(0.2,1),2))
		temp=dict()
		for u in nodes:
			if u not in g.nodes():
				g.add_node(u)
			temp[u]=1
		score.append(temp)
		Graphs.append(g)
		for node in g.nodes():
			flags[i][node]=0
			if g.degree(node)>DN[i]:
				DN[i]=g.degree(node)
	return Graphs
IL=[]
H_measure=[]
max_h_measure=[]
K_Shell_measure=[]
I_U_value=[]
que=Q.PriorityQueue()
ques=[]
seed=set()
seeds=[]
def reset():
	global IL
	global H_measure
	global max_h_measure
	global K_Shell_measure
	global I_U_value
	global seeds
	global flag
	for i in range(m):
		flags.append(dict())
		IL.append(dict())
		H_measure.append(dict())
		K_Shell_measure.append(dict())
		I_U_value.append(dict())
		temp1=set()
		seeds.append(temp1)
		DN.append(1)
		max_h_measure.append(0)
		temp2=Q.PriorityQueue()
		ques.append(temp2)
def reset_1():
	global current
	current=dict()
	for u in nodes:
		temp=list()
		current[u]=temp

def calculate_IL(G,i):		#local influence
	global IL
	global MIL
	for u in G.nodes:
		temp=1
		nbrs=G[u]
		for nbr in nbrs:
			temp+=G[u][nbr]['weight']
			for v in G[nbr]:
				if v==u:
					continue
				temp+=G[nbr][v]['weight']
		MIL=max(MIL,temp)
		IL[i][u]=temp
def calculate_H_measure(G,i):			
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
		H_measure[i][u]=temp
		if temp>max_h_measure[i]:
			max_h_measure[i]=temp
def calculate_K_Shell_measure(G,i):		#for coreness score
	global K_Shell_measure
	global DN
	ks=1
	for j in range(len(nodes)):
		temp=nx.k_shell(G,j+1).nodes()
#		if len(temp)==0:
#			break
		for node in temp:
			K_Shell_measure[i][node]=j+1
			ks=j+1
	for node in G.nodes():
		if node not in K_Shell_measure[i]:
			K_Shell_measure[i][node]=0
def calculate_Iu(G,i):			#calculating influenc capacity
	for node in nodes:
		CS=K_Shell_measure[i][node]*(1+G.degree(node)/float(DN[i]))
#		IU=G.degree(node)/float(DN)+H_measure[node]/float(max_h_measure)
		IU=IL[i][node]/float(MIL)+H_measure[i][node]/float(max_h_measure[i])
		IU*=CS
		I_U_value[i][node]=IU
		ques[i].put((-IU,node))
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
def seed_infl(Graphs,seed):
	cur=[]
	infl=0
	for i in range(m):
		cur.append(list(seeds[i]))
	j=0
	while(1):
		flag=0
		cur1=set()
		for i in range(m):
			for u in cur[i]:
				for v in nodes:
					if status[v]!=0 or 1-score[i][v]>0.5:
						continue
					temp=infl_btw_nodes(Graphs[0],u,v)
					score[i][v]*=(1-temp)
					if(1-score[i][v]>0.5):
						current[v].append(i)
						cur1.add(v)
				cur[i]=cur[i][1:]
		infl+=len(cur1)
		for u in cur1:				#choosing randomely from one of the items that influence a user at same time
			temp=random.choice(current[u])
			cur[temp].append(u)
			status[u]=temp+1
		for i in range(m):
			if len(cur[i])>0:
				flag=1
				break
		if flag==0:
			break
		j+=1
	return infl

if __name__=="__main__":
	k=10#int(sys.argv[1])
	m=4#int(sys.argv[2])
	G=create_graph()
	reset()
	Graphs=create_mul_graph(G)
	for i in range(m):
		calculate_IL(Graphs[i],i)
		calculate_H_measure(Graphs[i],i)
		calculate_K_Shell_measure(Graphs[i],i)
		calculate_Iu(Graphs[i],i)
#	print(I_U_value[0])
	que=Q.PriorityQueue()
	flag1=-1
	while k > 0:
		reset_1()
		flag1=-1
		if flag1==-1:			#only one graph will insert candidate for seed node in PQ because 
			for i in range(m):		#only one node from flag1'th graph became seed node in last step
				temp=(0,-1)
				while not ques[i].empty() and temp[1] == -1:
					temp1=ques[i].get()
					if flags[i][temp1[1]]==0:
						temp=temp1
						que.put((temp[0],temp[1],i))
		else:
			i=flag1
			temp=(0,-1)
			while not ques[i].empty() and temp[1] == -1:
				temp1=ques[i].get()
				if flags[i][temp1[1]]==0 and temp1[1] not in seed:			###
					temp=temp1
					que.put((temp[0],temp[1],i))
		if que.empty():
			break
		temp=que.get()
		while(temp[1] in seed and not que.empty()):
			temp=que.get()
		u=temp[1]
		i=temp[2]
		flag1=i
		seed.add(u)
		seeds[i].add(u)
		flags[i][u]=1
		status[u]=1
		flag[u]=1
		for v in G[u]:
			cn=calculate_CN(G,u,v)
			if cn > alpha:
				flags[i][v]=1
				status[v]=1
		k-=1
	print(seed)
	print((len(Graphs[0].nodes()),len(Graphs[0].edges())))
	print(seed_infl(Graphs,seeds))
	for i in range(m):
		print(seeds[i])
 