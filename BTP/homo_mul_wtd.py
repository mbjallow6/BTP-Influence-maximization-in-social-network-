import networkx as nx
import random
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q
m=1
cnt=0
term_node=-1
theta=0.005
seed=set()
seeds=[]
fi=dict()
k=5
def lossless_coupling():
	k=5
	G=[]
	g=nx.DiGraph()
	wts=[]
	for i in range(k):
		temp=nx.Graph()
		for u in range(1,100):
			for v in range(1,100):
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
	return (g,mx)
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
	for i in range(k):
		temp=nx.Graph()
		for u in range(1,100):
			for v in range(1,100):
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
	print(len(g.edges()))
	for edge in g.edges():
		g[edge[0]][edge[1]]['weight']=wts[edge[0]][edge[1]]
	#	print(edge,g[edge[0]][edge[1]]['weight'])
	return g
#	return (g,mx,weights)

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
total=0
if __name__ == "__main__":
	temp=weighted_coupling()
	g=temp
	nodes=g.nodes()
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