from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget,QMessageBox,QFileDialog,QTableWidgetItem,QTreeWidgetItem,QGraphicsScene
from PyQt5.QtCore import Qt,QPointF
from creater import creater,mover
from palette import palette
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from TrimMCStruct import Block
import sys
import os
import matplotlib.pyplot as plt
import numpy as np

class window(QWidget):
    def __init__(self):
        super().__init__()
        self.ui=uic.loadUi(r"UI/mainwindow.ui",self)
        self.ui.importButton.clicked.connect(self.importFile)
        self.tableRow=0
        self.creaters=[]
        self.ui.structEditer.clicked.connect(self.editor_clicked)
        self.editor=structeditor_Window(self)
        self.displayTable.itemClicked.connect(self.item_clicked)
        self.structMerge.clicked.connect(self.mergePage)
        self.mergeinButton.clicked.connect(self.mergeinPage)
        self.mergepage=mergePage(self,"merge")
        self.mergeinpage=mergePage(self,"mergein")
        self.moverPage=moverPage(self)
        self.introPage=introWindow(self)
        self.moverButton.clicked.connect(self.moverpage)
        self.saveButton.clicked.connect(self.saveStruct)
        self.clearButton.clicked.connect(self.clear)
        self.introButton.clicked.connect(self.intro)
        self.selected=None
        self.selectedStruct=None

    def intro(self):
        self.introPage.show()

    def clear(self):
        self.creaters=[]
        self.moverPage.structList.clear()
        self.mergeinpage.structList.clear()
        self.mergepage.structList.clear()
        self.ui.ioShower.clear()
        self.ui.displayTable.clearContents()

    def saveStruct(self):
        for i in range(len(self.creaters)):
            if str(self.creaters[i].base_name).strip()==str(self.selected).strip():
                self.selectedStruct=self.creaters[i]
                break
        if self.selectedStruct==None:
            QMessageBox.information(None, "报错", "你还没选择要保存的结构")
            return
        if self.GlassSave.isChecked():
            pass
        else:
            self.selectedStruct.struct.set_block((2,2,2),Block("minecraft","movingblock"))
        file_path = QFileDialog.getExistingDirectory(self, "选择文件夹", "")
        file_name = "struct.mcstructure"
        full_path = os.path.join(file_path, file_name)
        self.selectedStruct.save(full_path)
        QMessageBox.information(None, "提示", "成功保存")

    def moverpage(self):
        self.moverPage.show()
        self.moverPage.structList.clear()
        for c in self.creaters:
            self.moverPage.structList.addItem(c.base_name)

    def mergeinPage(self):
        self.mergeinpage.show()
        self.mergeinpage.structList.clear()
        for c in self.creaters:
            self.mergeinpage.structList.addItem(c.base_name)

    def mergePage(self):
        self.mergepage.show()
        self.mergepage.structList.clear()
        for c in self.creaters:
            self.mergepage.structList.addItem(c.base_name)

    def item_clicked(self,item):
        self.displayTable.setCurrentItem(item)
        self.selected=self.displayTable.currentItem().text()
        print(self.selected)
        self.editor.selected=self.displayTable.currentItem().text()

    def importFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "")
        if file_path:
            if os.path.splitext(file_path)[1].strip()==".mcstructure":
                self.updateIoShower(file_path)
            else:
                QMessageBox.information(None, "错误", "必须导入mcstructure文件")
                return
        readMode = self.ui.readMode.currentText()
        self.ui.displayTable.setItem(self.tableRow, 0, QTableWidgetItem(os.path.basename(file_path)))
        self.ui.displayTable.setItem(self.tableRow, 1, QTableWidgetItem(readMode))
        self.tableRow+=1
        Creater=creater(file_path,os.path.basename(file_path),readMode)
        Creater.main()
        self.creaters.append(Creater)

    def editor_clicked(self):
        for i in range(len(self.creaters)):
            if str(self.creaters[i].base_name).strip()==str(self.editor.selected).strip():
                self.editor.selected=i
                break
                
        self.editor.show()

    def updateIoShower(self,io):
        self.ui.ioShower.clear()
        self.ui.ioShower.setPlainText(io)

class introWindow(QWidget):
    def __init__(self,mainwindow):
        super().__init__()
        self.ui=uic.loadUi("UI/intro.ui",self)

