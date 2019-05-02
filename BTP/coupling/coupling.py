import networkx as nx
import random
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q
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
				if random.randint(1,100) < 99:
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
if __name__ == "__main__":
	g=weighted_coupling()
	print(g.edges())