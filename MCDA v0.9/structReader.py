from TrimMCStruct import Block, Structure
from palette import palette
import heapq



class Reader:
    def dist(self,coord1,coord2):
        return abs(coord1[0]-coord2[0])+abs(coord1[1]-coord2[1])+abs(coord1[2]-coord2[2])
    def __init__(self,io):
        self.palette=palette()
        self.struct=Structure((1000,1000,1000),Block("minecraft","air"))
        if io!=None:
            with open(io, "rb") as f:
                self.struct = Structure.load(f)
            self.size=self.struct.size
            self.io=io
            self.coordList=self.getNonAirBlock()


    def getBlock(self,x,y,z):
        return self.struct.getblocknoBA((x,y,z))
    
    def getNonAirBlock(self):
        result=[]
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                for z in range(self.size[2]):
                    block=self.getBlock(x,y,z)
                    if block.base_name!="air":
                        result.append((x,y,z))
        return result
    
    @staticmethod
    def getdir(coord1,coord2):
        index=0
        dir=[3,0,5,0,4,1,2]
        for i in range(3):
            index+=(coord1[i]-coord2[i])*(i+1)
        return dir[index+3]
        
    
    def createPath(self,coord1,coord2,block,result):
        
        try:
            result[-1]=[block,coord1]
        except IndexError:
            result.append([block,coord1])
        air=self.palette.getBlockbyID(0)
        d=lambda v1,v2 : 1 if v2>v1 else -1
        dir=[d(coord1[0],coord2[0]),d(coord1[1],coord2[1]),d(coord1[2],coord2[2])]
        dirList=[(dir[0],0,0)]*(abs(coord2[0]-coord1[0]))+[(0,dir[1],0)]*(abs(coord2[1]-coord1[1]))+[(0,0,dir[2])]*(abs(coord2[2]-coord1[2]))
        coord=coord1
        for i in dirList:
            coord= tuple(map(lambda a, b: a + b, coord, i))
            result.append([air,coord])
        return result


    def minPath(self):
        result,path=[],[]
        currentPos=self.coordList[0]
        visited=set()
        for i in range(len(self.coordList)-1):
            
            visited.add(currentPos)
            nextPos=min([pos for pos in self.coordList if pos not in visited],key=lambda pos: self.dist(currentPos,pos))
            path=self.createPath(currentPos,nextPos,self.getBlock(currentPos[0],currentPos[1],currentPos[2]),path)
            currentPos=nextPos

        for i in range(len(path)-1):
            currentPos,nextPos=path[i][1],path[i+1][1]
            result.append([path[i][0],self.getdir(nextPos,currentPos)])
        result.append([path[-1][0],0])
        return result
    
    def traversPath(self):
        result=[]
        X,Y,Z,yDir,zDir=0,0,0,1,1

        for x in range(self.size[0]):
            for y in range(self.size[1]):
                for z in range(self.size[2]):
                    dir=3 if zDir==1 else 2
                    result.append([self.getBlock(X,Y,Z),dir])
                    Z+=zDir
                Z-=zDir
                result[-1][1]=0 if yDir==1 else 1
                zDir=zDir*(-1)
                Y+=yDir
            Y-=yDir
            result[-1][1]=5
            yDir=yDir*(-1)
            X+=1
        return result




        
        


    
