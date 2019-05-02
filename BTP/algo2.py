import networkx as nx
import random
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q
m=6
k=10
asf=0.9
mx_m=10
cnt=0
term_node=-1
theta=0.005
nodes=[]
term_node=-1
Graphs=[]
def reset():
	global seeds
	global actvd
	global actvds
	global fi
	global cnt
	global seed
	global status
	global score
	global current
	global infld
	fi=[]
	infld=[]
	actvd=set()
	seeds=[]
	actvds=[]
	seed=set()
	status=dict()
	score=[]
	cnt=0
	for node in nodes:
		status[node]=0
	for i in range(m):
		infld.append(0)
		temp=set()
		temp1=dict()
		actvds.append(temp)
		seeds.append(temp)
		temp=dict()
		for u in Graphs[i].nodes():
			temp1[u]=1
			temp[(1,u)]=1
		fi.append(temp)
		score.append(temp1)
def reset_1():
	global current
	current=dict()
	for u in nodes:
		temp=list()
		current[u]=temp

def prepare():			
	graph=nx.Graph()
	for u in range(150):
		for v in range(150):
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
				graph.add_edge(u,v,weight=round(random.uniform(0.5,1),2))
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
#	cnt=len(S)
	if cnt > 0:
		for node in Graphs[i].nodes():
			if node in S or node in actvd:
				continue
			fi[i][(cnt+1,node)]=fi[i][(cnt,node)]*(1-infl_btw_nodes(Graphs[i],term_node,node))
#	print(fi)
	gain=fi[i][(cnt+1,u)]
	for node in Graphs[i].nodes():
		if node in S or node == u or node in actvd:
			continue
		gain+=infl_btw_nodes(Graphs[i],u,node)*fi[i][(cnt+1,node)]
	return gain
def post_add(i,u):
	temp=0
#	print(fi[0])
	for node in nodes:
		if node in seed or node in actvd:
			continue
		temp1=1-(1-infl_btw_nodes(Graphs[i],u,node))*(fi[i][(cnt+1,node)])
#		for v in seed:
#			temp1*=1-(1-infl_btw_nodes(Graphs[i],v,node))*(fi[i][(cnt+1,node)])			
		temp1=1-temp1
		if temp1>asf:
			temp+=1
			actvd.add(node)
			actvds[i].add(node)
	print(i,cnt+1,len(actvd))
def marg_gain1(i,S,u):
	gain=0
	que=list(S)
	que.append(u)
	temp=score[:]
	temp1=set()
	while len(que)>0:
		u=que[0]
		que=que[1:]
		for v in Graphs[i][u]:
			if status[v]!=0 or v in temp1:
				continue
			temp[i][v]+=Graphs[i][u][v]['weight']
			if temp[i][v]>0.5:
				que.append(v)
				temp1.add(v)
	return (len(temp1)-len(actvd),temp,temp1)
def seed_infl():
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
if __name__ == "__main__":
	global term_node
	g=prepare()
	create_mul_graph(g)
	reset()
	print(len(Graphs[0].edges()),len(nodes))
#	print(infl_btw_nodes(Graphs[0],nodes[0],nodes[1]))
	global cnt
	while 0 < k:
		reset_1()
		my_queue=Q.PriorityQueue()
		t_current=set()
		for i in range(m):
			gain=0
			t_score=score
			t_actvd=actvd
			t_node=-1
			for u in nodes:
				if u in actvd or u in seed:
					continue
				temp=marg_gain(i,seed,u)
				if gain < temp:
					gain=temp
					t_node=u
			my_queue.put((-gain,i,t_node))
		temp=my_queue.get()
		if temp[2] !=-1:
			post_add(temp[1],temp[2])
			seed.add(temp[2])
			seeds[temp[1]].add(temp[2])
		term_node=temp[2]
		cnt=cnt+1
		k-=1
	print(seed)
	print(seed_infl())
