from collections import defaultdict
from graphviz import Digraph
from .repository import person_repository


persons = person_repository.get_persons()
node_connections = defaultdict(list)


def create_relationship_graph():
    for person in persons:
        for friend in person.friends:
            node_connections[person.id].append(friend.person_id)
            node_connections[friend.person_id].append(person.id)

        if person.family_member:
            node_connections[person.id].append(person.family_member.person_id)
            node_connections[person.family_member.person_id].append(person.id)

    graph = Digraph(format="png")

    for person in persons:
        graph.node(str(person.id), person.full_name)

        for connection in node_connections[person.id]:
            graph.edge(str(person.id), str(connection))

    graph.render("person_graph", view=True)
