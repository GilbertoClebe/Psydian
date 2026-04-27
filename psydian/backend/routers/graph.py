from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from graph_engine import build_graph

router = APIRouter(prefix="/graph", tags=["graph"])

@router.get("/")
def get_graph(db: Session = Depends(get_db)) :
    G = build_graph(db)
    
    nodes = []
    for node_id, data in G.nodes(data=True) :
        nodes.append({
            "data": {
                "id": str(node_id),
                "label": data.get("title", f"Node {node_id}"),
                "tags": data.get("tags", "")
            }
        })
    
    edges = []
    for source, target, data in G.edges(data=True) :
        if data.get("label") :
            mid_id = f"mid-{source}-{target}"
            nodes.append({
                "data": {
                    "id": mid_id,
                    "label": data.get("label", ''),
                    "type": "edge-node"
                }
            })
        
        edges.append({"data": {"source": str(source), "target": mid_id}})
        edges.append({"data": {"source": mid_id, "target": str(target)}})
        
        edges.append({
            "data": {
                "id": f"e{data.get('id', '')}",
                "source": str(source),
                "target": str(target),
                "label": data.get("label", ""),
            }
        })
        
    return {"nodes": nodes, "edges": edges}
    
    