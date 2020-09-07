from Qt import QtWidgets,QtCore,QtGui
import pymel.core as pm
from maya import  cmds





class Gear(QtWidgets.QDialog):
    def __init__(self):
        super(Gear, self).__init__()
        self.setWindowTitle('Gear Creator')
        self.transform=None
        self.constructor=None
        self.extrude=None
        self.buildUI()

# UI Code
    def buildUI(self):
        layout=QtWidgets.QGridLayout(self)

        self.lineEdit=QtWidgets.QLineEdit(self)
        self.lineEdit.setMaximumWidth(30)
        self.lineEdit.returnPressed.connect(self.onPressed)
        layout.addWidget(self.lineEdit,4,0,1,2)



        self.label2=QtWidgets.QLabel(self)
        layout.addWidget(self.label2,1,3,1,2)

        createBtn=QtWidgets.QPushButton('Create Gear')
        createBtn.setMaximumWidth(70)
        createBtn.setMaximumHeight(30)
        createBtn.clicked.connect(self.createGear)
        layout.addWidget(createBtn,1,0)



        label=QtWidgets.QLabel(self)
        label.setText('Modify')
        layout.addWidget(label,2,0)

        self.slider=QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(10)
        self.slider.setMaximum(100)
        self.slider.setValue(10)
        self.slider.setMaximumWidth(90)
        self.slider.setMaximumHeight(30)
        self.slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider.setTickInterval(10)
        self.slider.valueChanged.connect(self.modifyGear)
        layout.addWidget(self.slider,3,0,1,1)

        self.scrollLayout=QtWidgets.QVBoxLayout(self)
        scroll=QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll,6,0,1,0)




    def onPressed(self):
        val=int(self.lineEdit.text())
        self.slider.setValue(val)



# Creating the gear teeth
    def createGear(self,teeth=20,length=0.5):
        spans=teeth*2

        self.transform,self.constructor=pm.polyPipe(subdivisionsAxis=spans)

        sidefaces=range(spans*2,spans*3,2)

        pm.select(clear=True)

        for face in sidefaces:
            pm.select('%s.f[%s]'%(self.transform,face),add=True)
        self.extrude = pm.polyExtrudeFacet(localTranslateZ=length)[0]



        siz = str(self.transform)
        self.label2.setText(siz)

        self.slider.setValue(10)
        self.lineEdit.clear()

# Modify the gear teeth
    def modifyGear(self, teeth=20,length=0.5):
        spans = teeth * 2
        pm.polyPipe(self.constructor,edit=True,subdivisionsAxis=spans)
        sidefaces = range(spans * 2, spans * 3, 2)

        faces=[]
        for face in sidefaces:

            face_count='f[%s]'%(face)
            faces.append(face_count)
        pm.setAttr('%s.inputComponents' % self.extrude, len(faces), *faces, type="componentList")

        pm.polyExtrudeFacet(self.extrude, edit=True, localTranslateZ=length)

        size=str(self.slider.value())
        self.lineEdit.setText(size)

def showUI():
    ui=Gear()
    ui.show()
    return ui

