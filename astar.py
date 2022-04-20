from collections import deque
from queue import PriorityQueue
from algorithm import *
import time

class ZeroHeuristic:
    def heuristicEstimate(self, r):
        return 0
    def __repr__(self):
        return 'ZeroHeuristic'
class DistanceFromTargetToExit:
    def heuristicEstimate(self, r):
        targetVehicle = r.getTragetVehicle()
        dist = 6 - (targetVehicle.x+targetVehicle.length)
        return dist
    def __repr__(self):
        return 'DistanceFromTargetToExit'

class BlockingExitHeuristic:
    def heuristicEstimate(self,r):
        targetVehicle = r.getTragetVehicle()
        if targetVehicle.x==4:
            return 0
        vehiclesBlockingExit = 1
        for vehicle in r.vehicles:
            if vehicle.vehicleType=='V' and vehicle.x >= (targetVehicle.x+targetVehicle.length) and (vehicle.y <= targetVehicle.y and vehicle.y+vehicle.length> targetVehicle.y):
                vehiclesBlockingExit +=1
        return  vehiclesBlockingExit

    def __repr__(self):
        return 'BlockingExitHeuristic'

class BlockingLowerBoundEstimation:
    def heuristicEstimate(self,r):
        targetVehicle = r.getTragetVehicle()
        if targetVehicle.x==4:
            return 0
        blockingCount=1
        blockingVehicle = []
        for vehicle in r.vehicles:
            if vehicle.vehicleType=='V' and vehicle.x >= (targetVehicle.x+targetVehicle.length) and (vehicle.y <= targetVehicle.y and vehicle.y+vehicle.length> targetVehicle.y):
                blockingCount +=1
                blockingVehicle.append(vehicle)
        blocking2 = {}

        for v in blockingVehicle:
            d = self._getBestDirectionToMove(r,v)
            if d =='UP':
                for vv in r.vehicles:
                    if vv != v and vv.y < 2 and vv.y <= v.x - v.length and vv.x<= v.x and vv.x+vv.length>v.x and vv.vehicleType=='H':
                        blocking2[vv] = 1
            else:
                for vv in r.vehicles:
                    if vv != v and vv.y > 2 and vv.y >= v.y + v.length and ((vv.x<= v.x and vv.x+vv.length>v.x and vv.vehicleType=='H')or(vv.vehicleType=='V' and vv.x == v.x)):#and vv.y > 2 and vv.y <= 2 + v.length and vv.x<= v.x and vv.x+vv.length>v.x and vv.vehicleType=='H':
                        blocking2[vv] = 1
        blockingCount += len(blocking2)
        return blockingCount
    def _getBestDirectionToMove(self, rushHour, vehicle):
        if vehicle.length==3:
            return 'DOWN'
        vehicleUPCount = 0
        vehicleDownCount = 0
        for v in rushHour.vehicles:
                if v != vehicle:
                    if v.y > 2 and v.y >= 2 + vehicle.length and ((v.x<= vehicle.x and v.x+v.length>vehicle.x and v.vehicleType=='H')or(v.vehicleType=='V' and v.x == vehicle.x)):
                        vehicleDownCount+= 1
                    if v.y < 2 and v.y <= 2 - vehicle.length and v.x<= vehicle.x and v.x+v.length>vehicle.x and v.vehicleType=='H':
                        vehicleUPCount += 1
        if vehicleUPCount >= vehicleDownCount:
            return 'DOWN'
        return'UP'
    def __repr__(self):
        return 'BlockingLowerBoundEstimation'
class AStar:
    def __init__(self, heuristicFun):
        self.heuristicFun = heuristicFun
    def heuristicEstimate(self,start):
        return self.heuristicFun.heuristicEstimate(start)

    def neighborNodes(self,current):
        return current.moves()

    def aStar(self,start):
        cameFrom = {}
        openSet = PriorityQueue()
        openSet.put(start)
        closedSet = set()
        gScore = {}
        gScore[start] = 0
        expandedNodes = 1
        current = start
        solution = []
        while not openSet.empty() and gScore[current]<100:
            current = openSet.get()
            solution.append(current)
            if current.solved():
                return {'Expanded Nodes': expandedNodes, 'Steps': gScore[current], 'Solution':self.__reconstructPath(cameFrom, current)}
            closedSet.add(current)
            for neighbor in self.neighborNodes(current):
                tentative_gScore = current.depth + 1
                neighbor.depth = tentative_gScore
                neighbor.hvalue = self.heuristicEstimate(neighbor)
                if neighbor in closedSet:# and tentative_gScore >= gScore[neighbor]:
                    continue
                if neighbor not in openSet.queue:
                    expandedNodes += 1
                    openSet.put(neighbor)
                else:
                    if tentative_gScore< gScore[neighbor]:
                        openSet.put(neighbor)
                    else:
                        continue
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore


        return {'Expanded Nodes': expandedNodes, 'Steps':-1, 'Solution':None}

    def __reconstructPath(self, cameFrom, current):
        total_path = [current]
        while current in cameFrom.keys():
            current = cameFrom[current]
            total_path.insert(0,current)
        return total_path

