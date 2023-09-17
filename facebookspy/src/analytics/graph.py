import networkx as nx
from ..repository import person_repository
import matplotlib.pyplot as plt


persons = person_repository.get_persons()


def create_relationship_graph():
    """
    Create a graph of connections between Person objects based on their Friends
    """
    G = nx.DiGraph()

    for person in persons:
        G.add_node(person.id, label=person.facebook_id)

    for person in persons:
        friend_urls = set(friend.url for friend in person.friends)
        for other_person in persons:
            if person != other_person:
                other_friend_urls = set(friend.url for friend in other_person.friends)
                common_urls = friend_urls.intersection(other_friend_urls)
                if common_urls:
                    for friend_url in common_urls:
                        G.add_edge(person.id, other_person.id, label=friend_url)

    pos = nx.spring_layout(G)
    labels = nx.get_node_attributes(G, "label")
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=1000)
    plt.show()

    return G
