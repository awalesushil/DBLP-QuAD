from dblp import Graph

g = Graph("DBLP")
g.load_from_ntriple("/srv/data/dblp/dblp-2022-08-01.nt")
g.save("dblp.pkl")
