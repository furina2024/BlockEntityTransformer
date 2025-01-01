from TrimMCStruct import Block, Structure
import copy

class defaultMb:
    def __init__(self):
        with open("default.mcstructure", "rb") as f:
            self.struct = Structure.load(f)
        self.defaultMba=copy.deepcopy(self.struct._special_blocks[26]["block_entity_data"])
        self.defaultMba["x"]=2
        self.defaultMba["y"]=2
        self.defaultMba["z"]=2
        
    
    def setPisPos(self,coord):
        self.defaultMba["pistonPosX"],self.defaultMba["pistonPosY"],self.defaultMba["pistonPosZ"]=coord
    
    def setMbablock(self,Block):
        self.defaultMba["movingBlock"]=Block
    
    def getPis(self,dir):
        dirList=[(0,2,0),(0,2,2),(2,0,2),(2,0,0),(0,0,2),(0,0,0)]
        return dirList[dir]


    