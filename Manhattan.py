import math
import sys
import datetime
def main():
    read()
def read():
    with open("Input8PuzzleCases.txt", "r") as file1:
        starttime=datetime.datetime.now()
        stepstotal=0
        linetotal=0
        for line in file1:
            linetotal=linetotal+1
            stepstotal=stepstotal+Manhattan(getStartstate(line))
            stoptime=datetime.datetime.now()
        print(stepstotal)
        print("Avg Steps=",stepstotal/linetotal)
        print("Time=",(stoptime-starttime),"secs")
def getStartstate(line):
    l=line.split(',')
    list1=list()
    for i in l:
        print(i)
        list1.append(int(i))
    return list1
def Manhattan(startstate):
    startState=startstate
    endState=[0, 1, 2, 3, 4, 5, 6, 7, 8]
    e=map(str,endState)
    end=''.join(e)
    nodeSet=set()
    s=map(str, startState)
    list=''.join(s)
    nodeSet.add(list)
    g=0
    f=0
    global h
    stepArray=[]
    global breakLoop
    breakLoop=False
    stepArray.append(startState)
    while not breakLoop:
        global stepNodeArray
        stepNodeArray=[]
        g = g + 1
        for node in stepArray:
            indexOfZero=node.index(0)
            if(canMoveUp(indexOfZero)):
                newNode=getNewNode(node,indexOfZero,indexOfZero - 3)
                print(newNode)
                N = map(str, newNode)
                newNs = ''.join(N)
                if not newNs in nodeSet:
                    print (newNode)
                    stepNodeArray=processNode(stepNodeArray, newNode)
                    if breakLoop:
                        break
                    nodeSet.add(newNs)
            if(canMoveRight(indexOfZero)):
                newNode=getNewNode(node,indexOfZero,indexOfZero + 1)
                print(newNode)
                N = map(str, newNode)
                newNs = ''.join(N)
                if not newNs in nodeSet:
                    print (newNode)
                    stepNodeArray=processNode(stepNodeArray, newNode)
                    if breakLoop:
                        break
                    nodeSet.add(newNs)
            if(canMoveDown(indexOfZero)):
                newNode=getNewNode(node,indexOfZero,indexOfZero + 3)
                print(newNode)
                N = map(str, newNode)
                newNs = ''.join(N)
                if not newNs in nodeSet:
                    print (newNode)
                    stepNodeArray=processNode(stepNodeArray, newNode)
                    if breakLoop:
                        break
                    nodeSet.add(newNs)
            if(canMoveLeft(indexOfZero)):
                newNode=getNewNode(node,indexOfZero,indexOfZero - 1)
                print(newNode)
                N = map(str, newNode)
                newNs = ''.join(N)
                if not newNs in nodeSet:
                    print (newNode)
                    stepNodeArray=processNode(stepNodeArray, newNode)
                    if breakLoop:
                        break
                    nodeSet.add(newNs)
        print(" ")
        print(" ")
        print("h====",h)
        f=g+h
        print('f====',f)
        print("g=", g)
        print("Nodes", len(stepNodeArray))
        print("================================")
        stepArray = []
        stepArray=stepNodeArray[:]

def getNewNode(node,indexOfZero, toIndex):
    newNode=node[:]
    toValue=newNode[toIndex]
    newNode[toIndex]=0
    newNode[indexOfZero]=toValue
    #newNode.set(toIndex, 0)
    #newNode.set(indexOfZero, toValue)
    return newNode
def processNode(stepNodeArray,newNode):
    nodeH=calculateHeuristic(newNode)
    print(nodeH)
    if nodeH == 0:
        print (newNode)
        breakLoop = True
        sys.exit()

    else:
        if len(stepNodeArray) == 0:
            stepNodeArray.append(newNode)
            global h
            h= nodeH
            print(h)
        else:
            if nodeH < h:
                stepNodeArray=[]
                stepNodeArray.append(newNode)
                h=nodeH
            elif nodeH == h:
                stepNodeArray.append(newNode)
    return stepNodeArray

def calculateHeuristic(newNode):
    h = 0
    targetRow = 0
    currentRow = 0
    targetCol = 0
    currentCol = 0
    for i in range(1,9):
        pos = newNode.index(i)
        currentRow = getCurrentRow(pos)
        currentCol = getCurrentCol(pos)
        targetRow = getTargetRow(i)
        targetCol = getTargetCol(i)
        diff = math.fabs(currentRow - targetRow) + math.fabs(currentCol - targetCol)
        h = h + diff
    return h
def getTargetCol(i):
    if i==3 or i == 6:
        return 1
    if i==1 or i==4 or i==7:
        return 2
    return 3
def getTargetRow(i):
    if i==1 or i == 2:
        return 1
    if i==3 or i==4 or i==5:
        return 2
    return 3
def getCurrentCol(pos):
    if pos ==0 or pos==3 or pos == 6:
        return 1
    if pos==1 or pos==4 or pos==7:
        return 2
    return 3
def getCurrentRow(pos):
    if pos <=2:
        return 1
    if pos<=5:
        return 2
    return 3



def canMoveUp(indexOfZero):
    return not (indexOfZero == 0 or indexOfZero == 1 or indexOfZero == 2)
def canMoveDown(indexOfZero):
    return not (indexOfZero == 6 or indexOfZero == 7 or indexOfZero == 8)
def canMoveLeft(indexOfZero):
    return not (indexOfZero == 0 or indexOfZero == 3 or indexOfZero == 6)
def canMoveRight(indexOfZero):
    return not (indexOfZero == 2 or indexOfZero == 5 or indexOfZero == 8)
if __name__ == "__main__":
	main()
