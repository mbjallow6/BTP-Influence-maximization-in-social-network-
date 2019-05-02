import networkx as nx
import sys
import random
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q
k=10
m=5
n=4
global mx
alpha=0.2
theta=0.05
global nodes
nodes=[]
weights=dict()
flag=dict()
flags=[]
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
		if u > 300 or v > 300:
			continue
		G.add_edge(u,v,weight=round(random.uniform(0.2,1),2))
	nodes=G.nodes()
	for node in nodes:
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
		for u in nodes:
			if u not in g.nodes():
				g.add_node(u)
		Graphs.append(g)
		for node in g.nodes():
			flags[i][node]=0
			if g.degree(node)>DN[i]:
				DN[i]=g.degree(node)
	for i in range(len(Graphs)):
		Graphs[i]=lossless_coupling(Graphs[i])
	return Graphs
def lossless_coupling(G1):
	k=n
	G=[]
	g=nx.DiGraph()
	wts=[]
	for i in range(k):
		temp=nx.Graph()
		for edge in G1.edges():
			if random.randint(1,10) >3 :
				continue
			temp.add_edge(edge[0],edge[1],weight=round(random.uniform(0.2,1),2))
			g.add_edge(edge[0],edge[1],weight=round(random.uniform(0.2,1),2))
#		for u in G1.nodes():
#			for v in G1.nodes():
#				if u==v:
#					continue
#				if random.randint(1,1000) < 998:
#					continue
#				temp.add_edge(u,v,weight=round(random.uniform(0.2,1),2))
#				g.add_edge(u,v,weight=0.0)
		G.append(temp)
	t_nodes=[]
	for i in range(k):
		temp_nodes=G[i].nodes()
		for node in temp_nodes:
			if node not in t_nodes:
				t_nodes.append(node)
	t_nodes=sorted(t_nodes)
	for i in range(k):
		temp=dict()
		temp_nodes=G[i].nodes()
		for node in temp_nodes:
			temp[node]=round(random.uniform(0.2,1),2)
		wts.append(temp)
	mx=t_nodes[-1]
	weights=dict()
	for node in t_nodes:
		g.add_node(node)
		weights[node]=1
	for i in range(k):
		edges=G[i].edges()
		temp_nodes=G[i].nodes()
		for edge in edges:
			u=mx*(i+1)+edge[0]
			v=mx*(i+1)+edge[1]
			if u not in g.nodes():
				g.add_node(u)
				weights[u]=round(random.uniform(0.2,1),2)
				g.add_edge(u,edge[0],weight=1)
				g.add_edge(edge[0],u,weight=wts[i][edge[0]])
			if v not in g.nodes():
				g.add_node(v)
				weights[v]=round(random.uniform(0.2,1),2)
				g.add_edge(v,edge[1],weight=1)
				g.add_edge(edge[1],v,weight=wts[i][edge[1]])
			g.add_edge(edge[0],v,weight=G[i][edge[0]][edge[1]]['weight'])
		for node in nodes:
			if node not in temp_nodes:
				g.add_node(mx*(i+1)+node)
				weights[mx*(i+1)+node]=1
	for node in nodes:
		if node not in g.nodes():
			g.add_node(node)
	return g
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
def seed_infl(G,seeds):
	infl=len(nodes)
	for v in nodes:
		if v in seed:
			continue
		temp=1
		for i in range(m):
			for u in seeds[i]:
				temp*=(1-infl_btw_nodes(G[i],u,v));
		infl-=temp
	return infl
#def fun(Graphs):

if __name__=="__main__":
	k=int(sys.argv[1])
	m=int(sys.argv[2])
	m=int(sys.argv[2])
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
				if flags[i][temp1[1]]==0:
					temp=temp1
					que.put((temp[0],temp[1],i))
		if que.empty():
			break
#		print(que.queue)
		temp=que.get()
		u=temp[1]
		i=temp[2]
		flag1=i
		seed.add(u)
		seeds[i].add(u)
		flags[i][u]=1
		flag[u]=1
		for v in G[u]:
			cn=calculate_CN(G,u,v)
			if cn > alpha:
				flags[i][v]=1
		k-=1
	print(seed)
	print((len(Graphs[0].nodes()),len(Graphs[0].edges())))
	print(seed_infl(Graphs,seeds))
	for i in range(m):
		print(seeds[i])
