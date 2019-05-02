import networkx as nx
import random
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q
m=6
cnt=0
term_node=-1
theta=0.005
path="content/drive/My Drive/BTP/0.edges"
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
	G.add_edge(u,v)
nodes=G.nodes()
k=len(nodes)/15
edges=dict()
scores=[]
Graphs=[]
status=[]
seed=set()
seeds=[]
fi=[]
def reset():
	global seeds
	global fi
	global seed
	fi=[]
	seeds=[]
	seed=set()
	for i in range(m):
		temp=set()
		seeds.append(temp)
		temp=dict()
		for u in nodes:
			temp[(1,u)]=1
		fi.append(temp)

def prepare():	
	global Graphs
	for i in range(10):
		temp=[]
		graph=nx.Graph()
		for u in nodes:
			for v in nodes:
				if u == v:
					continue
				if random.randint(1,1000) <985:
					continue
				graph.add_edge(u,v,weight=round(random.uniform(0,1),2))
		Graphs.append(graph)
		for u in nodes:
			temp.append(0)
			if u not in Graphs[i].nodes():
				Graphs[i].add_node(u)
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
	cnt=len(S)
	if len(S) > 0:
		for node in nodes:
			if node in S:
				continue
			fi[i][(cnt+1,node)]=fi[i][(cnt,node)]*(1-infl_btw_nodes(Graphs[i],term_node,node))
	gain=fi[i][(cnt+1,u)]
	for node in nodes:
		if node in S or node == u:
			continue
		gain+=infl_btw_nodes(Graphs[i],u,node)*fi[i][(cnt+1,node)]
	return gain
total=0
def seed_infl():
	infl=len(G.nodes())
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
	while 0 < k:
		PQ=Q.PriorityQueue()
		for i in range(m):
			max_gain_node=-1
			max_gain=0
			for u in nodes:
				if u in seeds[i]:
					continue
				gain=marg_gain(i,seeds[i],u)
				if gain > max_gain:
					max_gain=gain
					max_gain_node=u
			PQ.put((-max_gain,max_gain_node,i))
		temp=PQ.get()
		seed.add(temp[1])
		seeds[temp[2]].add(temp[1])
		global term_node
		term_node=temp[1]
#		print(temp)
		cnt+=1
		k-=1
	print(seed)
#	for i in range(m):
#		print(i,seeds[i])
	infl=seed_infl()
	print(infl)
	return(infl)
if __name__ == "__main__":
	global k
	prepare()
	file=open("result1.txt","w")
	for k in range(10,11):
		for m in range(4,5):
			reset()
	#		fun(m,k)
			file.write(str((fun(m,k),m,k)))
			file.write("\n")
