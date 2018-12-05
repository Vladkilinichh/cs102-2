import pygame
from pygame.locals import *
import random
from copy import deepcopy


class GameOfLife:

    def __init__(self, width=640, height=480, cell_size=10, speed=10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('DimGray'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('DimGray'),
                    (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.clist = CellList(self.cell_height, self.cell_width, True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_cell_list(self.clist)
            self.clist = self.clist.update()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def draw_cell_list(self, clist) -> None:
        for cell in clist:
            x = cell.col * self.cell_size
            y = cell.row * self.cell_size
            rect = (x + 1, y + 1, self.cell_size - 1, self.cell_size - 1)
            if cell.is_alive() == 1:
                cell_color = pygame.Color('LightSkyBlue3')
            else:
                cell_color = pygame.Color('white')
            pygame.draw.rect(self.screen, cell_color, rect)


class Cell:

    def __init__(self, row: int, col: int, state=False) -> None:
        self.row = row
        self.col = col
        self.state = state

    def is_alive(self):
        return self.state


class CellList:

    def __init__(self, nrows: int, ncols: int, randomize=False,
                 is_file: bool=False, file_clist: list=[]) -> None:
        self.nrows = nrows
        self.ncols = ncols
        self.randomize = randomize
        self.clist = []
        for i in range(nrows):
            self.clist.append([])
            for j in range(ncols):
                state = 0
                if randomize:
                    state = random.randint(0, 1)
                cell = Cell(i, j, state)
                self.clist[i].append(cell)
        self.x = 0
        self.y = 0

    def get_neighbours(self, cell) -> list:
        neighbours = []
        ri = cell.row
        ci = cell.col
        for i in range(ri - 1, ri + 2):
            for j in range(ci - 1, ci + 2):
                if (i, j) != cell and i >= 0 and i < len(self.clist) and j >= 0 and j < len(self.clist[0]):
                    neighbours.append(self.clist[i][j])
        return neighbours

    def update(self) -> list:
        new_clist = deepcopy(self)
        for row in range(self.nrows):
            for col in range(self.ncols):
                neighbours = new_clist.get_neighbours(
                    new_clist.clist[row][col])
                sum = 0
                for i in neighbours:
                    if i.is_alive() == 1:
                        sum += 1
                if new_clist.clist[row][col].is_alive() == 0 and sum == 3:
                    self.clist[row][col] = Cell(row, col, True)
                elif new_clist.clist[row][col].is_alive() == 1 and (
                        sum == 2 or sum == 3):
                    self.clist[row][col] = Cell(row, col, True)
                else:
                    self.clist[row][col] = Cell(row, col, False)
        return self

    def __iter__(self):
        return self

    def __next__(self) -> Cell:
        if self.y < len(self.clist[0]):
            cell = self.clist[self.x][self.y]
            self.y += 1
            return cell
        elif self.x < len(self.clist):
            self.x += 1
            self.y = 0
            if self.x < len(self.clist):
                return self.__next__()
            else:
                self.x = 0
                self.y = 0
                raise StopIteration

    def __str__(self):
        list_of_states = []
        for i, row in enumerate(self.clist):
            list_of_states.append([])
            for elem in row:
                list_of_states[i].append(int(elem.is_alive()))
        return list_of_statess

    @classmethod
    def from_file(cls, filename) -> list:
        grid = []
        with open(filename) as file:
            line = file.readline()
            row = 0
            while line:
                grid.append([])
                col = 0
                for pos in line:
                    if pos in '01':
                        grid[row].append(Cell(row, col, bool(int(pos))))
                        col += 1
                line = file.readline()
                row += 1
        clist = cls(len(grid), len(grid[0]))
        clist.clist = grid
        return clist


if __name__ == '__main__':
    game = GameOfLife(900, 600, 20)
    game.run()

