def dfs(start, target, path = [], visited = set()):
    path.append(start)
    visited.add(start)
    if start == target:
        return path
    for (neighbour, weight) in self.m_adj_list[start]:
        if neighbour not in visited:
            result = self.dfs(neighbour, target, path, visited)
            if result is not None:
                return result
    path.pop()
    return None

def main():
    graph = {
        'Red': ['Green-B', 'Green-C', 'Green-D', 'Green-E', 'Mattapan', 'Orange'],
        'Orange': ['Red', 'Blue', 'Green-D', 'Green-E'],
        'Mattapan': ['Red', 'Green-B', 'Green-C', 'Green-D', 'Green-E'],
        'Blue': ['Orange'],
        'Green-B': ['Red', 'Green-C', 'Green-D', 'Green-E', 'Blue'],
        'Green-C': ['Red', 'Green-B', 'Green-D', 'Green-E', 'Blue'],
        'Green-D': ['Red', 'Green-B', 'Green-C', 'Green-E', 'Blue', 'Orange'],
        'Green-E': ['Red', 'Green-B', 'Green-C', 'Green-D', 'Blue', 'Orange'],

    }

    visited = set()  # Set to keep track of visited nodes of graph.

    dfs(visited, graph, 'Red', 'Orange')


main()
