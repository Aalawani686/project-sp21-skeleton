import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob


def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    c, k = 0, 0
    s = 0
    e = len(G.nodes) - 1
    if (len(G.nodes) > 50):
        k = 100
        c = 5
    elif (len(G.nodes) > 30):
        k = 50
        c = 3
    else:
        k = 15
        c = 1

    remove_nodes = []
    remove_weighted_edges = []
    remove_edges = []

    # print(nx.shortest_path_length(G, source=s, target=e))

    for i in range(k):
        p = nx.shortest_path(G, source=s, target=e)
        edges = []
        weights = []
        for i in range(len(p) - 1):
            edge = [p[i], p[i+1]]
            weight = G[p[i]][p[i+1]]["weight"]
            # if (weight > min_weight):
            #     min_weight = weight
            #     min_edge = edge
            edges.append(edge)
            weights.append(weight)
        min_edge = -1
        min_weight = -1
        while len(edges) > 0:
            pos = weights.index(min(weights))
            min_edge = edges[pos]
            min_weight = weights[pos]
            G.remove_edge(min_edge[0], min_edge[1])
            if (not nx.has_path(G, s, e)):
                G.add_edge(min_edge[0], min_edge[1], weight = min_weight)
                edges.pop(pos)
                weights.pop(pos)
                min_edge = -1
                min_weight = -1
            else:
                break
        if (min_edge != -1):
            remove_edges.append(min_edge)
            temp = min_edge.copy()
            temp.append(min_weight)
            remove_weighted_edges.append(temp)

    # print(nx.shortest_path_length(G, source=s, target=e))
    G.add_weighted_edges_from(remove_weighted_edges)

    return [], remove_edges


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     c, k = solve(G)
#     assert is_valid_solution(G, c, k)
#     print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
#     write_output_file(G, c, k, 'outputs/small-1.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
if __name__ == '__main__':
    inputs = glob.glob('inputs/small/*')
    inputs.extend(glob.glob('inputs/medium/*'))
    inputs.extend(glob.glob('inputs/large/*'))
    # inputs = []
    # inputs.append("inputs/large/large-3.in")
    for input_path in inputs:
        output_path = 'outputs/' + input_path.split("/")[1] + "/" + basename(normpath(input_path))[:-3] + '.out'
        G = read_input_file(input_path)
        c, k = solve(G)
        print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
        assert is_valid_solution(G, c, k)
        distance = calculate_score(G, c, k)
        write_output_file(G, c, k, output_path)
