from .algorithm import *
from .edge import cubeEdges
from .corner import cubeCorners

from .algorithm import (
    setCube as algoSetCube,
    displayCube as algoDisplayCube,
    solveEdges as algoSolveEdges,
    solveCorners as algoSolveCorners
)

def reset():
    # cubeEdges.edgeCount = 0
    # cubeEdges.edgeColor.clear()
    # cubeEdges.edgeIndex.clear()

    cubeEdges.edgeSequence.clear()


    # ✅ corner 초기화 - 실제 정의된 것만
    cubeCorners.cornerSequence.clear()

    # ❌ 아래는 정의 안 되어 있으니 제거
    # cubeCorners.cornerCount = 0
    # cubeCorners.cornerColor.clear()
    # cubeCorners.cornerIndex.clear()

def setCube(sides):
    algoSetCube(sides)

def displayCube():
    return algoDisplayCube()

def solveEdges():
    return algoSolveEdges()

def solveCorners():
    return algoSolveCorners()
