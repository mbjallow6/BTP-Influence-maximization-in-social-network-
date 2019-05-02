import networkx as nx
import random
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q
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
if __name__ == "__main__":
	g=lossless_coupling()
	mx=g[1]
	g=g[0]
	print(g[1])