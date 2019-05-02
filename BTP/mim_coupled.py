import networkx as nx
import random
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q
mx_m=9
m=5
mx_n=5
n=4
cnt=0
term_node=-1
theta=0.005
edges=dict()
scores=[]
Graphs=[]
status=[]
seed=set()
seeds=[]
fi=[]
nodes=[]
def reset():		#reset parameters for new iteration
	global seeds
	global fi
	global cnt
	global seed
	fi=[]
	seeds=[]
	seed=set()
	cnt=0
	for i in range(m):
		temp=set()
		seeds.append(temp)
		temp=dict()
		for u in nodes:
			temp[(1,u)]=1
		fi.append(temp)
def create_mul_graph(g):		#for multiple items
	global Graphs
	Graphs=[]
	for i in range(mx_m):
		temp=[]
		graph=nx.Graph()
		for u in nodes:
			for v in nodes:
				if u == v:
					continue
				if random.randint(1,1000) <850:
					continue
				graph.add_edge(u,v,weight=round(random.uniform(0,1),2))
		Graphs.append(graph)
		for u in nodes:
			temp.append(0)
			if u not in Graphs[i].nodes():
				Graphs[i].add_node(u)
	for i in range(mx_m):
		Graphs[i]=lossless_coupling()
def prepare():			#creating initial graph
	G=nx.Graph()
	x=open("facebook/0.edges","r")
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
	global nodes
	for edge in G.edges():
		u=edge[0]
		v=edge[1]
		if u not in nodes:
			nodes.append(u)
		if v not in nodes:
			nodes.append(v)
	nodes=sorted(nodes)
	return G
def lossless_coupling():		#coupling for multiple networks
	global nodes
	G=[]
	g=nx.DiGraph()
	wts=[]
	for i in range(mx_n):
		temp=nx.Graph()
		for u in nodes:
			for v in nodes:
				if u==v:
					continue
				if random.randint(1,1000) < 999:
					continue
				temp.add_edge(u,v,weight=round(random.uniform(0.2,1),2))
				g.add_edge(u,v,weight=0.0)
		G.append(temp)
	for i in range(mx_n):
		temp_nodes=G[i].nodes()
		for node in temp_nodes:
			if node not in nodes:
				nodes.append(node)
	nodes=sorted(nodes)
	for i in range(mx_n):
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
	for i in range(mx_n):
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
	return g

def infl_btw_nodes(G,u,v):			#calculates influence spread of a node to some specific node
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
def marg_gain(i,S,u):		#calculates marginal gain of a node 
#	cnt=len(S)
	if cnt > 0:
		for node in nodes:
			if node in S:
				continue
			fi[i][(cnt+1,node)]=fi[i][(cnt,node)]*(1-infl_btw_nodes(Graphs[i],term_node,node))
#	print(fi)
	gain=fi[i][(cnt+1,u)]
	for node in nodes:
		if node in S or node == u:
			continue
		gain+=infl_btw_nodes(Graphs[i],u,node)*fi[i][(cnt+1,node)]
	return gain
total=0
def seed_infl(infl):		#calculates total influence spread of seed set
#	infl=len(G.nodes())
	for v in nodes:
		if v in seed:
			continue
		temp=1
		for u in seed:
			for i in range(m):
				if u in seeds[i]:
					temp*=(1-infl_btw_nodes(Graphs[i],u,v));
		infl-=temp
	return infl

def fun(m,k):
	global cnt
	global term_node
	global nodes
	while 0 < k:
		PQ=Q.PriorityQueue()
		for i in range(m):
			max_gain_node=-1
			max_gain=0
			for u in nodes:
				if u in seed:		#if one seed node for only one item then seed else seeds[i]
					continue
				gain=marg_gain(i,seeds[i],u)
				if gain > max_gain:
					max_gain=gain
					max_gain_node=u
			PQ.put((-max_gain,max_gain_node,i))
		temp=PQ.get()
		seed.add(temp[1])
		seeds[temp[2]].add(temp[1])
		term_node=temp[1]
		cnt+=1
		k-=1
	print(seed)
	infl=seed_infl(len(nodes))
	print(infl)
	return infl
if __name__ == "__main__":
	global k
	global m
	g=prepare()
	create_mul_graph(g)			#network is now ready to use
	file=open("result.txt","w")
	for k in range(10,11):
		for m in range(5,6):
			reset()				
			print(m,k)
			file.write(str((fun(m,k),m,k)))
			file.write("\n")
