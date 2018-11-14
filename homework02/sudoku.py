from typing import Any, Union, List



def read_sudoku(puzzle1):
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(puzzle1).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def group(values, n):
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    list1 = []
    list2 = []
    j = 0
    for i in values:
        if j < n:
            list2.append(i)
            j += 1
        if j == n:
            j = 0
            list1.append(list2)
            list2 = []
    return list1


def display(values):
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width)+('|' if str(col)in'25'else'')for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def get_row(values, pos):
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    row, col = pos
    i = 0
    new_data = []
    for j in values:
        if i == row:
            new_data = j
        i += 1
    return new_data


def get_col(values, pos):
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    row, col = pos
    new_data = []
    for j in values:
        for i in range(len(j)):
            if i == col:
                new_data.append(j[i])
    return new_data


def get_block(values, pos):
    """ Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    block = []
    block_row = (pos[0] // 3) * 3
    block_col = (pos[1] // 3) * 3
    for i in range(3):
        for j in range(3):
            block.append(values[block_row + i][block_col + j])
    return block


def find_empty_positions(grid):
    """ Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2','.'],['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2','3'],['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2','3'],['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for row in range(len(grid)):
        for col in range(len(grid)):
            if grid[row][col] == '.':
                return(row, col)
    return None


def find_possible_values(grid: list, pos: tuple) -> set:
    """ Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    row = get_row(grid, pos)
    col = get_col(grid, pos)
    block = get_block(grid, pos)
    possible_values = set()
    for i in range(1, 10):
        if not str(i) in row and not str(i) in col and not str(i) in block:
            possible_values.add(str(i))
    return possible_values


def solve(grid: list) -> Any:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    pos = find_empty_positions(grid)
    if not pos:
        return grid
    possible_values = find_possible_values(grid, pos)
    for i in possible_values:
        grid[pos[0]][pos[1]] = i
        if solve(grid):
            return(grid)
        else:
            grid[pos[0]][pos[1]] = '.'
    return None


def check_solution(solution):
    """ Если решение solution верно, то вернуть True, в противном случае False """
    for i in range(9):
        for j in row(9):
            pos = (i, j)
            row = get_row(solution, pos)
            for num in row:
                if row.count(num) != 1:
                    return False
            col = get_col(solution, pos)
            for num in col:
                if col.count(num) != 1:
                    return False
            block = get_block(solution, pos)
            for num in block:
                if block.count(num) != 1:
                    return False
    return True

if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