class structeditor_Window(QWidget):

    def __init__(self,mainwindow):
        self.addItem_blocksearcher=False
        self.palette1=palette()
        super().__init__()
        self.ui=uic.loadUi("UI/editor.ui",self)
        self.deepth.textChanged.connect(self.deepthset)
        self.mainwindow=mainwindow
        self.selected=0
        self.deep=0
        self.blocksearcher.textChanged.connect(self.searchBlock)
        self.blockList.currentTextChanged.connect(self.createLabel)
        self.saveLabel.clicked.connect(self.save)
        self.deleteLabel.clicked.connect(self.deletelabel)

    def deletelabel(self):
        self.targetTree.clear()

    def save(self):
        treeDict=self.tree_to_dict(self.targetTree)
        print(treeDict)
        self.mainwindow.creaters[self.selected].setLayer(self.deep,
                               treeDict["blockentity"]["movingBlock"]["name"]["value"][1],
                               treeDict["blockentity"]["movingBlock"]["states"]["value"][1],
                               treeDict["blockentity"]["movingBlockExtra"]["name"]["value"][1],
                               treeDict["blockentity"]["movingBlockExtra"]["states"]["value"][1]
                               )
        print(self.mainwindow.creaters[self.selected].struct._special_blocks[26]["block_entity_data"])

    def createLabel(self,text):
        if not self.addItem_blocksearcher:
            self.targetTree.clear()
            block=self.palette1.getBlockbyName(text)
            air=self.palette1.getBlockbyID(0)
            print(block.base_name)
            blockentity=self.palette1.createMbEntity(block.base_name,block.states,air.base_name,air.states)
            self.initTree(blockentity,self.targetTree)
            print(blockentity)
            print("--------------------")

    def searchBlock(self):
        self.addItem_blocksearcher=True
        blockname=self.blocksearcher.toPlainText()
        blockList=self.palette1.searchBlocks(blockname)
        self.blockList.clear()
        for block in blockList:
            self.blockList.addItem(block)
        self.addItem_blocksearcher=False

    def initTree(self,blockentity,tree):
        root = QTreeWidgetItem(tree)
        tree.setColumnCount(2)
        root.setText(0, "blockentity")
        tree.addTopLevelItem(root)
        block=QTreeWidgetItem(["movingBlock", ""])
        extrablock=QTreeWidgetItem(["movingBlockExtra", ""])
        root.addChild(block)
        root.addChild(extrablock)
        root.addChild(QTreeWidgetItem(["movingEntity", "..."]))
        root.addChild(QTreeWidgetItem(["pistonX", str(blockentity["pistonPosX"])]))
        root.addChild(QTreeWidgetItem(["pistonY", str(blockentity["pistonPosY"])]))
        root.addChild(QTreeWidgetItem(["pistonZ", str(blockentity["pistonPosZ"])]))
        root.addChild(QTreeWidgetItem(["x", str(blockentity["x"])]))
        root.addChild(QTreeWidgetItem(["y", str(blockentity["y"])]))
        root.addChild(QTreeWidgetItem(["z", str(blockentity["z"])]))
        blockname=QTreeWidgetItem(["name", blockentity["movingBlock"]["name"]])
        blockstate=QTreeWidgetItem(["states", str(blockentity["movingBlock"]["states"])])
        extrablockname=QTreeWidgetItem(["name", blockentity["movingBlockExtra"]["name"]])
        extrablockstate=QTreeWidgetItem(["states", str(blockentity["movingBlockExtra"]["states"])])
        blockname.setFlags(blockname.flags() | Qt.ItemIsEditable)
        blockstate.setFlags(blockstate.flags() | Qt.ItemIsEditable)
        extrablockname.setFlags(extrablockname.flags() | Qt.ItemIsEditable)
        extrablockstate.setFlags(extrablockstate.flags() | Qt.ItemIsEditable)
        block.addChild(blockname)
        block.addChild(blockstate)
        extrablock.addChild(extrablockname)
        extrablock.addChild(extrablockstate)

    def deepthset(self):
        deepth=self.deepth.toPlainText()
        if deepth!='': 
            deepth = int(deepth)
        else:
            return
        if not self.mainwindow.creaters[self.selected]:
            return
        try:
            self.originTree.clear()
            layer=self.mainwindow.creaters[self.selected].getLayer(deepth)
            self.originTree.setHeaderLabels([str(deepth), ""])
            self.initTree(layer,self.originTree)
            self.deep=deepth
        except TypeError:
            pass

    def tree_to_dict(self, tree):
        def item_to_dict(item):
            node_dict = {"value": [item.text(i) for i in range(item.columnCount())]}
            for i in range(item.childCount()):
                child = item.child(i)
                node_dict[child.text(0)] = item_to_dict(child)
            return node_dict

        tree_dict = {}
        for i in range(tree.topLevelItemCount()):
            top_item = tree.topLevelItem(i)
            tree_dict[top_item.text(0)] = item_to_dict(top_item)
        return tree_dict

