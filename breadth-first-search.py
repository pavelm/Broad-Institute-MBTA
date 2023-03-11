

def bfs(queue, visited, graph, starting_location, end_location):  # function for BFS

    visited.append(starting_location)
    queue.append(starting_location)

    travel = []

    while queue:  # Creating loop to visit each node
        m = queue.pop(0)

        for neighbour in graph[m]:
            if neighbour not in visited:

                if end_location == neighbour:
                    travel.append([m, end_location])
                    return travel

                travel.append([m, neighbour])

                visited.append(neighbour)
                queue.append(neighbour)


    return travel

def main():

    graph = {
        '5': ['3', '7'],
        '3': ['2', '4', '5'],
        '7': ['5', '8'],
        '2': ['3'],
        '4': ['3', '8'],
        '8': ['4', '7']
    }

    visited = []  # List for visited nodes.
    queue = []

    print(bfs(queue, visited, graph, '5', '8'))


main()
