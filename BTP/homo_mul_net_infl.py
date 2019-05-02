import networkx as nx
import random
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q
m=5
cnt=0
term_node=-1
theta=0.005
seed=set()
seeds=[]
fi=dict()
k=10
def create_graph():
	global nodes
	global DN
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
	nodes=G.nodes()
	return G

def lossless_coupling(G1):
	k=m
	G=[]
	g=nx.DiGraph()
	wts=[]
	for i in range(k):
		temp=nx.Graph()
		for u in G1.nodes():
			for v in G1.nodes():
				if u==v:
					continue
				if random.randint(1,1000) < 999:
					continue
				temp.add_edge(u,v,weight=round(random.uniform(0.2,1),2))
				g.add_edge(u,v,weight=0.0)
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

def infl_btw_nodes(g,u,v):
	paths=nx.all_simple_paths(g,u,v,4)
	temp1=1
	for path in paths:
		temp=1
		for i in range(1,len(path)):
			temp*=g[path[i-1]][path[i]]['weight']
			if temp < theta:
				break
		if temp < theta:
			continue
		temp1*=(1-temp)
	return 1-temp1
def marg_gain(g,S,u):
	cnt=len(S)
	if len(S) > 0:
		for node in nodes:
			if node in S:
				continue
			fi[(cnt+1,node)]=fi[(cnt,node)]*(1-infl_btw_nodes(g,term_node,node))
	gain=fi[(cnt+1,u)]
	for node in nodes:
		if node in S or node == u:
			continue
		gain+=infl_btw_nodes(g,u,node)*fi[(cnt+1,node)]
	return gain
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
total=0
if __name__ == "__main__":
	g=create_graph()
	temp=lossless_coupling(g)
	g=temp[0]
	mx=temp[1]
	nodes=[]
	for node in g.nodes():
		if node < mx:
			nodes.append(node)
	for u in nodes:
		fi[(1,u)]=1
	while 0 < k:
		PQ=Q.PriorityQueue()
		max_gain_node=-1
		max_gain=0
		for u in nodes:
			if u in seed:
				continue
			gain=marg_gain(g,seed,u)
			if gain > max_gain:
				max_gain=gain
				max_gain_node=u
		PQ.put((-max_gain,max_gain_node))
		temp=PQ.get()
		seed.add(temp[1])
		term_node=temp[1]
		print(temp)
		cnt+=1
		k-=1
	print(seed)
	print(seed_infl(g,seed))