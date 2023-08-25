import networkx as nx
from .repository import person_repository
import matplotlib.pyplot as plt


persons = person_repository.get_persons()


def create_relationship_graph():
    graph = nx.DiGraph()

    for person in persons:
        graph.add_node(person.id, label=person.full_name)

        for friend in person.friends:
            graph.add_edge(person.id, friend.person_id)

    pos = nx.spring_layout(graph)
    labels = nx.get_node_attributes(graph, "label")
    nx.draw(graph, pos, labels=labels, with_labels=True, node_size=1000)
    plt.show()

    return graph
