

import random
import math

Max_Length = int(input())
Initial_Temperature = 30.0
Final_Temperature = 0.5
Alpha = 0.97
Steps_per_Change = 100


class memberType:
    solutionType = []
    energy = 0.0


def tweakSolution(member):
    x = random.randrange(Max_Length)
    y = random.randrange(Max_Length)
    while x == y:
        y = random.randrange(Max_Length)
    member.solutionType[x], member.solutionType[y] = member.solutionType[y], member.solutionType[x]


def initializeSolution(member):
    for i in range(Max_Length):
        member.solutionType.append(i)
    for j in range(Max_Length):
        tweakSolution(member)


def computeEnergy(member):
    dx = [-1, 1, -1, 1]
    dy = [-1, 1, 1, -1]
    board = [[' ' for i in range(Max_Length)] for j in range(Max_Length)]
    for i in range(Max_Length):
        board[i][member.solutionType[i]] = 'Q'

    conflicts = 0

    for i in range(Max_Length):
        x = i
        y = member.solutionType[i]
        for j in range(4):
            tempx, tempy = x, y
            while 1:
                tempx += dx[j]
                tempy += dy[j]
                if tempy < 0 or tempx >= Max_Length or tempy < 0 or tempy >= Max_Length:
                    break
                if board[tempx][tempy] == 'Q':
                    conflicts += 1

        member.energy = float(conflicts)


def copySolution(dest, src):
    for i in range(Max_Length):
        dest.solutionType[i] = src.solutionType[i]
    dest.energy = src.energy


def emitSolution(member):
    board = [['' for i in range(Max_Length)] for j in range(Max_Length)]

    for i in range(Max_Length):
        board[i][member.solutionType[i]] = 'Q'

    print("board:")
    for x in range(Max_Length):
        for y in range(Max_Length):
            if board[x][y] == 'Q':
                print("Q", end=" ")
            else:
                print(". ", end="")
        print()


# Main
timer, solution = 0, 0
useNew, accepted = 0, 0
temperature = Initial_Temperature
current, working, best = memberType(), memberType(), memberType()
database = open('DataBase.txt', 'w')
initializeSolution(current)

computeEnergy(current)
best.energy = 100.0

copySolution(working, current)

while temperature > Final_Temperature:
    accepted = 0
    for step in range(Steps_per_Change):
        useNew = 0
        tweakSolution(working)
        computeEnergy(working)
        if working.energy <= current.energy:
            useNew = 1
        else:
            test = random.random()
            delta = working.energy - current.energy
            calc = math.exp(-delta / temperature)
            if calc > test:
                accepted += 1
                useNew = 1
        if useNew:
            useNew = 0
            copySolution(current, working)

            if current.energy < best.energy:
                copySolution(best, current)
                solution = 1
        else:
            copySolution(working, current)
    timer += 1

    database.write(str(timer) + " " + str(temperature) + " " + str(best.energy) + " " + str(accepted) + '\n')
    temperature *= Alpha
database.close()
if solution:
    emitSolution(best)