class mergePage(QWidget):
    def __init__(self,mainwindow,mergetype):
        super().__init__()
        self.mergeType=mergetype
        self.mainwindow=mainwindow
        if self.mergeType=="merge":
            self.ui=uic.loadUi("UI/structMerge.ui",self)
        else:
            self.ui=uic.loadUi("UI/structAdd.ui",self)
        self.addStruct.clicked.connect(self.addStruct_)
        self.delButton.clicked.connect(self.delstruct)
        self.creaters=[]
        self.tableRow=0

    def addStruct_(self):
        struct = self.ui.structList.currentText()
        self.ui.structTable.setItem(self.tableRow, 0, QTableWidgetItem(os.path.basename(struct)))
        self.saveButton.clicked.connect(self.save)
        self.tableRow+=1
        for i in range(len(self.mainwindow.creaters)):
            if str(self.mainwindow.creaters[i].base_name).strip()==str(self.structList.currentText()).strip():
                self.creaters.append(self.mainwindow.creaters[i])
                break

    def save(self):
        if self.creaters!=[]:
            if self.mergeType=="merge":
                display="合并结构"
                mergedStruct=self.creaters[0].merge(self.creaters)
            else:
                display="嵌套结构"
                mergedStruct=self.creaters[0].mergeWithPis(self.creaters)
            self.mainwindow.creaters.append(mergedStruct)
            self.mainwindow.displayTable.setItem(self.tableRow, 0, QTableWidgetItem(os.path.basename(mergedStruct.base_name)))
            self.mainwindow.displayTable.setItem(self.tableRow, 1, QTableWidgetItem(display))
            self.mainwindow.tableRow+=1

    def delstruct(self):
        self.ui.structTable.clear()
        self.creaters=[]

class moverPage(QWidget):
    def __init__(self,mainwindow):
        self.ax=None
        self.mover=None
        self.mainwindow=mainwindow
        super().__init__()
        self.ui=uic.loadUi("UI/mover.ui",self)
        self.points=[]
        self.creater_=None
        self.addButton.clicked.connect(self.addStruct)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.scene = QGraphicsScene(self)
        self.graph.setScene(self.scene)
        self.scene.addWidget(self.canvas)
        self.plot_3d(None)
        self.path=None
        self.enter.clicked.connect(self.addPoint)
        self.clearButton.clicked.connect(self.clearGraph)
        self.saveButton.clicked.connect(self.save)
        self.ax=None

    def save(self):
        if self.mover!=None:
            self.mover.savePath(self.path)
            self.mainwindow.creaters.append(self.mover)
            self.mainwindow.displayTable.setItem(self.mainwindow.tableRow, 0, QTableWidgetItem("movedStruct"))
            self.mainwindow.tableRow+=1
        else:
            QMessageBox.information(None, "报错", "你还没选择要移动的结构")

    def addPoint(self):
        print(self.points)
        try:
            x=float(self.setX.toPlainText())
            y=float(self.setY.toPlainText())
            z=float(self.setZ.toPlainText())
        except ValueError:
            return

        self.points.append([x,y,z])
        points=np.array(self.points)
        print(points)
        if len(self.points)>1:
            self.path=mover.genePath(points)
        print(self.path)
        self.plot_3d(self.path)
        self.setX.clear()
        self.setY.clear()
        self.setZ.clear()

    def plot_3d(self,path):
        if path==None:
            path=[[0],[0],[0]]
        self.ax = self.figure.add_subplot(111, projection='3d')

        self.ax.scatter(path[0], path[1], path[2], c='r', marker='o')
        self.ax.set_xlabel('X Label')
        self.ax.set_ylabel('Y Label')
        self.ax.set_zlabel('Z Label')
        self.ax.set_box_aspect([1, 1, 1])

        self.canvas.draw()

    def addStruct(self):
        for i in range(len(self.mainwindow.creaters)):
            if str(self.mainwindow.creaters[i].base_name).strip()==str(self.structList.currentText()).strip():
                self.creater_=self.mainwindow.creaters[i]
                break
        self.mover=mover(None,self.creater_,"movedStruct")
        print(self.mover.base_name+"aaaaaa")
    
    def clearGraph(self):
        self.points=[]
        if self.ax!=None:
            self.ax.cla()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window=window()
    window.show()

    sys.exit(app.exec_())
