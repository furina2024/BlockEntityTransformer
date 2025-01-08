from TrimMCStruct import Block, Structure
from defaultMb import defaultMb
from structReader import Reader
from palette import palette
from scipy.interpolate import splprep, splev
import copy
import sys
import os
import numpy as np

class creater:

    palette=palette()

    @classmethod
    def getBlock(cls,id):
        return cls.palette.getBlockbyID(id)

    def create(self,index,offset=0):
        if index>=len(self.blockList) or index>600:
            return None
        try:
            nextMb=defaultMb()
        except RecursionError as r:
             print(index)
             print(r)
             return
        nextMb=defaultMb()
        nextMb.defaultMba["movingBlock"]["name"]=self.blockList[-index-1][0].base_name
        nextMb.defaultMba["movingBlock"]["states"]=self.blockList[-index-1][0].states
        nextMb.setPisPos(nextMb.getPis(self.blockList[-index-1][1]))
        nextMb.defaultMba["movingEntity"]=self.create(index+1)
        return nextMb.defaultMba

    def __init__(self,io,base_name,type="最小路径遍历解析",size=(3,3,3)):
        self.reader=Reader(io)
        if io and os.path.isfile(io):
            if type=="最小路径遍历解析":
                self.blockList=self.reader.minPath()
            elif type=="全位置遍历解析":
                self.blockList=self.reader.traversPath()
            else:
                self.blockList=[]
        else:
            self.blockList=[]
        self.mb=defaultMb(size)
        self.struct=self.mb.struct
        self.base_name=base_name
        sys.setrecursionlimit(len(self.blockList)+1000)

    def main(self):
        message="成功转换"
        if len(self.blockList)>600:
             message="警告：结构文件大小超过600方块可能会在渲染时导致游戏崩溃"
        self.struct._special_blocks[26]["block_entity_data"]=self.create(0)
        return message
    
    def save(self,io):
        with open(io, "wb") as f:
	        self.struct.dump(f)

    def getLayer(self,deepth):
        if deepth>len(self.blockList):
            return None
        mba=self.struct._special_blocks[26]["block_entity_data"]
        getnextlayer=lambda layer:copy.deepcopy(layer["movingEntity"])
        layer=mba
        for i in range(deepth):
            layer=getnextlayer(layer)
        try:
            layer["movingEntity"]=None
        except TypeError:
            pass
        return layer

    def getChgLayer(self,deepth):
        if deepth>len(self.blockList):
            return None
        mba=self.struct._special_blocks[26]["block_entity_data"]
        getnextlayer=lambda layer:layer["movingEntity"]
        layer=mba
        for i in range(deepth):
            layer=getnextlayer(layer)
        return layer

    def setLayer(self,deepth,name,states,extraname,extrastate):
        preLayer=self.getChgLayer(deepth)
        if preLayer==None:
            return
        preLayer["movingBlock"]["name"]=name
        preLayer["movingBlock"]["states"]=states
        preLayer["movingBlockExtra"]["name"]=extraname
        preLayer["movingBlockExtra"]["states"]=extrastate

    def mergeWithPis(self,creaters):
        newCreater=creater(None,"mergedStruct")
        for c in creaters:
            newCreater.blockList+=c.blockList
        newCreater.main()
        return newCreater

    def merge(self,creaters):
        newCreater=creater(None,"mergedStruct")
        newCreater.struct=Structure((64,3,3))
        i=0
        pisLayer=[]
        for Creater in creaters:
            for x in range(3):
                for y in range(3):
                    for z in range(3):
                        newCreater.struct.set_block((x+i*4,y,z),Creater.struct.getblocknoBA((x,y,z)))
                        newCreater.struct._special_blocks={}
                
            newCreater.struct.set_block((2+i*4,2,2),Creater.getBlock(1))
            newCreater.blockList+=Creater.blockList
            pisLayer+=[i]*len(Creater.blockList)
            i+=1
        newCreater.struct.set_block((2,2,2),Creater.struct.get_block((2,2,2)))
        newCreater.main()
        i,getNextLayer=0,lambda preLayer : preLayer["movingEntity"]
        Layer=newCreater.struct._special_blocks[26]["block_entity_data"]
        while Layer["movingEntity"]!=None:
            nextLayer=getNextLayer(Layer)
            nextLayer["pistonPosX"]=nextLayer["pistonPosX"]+4*pisLayer[i]
            Layer=nextLayer
            i+=1
        return newCreater

class mover(creater):
    def __init__(self,io, creater,base_name="movedStruct",type="minPath", size=(3, 3, 3)):
        super().__init__(io, type, size)
        self.base_name="movedStruct"
        self.creater=creater
        self.reader=Reader(None)

    @classmethod
    def genePath(cls,points):
        points = np.array(points)
        x, y, z = points[:, 0], points[:, 1], points[:, 2]
        tck, u = splprep([x, y, z], s=0,k=1)
        startPoint=min(points,key=lambda p: p[0])
        endPoint=max(points,key=lambda p: p[0])
        pointNum=int(round(max([abs(endPoint[i]-startPoint[i]) for i in range(3)])))

        new_points = splev(np.linspace(0,1, pointNum), tck)
        return new_points

    def savePath(self,path):
        if path==None:
            return
        points=[]
        for i in range(len(path[0])):
            points.append((round(path[0][i]),round(path[1][i]),round(path[2][i])))
        self.reader.coordList=points
        Path=self.reader.minPath()
        self.blockList=Path
        self.struct=Structure((len(Path)*2+20,3,3))
        for i in range(len(Path)):
            self.struct.set_block((i*2+5,0,0),self.mb.struct.get_block(self.mb.getPis(Path[i][1])))
        
        self.mb.struct._special_blocks[26]["block_entity_data"]=self.save_(0)
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    self.struct.set_block((x,y,z),self.mb.struct.get_block((x,y,z)))

    def save_(self,index):
        if index>=len(self.blockList) or index>600:
            return self.creater.struct._special_blocks[26]["block_entity_data"]
        try:
            nextMb=defaultMb()
        except RecursionError as r:
            print(index)
            print(r)
            return
        nextMb=defaultMb()
        nextMb.defaultMba["movingBlock"]["name"]=self.blockList[-index-1][0].base_name
        nextMb.defaultMba["movingBlock"]["states"]=self.blockList[-index-1][0].states
        nextMb.defaultMba["pistonPosX"]=index*2+5
        nextMb.defaultMba["pistonPosY"]=0
        nextMb.defaultMba["pistonPosZ"]=0
        nextMb.defaultMba["movingEntity"]=self.save_(index+1)
        return nextMb.defaultMba
