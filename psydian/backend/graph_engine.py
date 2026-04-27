import networkx as nx
from sqlalchemy.orm import Session
from models import Connection, FileModel

def build_graph(db: Session) -> nx.DiGraph :
    G = nx.DiGraph()
    
    files = db.query(FileModel).all()
    
    for f in files :
        G.add_node(f.id, title=f.title, path=f.path, tags=f.tags)
        
    connections = db.query(Connection).all()
    for c in connections :
        G.add_edge(c.source_id, c.target_id, id=c.id, label=c.label)
        
    return G
    