import sys
import networkx as nx
import random
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q
k=10
m=4
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
		if u > 400 or v > 400:
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
def lossless_coupling(G1):
	k=m
	G=[]
	g=nx.DiGraph()
	wts=[]
	for i in range(k):
		temp=nx.Graph()
		for edge in G1.edges():
			if random.randint(1,10) >5 :
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
	nodes=[]
	for i in range(k):
		temp_nodes=G[i].nodes()
		for node in temp_nodes:
			if node not in nodes:
				nodes.append(node)
	nodes=sorted(nodes)
	for i in range(k):
		temp=dict()
		temp_nodes=G[i].nodes()
		for node in temp_nodes:
			temp[node]=round(random.uniform(0.2,1),2)
		wts.append(temp)
	mx=nodes[-1]
	weights=dict()
	for node in nodes:
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
	for node in g.nodes():
		u=node
		break
	return (g,mx,weights)
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
	for i in range(len(nodes)):
		temp=nx.k_shell(G,i+1).nodes()
#		if len(temp)==0:
#			break
		for node in temp:
			K_Shell_measure[node]=i+1
			ks=i+1
	for node in G.nodes():
		if node not in K_Shell_measure:
			K_Shell_measure[node]=0
def calculate_Iu(G):			#calculating influenc capacity
	for node in G.nodes():
		if node > mx:
			continue
		CS=K_Shell_measure[node]*(1+G.degree(node)/float(DN))
#		IU=G.degree(node)/float(DN)+H_measure[node]/float(max_h_measure)
		IU=IL[node]/float(MIL)+H_measure[node]/float(max_h_measure)
		IU*=CS
		I_U_value[node]=IU
		que.put((-IU,node))
def calculate_CN(G,u,v):			#common neighbour cofficient
	temp1=G[u]
	temp2=G[v]
	i=0
	s=set()
	for u in temp1:
		s.add(u)
	for u in temp2:
		if u in s:
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
	infl=len(nodes)
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
	m=int(sys.argv[2])
	G=create_graph()
	G=lossless_coupling(G)
	mx=G[1]
	G=G[0]
	nodes=[]
	for node in G.nodes():
		if node <= mx:
			nodes.append(node)
	calculate_IL(G)
	calculate_H_measure(G)
	calculate_K_Shell_measure(G)
	calculate_Iu(G)
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
	print(seed_infl(G,seed))