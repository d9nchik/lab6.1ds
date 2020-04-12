from copy import deepcopy


def get_data():
    data = []
    with open("input.txt") as iFile:
        while True:
            line = iFile.readline()
            if not line:
                break
            temp = (line[:len(line)] + line[len(line) + 1:]).split()
            for x in range(len(temp)):
                temp[x] = int(temp[x])
            data.append(temp)
    return data


def create_adjacency_matrix(idata):
    matrix = [0] * idata[0][0]
    for x in range(idata[0][0]):
        matrix[x] = [0] * idata[0][0]

    for y in range(1, len(idata)):
        matrix[idata[y][0] - 1][idata[y][1] - 1] = 1
        matrix[idata[y][1] - 1][idata[y][0] - 1] = 1
    return matrix


def is_euler_loop(matrix_of_power):
    for x in matrix_of_power:
        if x % 2 == 1:
            return False
    return True


def is_euler_path(matrix_of_power):
    counter = 0
    for x in matrix_of_power:
        if x % 2 == 1:
            counter += 1
    return counter == 2


def create_power_of_heights(adjacency_matrix):
    matrix_of_power = []
    for i in range(len(adjacency_matrix)):
        total = 0
        for j in range(len(adjacency_matrix)):
            total += adjacency_matrix[i][j]
        matrix_of_power.append(total)
    return matrix_of_power


def find_start_point(matrix_of_power):
    for x in range(len(matrix_of_power)):
        if matrix_of_power[x] > 0:
            return [x]
    return []


def find_euler_path(array, matrix_of_power, adjacency_matrix):
    while len(array) != 0:
        if matrix_of_power[array[-1]] == 0:
            print(array[-1] + 1, end="->")
            del array[-1]
        else:
            number = -1
            for x in range(len(adjacency_matrix[array[-1]])):
                if adjacency_matrix[array[-1]][x] == 1:
                    number = x
                    adjacency_matrix[array[-1]][x] = 0
                    adjacency_matrix[x][array[-1]] = 0
                    break
            matrix_of_power[array[-1]] -= 1
            array.append(number)
            matrix_of_power[number] -= 1


def search_euler_loop(adjacency_matrix):
    matrix = deepcopy(adjacency_matrix)
    matrix_of_power = create_power_of_heights(matrix)
    if is_euler_loop(matrix_of_power):
        print("Граф містить Ейлеровий цикл")
    elif is_euler_path(matrix_of_power):
        print("Граф містить Ейлеровий шлях")
    else:
        print("Граф не містить Ейлерового циклу чи шляху")
        return
    stack = find_start_point(matrix_of_power)
    find_euler_path(stack, matrix_of_power, matrix)


def hamilton_cycle(curr, adjacency_matrix, n, path):
    path.append(curr)
    if len(path) == n:
        if adjacency_matrix[path[0]][path[-1]] == 1:
            return True
        else:
            path.pop()
            return False
    visited[curr] = True
    for next_my in range(n):
        if adjacency_matrix[curr][next_my] == 1 and not visited[next_my]:
            if hamilton_cycle(next_my, adjacency_matrix, n, path):
                return True
    visited[curr] = False
    path.pop()
    return False


def hamilton_path_for_single(curr, adjacency_matrix, n, path):
    path.append(curr)
    if len(path) == n:
        return True
    visited[curr] = True
    for next_my in range(n):
        if adjacency_matrix[curr][next_my] == 1 and not visited[next_my]:
            if hamilton_path_for_single(next_my, adjacency_matrix, n, path):
                return True
    visited[curr] = False
    path.pop()
    return False


def hamilton_path(adjacency_matrix, n, path):
    for x in range(n):
        path.clear()
        if hamilton_path_for_single(x, adjacency_matrix, n, path):
            return True
    return False


def show_hamilton_path(path):
    for x in path:
        print(x + 1, end="->")


myAdjacencyMatrix = create_adjacency_matrix(get_data())
search_euler_loop(myAdjacencyMatrix)
size = len(myAdjacencyMatrix)
visited = [False] * size
Path = []
if hamilton_cycle(0, myAdjacencyMatrix, size, Path):
    print("Знайдено гамільтоновий цикл: ")
    show_hamilton_path(Path)
else:
    Path = []
    visited = [False] * size
    if hamilton_path(myAdjacencyMatrix, size, Path):
        print("Знайдено гамільтоновий шлях: ")
        show_hamilton_path(Path)
    else:
        print("Гамільтонового шляху чи циклу не знайдено")
