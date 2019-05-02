import networkx as nx
import random
import Queue as Q
m=5
theta=0.05
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
	if u > 150 or v > 150:
 		continue
	G.add_edge(u,v)
nodes=G.nodes()
k=len(nodes)/20
edges=dict()
scores=[]
Graphs=[]
status=[]
for i in range(m):
	scores.append([])
	graph=nx.Graph()
	for u in nodes:
		for v in nodes:
			if u == v:
				continue
			if random.randint(1,1000) <996:
				continue
			graph.add_edge(u,v,weight=round(random.uniform(0,1),2))
	Graphs.append(graph)
pq=[]
PQ=Q.PriorityQueue()
infl=[]
ttl_infl=[]
for i in range(m):
	t2=[]
	t3=[]
	for u in range(max(nodes)+1):
		t3.append(0)
		t1=[]
		for v in range(max(nodes)+1):
			t1.append(0)
		t2.append(t1)
	infl.append(t2)
	ttl_infl.append(t3)
seed=set()
seeds=[]
seed_infl=[]
for i in range(m):
	seed_infl.append(0)
	temp=set()
	seeds.append(temp)
	temp=Q.PriorityQueue()
	pq.append(temp)
	temp=[]
	for u in nodes:
		infl[i][u][u]=1
		temp.append(0)
		if u not in Graphs[i].nodes():
			Graphs[i].add_node(u)
for i in range(max(nodes)+1):
	status.append(0)
"""for i in range(m):
	break
	cur_edges=Graphs[i].edges()
	for u in nodes:
		score=0
		for v in nodes:
#			if random.randint(1,10) <9 or random.randint(1,10) <8:
#				continue
			if u == v:
				continue
			paths=nx.all_simple_paths(Graphs[i],source=u,target=v,cutoff=4)
			temp=[]
			for path in paths:
				temp1=1
				for x in range(1,len(path)):
					temp1*=Graphs[i][path[x-1]][path[x]]['weight']
				if temp1 >= theta:
					temp.append(temp1)
			temp2=1
			for val in temp:
				temp2*=(1-val)
			temp=1-temp2
			print(u,v,temp)
			infl[i][u][v]=temp
			infl[i][v][u]=temp
			score+=temp
		ttl_infl[i][u]=1+score
		pq[i].put((-1-score,u))
		if u > 20:
			break
	temp=pq[i].get()
	pq[i].put(temp)
	PQ.put((temp[0],i))
	"""
i=0
while i < k:
	p1=[]
	p2=Q.PriorityQueue()
	for j in range(max(nodes)+1):
		temp=Q.PriorityQueue()
		p1.append(temp)
	for j in range(m):
		for src in nodes:
			if src in seed:
				continue
			temp=seed.copy()
			temp.add(src)
			temp4=0
			for v in nodes:
				if v in seed:
					continue
				temp3=1
				for u in temp:
					paths=nx.all_simple_paths(Graphs[j],source=u,target=v,cutoff=4)
					temp2=1
					for path in paths:
						temp1=1
						for x in range(1,len(path)):
							temp1*=Graphs[j][path[x-1]][path[x]]['weight']
							if temp1 < theta:
								break
						if temp1 < theta:
							break
						temp2*=(1-temp1)
					temp2=1-temp2
					temp3*=(1-temp2)
				temp4+=temp3
			temp4=len(nodes)-temp4
#			print(seed,src,temp4)
			p1[j].put((-temp4,src))
		temp5=p1[j].get()
		p1[j].put(temp5)
		p2.put((temp5[0],temp5[1],j))
	newNode=p2.get()
	seed.add(newNode[1])
	print(seed,-newNode[0])
#	seeds[newNode[2]].add((newNode[1]))
	i+=1
