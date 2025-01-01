from TrimMCStruct import Block, Structure
from defaultMb import defaultMb
from structReader import Reader
import sys


class creater:
    def create(self,index):
        if index>=len(self.blockList) or index>500:
            return None
        try:
            nextMb=defaultMb()
        except RecursionError as r:
             print(index)
             print(r)
             return
        nextMb=defaultMb()
        nextMb.defaultMba["movingBlock"]["name"]=self.blockList[-index-1][0].base_name
        nextMb.defaultMba["movingBlock"]["state"]=self.blockList[-index-1][0].states
        nextMb.setPisPos(nextMb.getPis(self.blockList[-index-1][1]))
        nextMb.defaultMba["movingEntity"]=self.create(index+1)
        print(nextMb.defaultMba["movingBlock"]["name"],nextMb.defaultMba["pistonPosX"],nextMb.defaultMba["pistonPosY"],nextMb.defaultMba["pistonPosZ"])
        return nextMb.defaultMba
    def __init__(self,io):

        self.reader=Reader(io)
        self.blockList=self.reader.traversXYZ()
        self.mb=defaultMb()
        self.struct=self.mb.struct
        self.io=io
        sys.setrecursionlimit(len(self.blockList)+1000)
    def main(self):
        message="成功转换"
        if len(self.blockList)>500:
             message="警告：结构文件大小超过500方块可能会在渲染时导致游戏崩溃"
        self.struct._special_blocks[26]["block_entity_data"]=self.create(0)
        with open(self.io, "wb") as f:
	        self.struct.dump(f)
        return message
             
        
if __name__=="__main__":     
    Creater=creater("test.mcstructure")
    print(Creater.main())
    
        
        


    
    

    


