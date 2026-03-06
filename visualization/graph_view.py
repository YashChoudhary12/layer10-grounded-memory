import networkx as nx
from pyvis.network import Network
from sqlalchemy import text
from database.db import get_db


def build_graph():

    G = nx.DiGraph()

    with get_db() as db:

        result = db.execute(text("""
        SELECT
            e1.canonical_name AS subject,
            e1.entity_type AS subject_type,
            c.predicate,
            e2.canonical_name AS object,
            e2.entity_type AS object_type,
            ev.excerpt
        FROM claims c
        JOIN entities e1 ON c.subject_entity = e1.entity_id
        JOIN entities e2 ON c.object_entity = e2.entity_id
        JOIN evidence ev ON ev.claim_id = c.claim_id
        LIMIT 300
        """))

        rows = result.fetchall()

        for row in rows:

            subject = row.subject
            obj = row.object

            G.add_node(subject, type=row.subject_type)
            G.add_node(obj, type=row.object_type)

            G.add_edge(
                subject,
                obj,
                label=row.predicate,
                title=row.excerpt
            )

    return G


def visualize_graph():

    G = build_graph()

    net = Network(height="800px", width="100%", directed=True)

    color_map = {
        "person": "#4A90E2",
        "org": "#50E3C2",
        "unknown": "#AAAAAA"
    }

    for node, data in G.nodes(data=True):

        entity_type = data.get("type", "unknown")

        color = color_map.get(entity_type.lower(), "#AAAAAA")

        size = 10 + G.degree(node) * 2

        net.add_node(
            node,
            label=node,
            color=color,
            size=size
        )

    for source, target, data in G.edges(data=True):

        net.add_edge(
            source,
            target,
            label=data["label"],
            title=data["title"]
        )

    net.write_html("memory_graph.html")


if __name__ == "__main__":
    visualize_graph()