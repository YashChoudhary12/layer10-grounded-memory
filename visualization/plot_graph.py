import networkx as nx
import matplotlib.pyplot as plt
from sqlalchemy import text
from database.db import get_db


def visualize(limit=50):

    G = nx.DiGraph()

    with get_db() as db:

        result = db.execute(text("""
        SELECT
            e1.canonical_name,
            c.predicate,
            e2.canonical_name
        FROM claims c
        JOIN entities e1 ON c.subject_entity = e1.entity_id
        JOIN entities e2 ON c.object_entity = e2.entity_id
        LIMIT :limit
        """), {"limit": limit})

        for s, p, o in result:
            G.add_edge(s, o, label=p)

    pos = nx.spring_layout(G)

    nx.draw(G, pos, with_labels=True, node_size=2000)
    plt.show()


if __name__ == "__main__":
    visualize()