import networkx as nx
import random
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q
mx_m=9
m=5
k=5
mx_n=5
n=5
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
def reset():
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
		for u in Graphs[i].nodes():
			temp[(1,u)]=1
		fi.append(temp)
def create_mul_graph(g):	
	global Graphs
	Graphs=[]
	for i in range(mx_m):
		temp=[]
		graph=nx.Graph()
		for u in nodes:
			for v in nodes:
				if u == v:
					continue
				if random.randint(1,1000) <990:
					continue
				graph.add_edge(u,v,weight=round(random.uniform(0,1),2))
		Graphs.append(graph)		
		for u in nodes:
			temp.append(0)
			if u not in Graphs[i].nodes():
				Graphs[i].add_node(u)
	for i in range(mx_m):
		Graphs[i]=weighted_coupling()
def prepare():			
	graph=nx.Graph()
	for u in range(80):
		for v in range(80):
			if u == v:
				continue
			if random.randint(1,1000) <990:
				continue
			graph.add_edge(u,v,weight=round(random.uniform(0,1),2))
	global nodes
	for edge in graph.edges():
		u=edge[0]
		v=edge[1]
		if u not in nodes:
			nodes.append(u)
		if v not in nodes:
			nodes.append(v)
	nodes=sorted(nodes)
	return graph
def weighted_coupling():
	k=5
	theta=[]
	sum=0
	for i in range(k):
		theta.append(round(random.uniform(0,1),3))
		sum+=theta[i]
	for i in range(k):
		theta[i]/=sum
	#	print(theta[i])
	G=[]
	g=nx.Graph()
	for i in range(n):
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
	wts=dict()
	for u in g.nodes():
		wts[u]=dict()
	for u in g.nodes():
		for v in g.nodes():
			if u==v:
				continue
			wts[u][v]=0
			wts[v][u]=0
	for i in range(k):
		temp=G[i]
		weight=0
		for edge in temp.edges():
			wts[edge[0]][edge[1]]+=theta[i]*G[i][edge[0]][edge[1]]['weight']
	#		print(edge,G[i][edge[0]][edge[1]]['weight'])
	for edge in g.edges():
		g[edge[0]][edge[1]]['weight']=wts[edge[0]][edge[1]]
	#	print(edge,g[edge[0]][edge[1]]['weight'])
	for u in nodes:
		if u not in g.nodes():
			g.add_node(u)
	return g
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
def marg_gain(i,S,u):
#	cnt=len(S)
	if cnt > 0:
		for node in Graphs[i].nodes():
			if node in S:
				continue
			fi[i][(cnt+1,node)]=fi[i][(cnt,node)]*(1-infl_btw_nodes(Graphs[i],term_node,node))
#	print(fi)
	gain=fi[i][(cnt+1,u)]
	for node in Graphs[i].nodes():
		if node in S or node == u:
			continue
		gain+=infl_btw_nodes(Graphs[i],u,node)*fi[i][(cnt+1,node)]
	return gain
total=0
def seed_infl(infl):
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
			for u in Graphs[i].nodes():
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
	create_mul_graph(g)
	reset()	
	file=open("result_weighted.txt","w")
	for k in range(4,8):
		for m in range(3,7):
			reset()	
			print(m,k)
			file.write(str((fun(m,k),m,k)))
			file.write("\n")