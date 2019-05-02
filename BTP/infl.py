import networkx as nx
import random
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
	G.add_edge(u,v)
status=dict()
nodes=G.nodes()
k=len(nodes)/100
edges=G.edges()
wts=dict()
req=dict()
for node in nodes:
	status[node]=0
	nbrs=G[node]
	req[node]=random.randint(20,100)/100
	for nbr in nbrs:
		wts[(nbr,node)]=1/len(nbrs)
activated=set()
score=set()
for i in range(0,k):
	newnode=(-1,-1)
	status1=status
	for node in nodes:
		if node in activated:
			continue
		temp=list()
		actvtd=list()
		nbrs=G[node]
		for nbr in nbrs:
			if nbr in activated:
				continue
			status[nbr]+=wts[(node,nbr)]
			if status[nbr]>=req[nbr]:
				temp.append(nbr)
				actvtd.append(nbr)
		depth=1
		for nod in temp:
			if depth > 3:
				break
			depth+=1
			nbrs=G[nod]
			for nbr in nbrs:
				if nbr in activated:
					continue
				status[nbr]+=wts[(nod,nbr)]
				if status[nbr]>=req[nbr]:
					temp.append(nbr)
					actvtd.append(nbr)
		if newnode[0] == -1 or newnode[1] < len(actvtd):
			newnode=(node,len(actvtd))
	activated.add(newnode[0])
	score.add(newnode)
print(score)