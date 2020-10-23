#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math
from queue import PriorityQueue
from copy import deepcopy


# In[2]:


class PuzzleHeuristic:
    def __init__(self, size: int, goal_state: list):
        self.size = size
        self.goal_pos = {}
        for i in range(self.size):
            for j in range(self.size):
                self.goal_pos[goal_state[i][j]] = (i, j)

        def get(self, board, pos: tuple):
            pass


# In[3]:


class PuzzleNode:
    def __init__(self, board, gval, fval, parent):
        self.board = board
        self.size = len(self.board)
        self.gval = gval
        self.fval = fval
        self.parent = parent

    def __lt__(self, other):
        return self.fval < other.fval

    def generateChildren(self):
        children = []
        x,y = self.emptySlotPos()
        possible_moves = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

        for pos_to in possible_moves:
            child_board = self.move((x,y), pos_to)
            if child_board is not None:
                child_node = PuzzleNode(child_board, self.gval + 1, 0, self)
                children.append(child_node)
        return children

    def move(self, pos_from: tuple, pos_to: tuple):
        if pos_to[0] < 0 or pos_to[1] < 0 or pos_to[0] >= self.size or pos_to[1] >= self.size:
            return None
        new_board = deepcopy(self.board)
        new_board[pos_to[0]][pos_to[1]] , new_board[pos_from[0]][pos_from[1]] = new_board[pos_from[0]][pos_from[1]] , new_board[pos_to[0]][pos_to[1]]
        return new_board

    def emptySlotPos(self) -> tuple:
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return (i,j)

    def printBoard(self):
        for row in self.board:
            print(row)


# In[4]:


class Puzzle:
    def __init__(self, size: int, inital_state: list, goal_state: list):
        self.size = size
        self.start = inital_state
        self.goal = goal_state

    def hCost(self, node: PuzzleNode):
        h_cost = 0
        for i in range(self.size):
            for j in range(self.size):
                val = self.heuristic.get(node.board, (i,j))
                h_cost += val
        return h_cost

    def fCost(self, node: PuzzleNode):
        return self.hCost(node) + node.gval

    def tracePath(self, path, node: PuzzleNode):
        if node is not None:
            path = path + self.tracePath(path, node.parent)
            path.append(node)
        return path

    def solve(self, heuristic):
        self.heuristic = heuristic(self.size, self.goal)
        board = self.start
        closed_list = set()

        start_state = PuzzleNode(self.start, 0, 0, None)
        start_state.fval = self.hCost(start_state) + start_state.gval
        
        open_list = PriorityQueue()
        open_list.put((start_state.fval, start_state))
        
        cur_state = None
        iterations = 0
        while True:
            iterations += 1
            cur_state = open_list.get()[1]

            h_cost = cur_state.fval - cur_state.gval
            if (h_cost == 0):
                break

            for child_state in cur_state.generateChildren():
                if child_state not in closed_list:
                    child_state.fval = self.fCost(child_state)
                    open_list.put((child_state.fval, child_state))
            closed_list.add(cur_state)

        path = []
        print(cur_state)
        path = self.tracePath(path, cur_state)

        print('Iterations:', iterations)
        print('Path length:', len(path))
        return path


# In[5]:


class ManhattanSolver(PuzzleHeuristic):
    def __init__(self, size, goal_state):
        super().__init__(size, goal_state)

    def get(self, board, pos):
        goal_pos = self.goal_pos[board[pos[0]][pos[1]]]
        return abs(pos[0] - goal_pos[0]) + abs(pos[1] - goal_pos[1])


# In[6]:


class EuclideanSolver(PuzzleHeuristic):
    def __init__(self, size, goal_state):
        super().__init__(size, goal_state)

    def get(self, board, pos):
        goal_pos = self.goal_pos[board[pos[0]][pos[1]]]
        return math.sqrt((pos[0] - goal_pos[0])**2 + (pos[1] - goal_pos[1])**2)


# In[7]:


class NumOutOfPlaceSolver(PuzzleHeuristic):
    def __init__(self, size, goal_state):
        super().__init__(size, goal_state)

    def get(self, board, pos):
        goal_pos = self.goal_pos[board[pos[0]][pos[1]]]
        if pos[0] != goal_pos[0] or pos[1] != goal_pos[1]:
            return 1
        return 0


# In[8]:


initial_state = [
    [2, 4, 3],
    [1, 8, 5],
    [7, 6, 0]
]

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

puzzle = Puzzle(len(initial_state), initial_state, goal_state)


# In[9]:


def printPath(path):
    print('Path:')
    it = 0
    for state in path:
        it += 1
        print('#', it)
        state.printBoard()
    print('End')


# In[10]:


print('\nManhattan Test')
printPath(puzzle.solve(ManhattanSolver))


# In[11]:


print('\nEuclidean Test')
printPath(puzzle.solve(EuclideanSolver))


# In[12]:


print('\nNum out of place Test')
printPath(puzzle.solve(NumOutOfPlaceSolver))

