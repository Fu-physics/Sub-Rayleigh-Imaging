
from __future__ import unicode_literals
import sys
import os
import random
import time

import numpy as np
import xarray as xr


from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QInputDialog, QPushButton, QMainWindow, QApplication, QSpinBox, QLabel
from PyQt5.QtWidgets import QWidget, QAction, QTabWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QGroupBox, QDialog, QGridLayout
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QFileDialog
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QFileDialog


import sys


import matplotlib
from mpl_toolkits.axes_grid1 import make_axes_locatable
# Make sure that we are using QT5BB
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
#plt.ion()
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib import cm


from scipy.stats import poisson
from statistics import mean
import seaborn as sns




#home made packages
from ThorlabsCamera import ThorlabsCamer, ReadData

from DataProcess import DataProcess

#from DataProcess import ReadData

#from MatplotlibEmbeddingQt5 import MyMplCanvas, MyStaticMplCanvas, MyDynamicMplCanvas



progname = os.path.basename(sys.argv[0])
progversion = "0.1"


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'PyQt5 tabs - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 1000
        self.height = 700

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = MyTableWidget(self)  # creat a Widgat.
        self.setCentralWidget(self.table_widget)  # set the Widget to be CentralWidget of QMainWindow.

        self.show()


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.fileName = ''

        self.layout = QVBoxLayout(self)  # create a Layout, which will be setted for self

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        # self.tabs.resize(800,600)

        self.tabs.addTab(self.tab1, "Auto-Image")  # Add tabs
        self.tabs.addTab(self.tab2, "Save Multi-frames")
        self.tabs.addTab(self.tab3, "Data Processing")

        self.layout.addWidget(self.tabs)  # Add tabs to widget

        self.setLayout(self.layout)

        self.initalUI_tab_1()
        self.initalUI_tab_2()
        self.initalUI_tab_3()

    def initalUI_tab_1(self):
        #################### Create Plot cavas widget ###################################################
        # Create first tab
        self.tab1_layout = QVBoxLayout(self)# create a Layout, which will be setted for tab_1

        self.tab1_layout_Up = QHBoxLayout(self)
        # left side of Table 1
        self.tab1_layout_L = QVBoxLayout(self)
        self.createGridLayout("Para setting panel")

        # show the info of setup
        self.infotextshow = QPlainTextEdit(self)
        self.infotextshow.insertPlainText("...")
        infobox = QVBoxLayout()
        infobox.addWidget(self.infotextshow)

        self.infotextGroupBox = QGroupBox("The experiment setup parameters: ")
        self.infotextGroupBox.setLayout(infobox)

        self.tab1_layout_L.addWidget(self.horizontalGroupBox)
        self.tab1_layout_L.addWidget(self.infotextGroupBox)


        ##   right side of Table 1
        self.tab1_layout_R = QVBoxLayout(self)

        self.plotUp = plt.figure("Background")
        axes_Up = self.plotUp.add_subplot(111)
        self.add_plotfigure(self.plotUp, self.tab1_layout_R)

        #self.axes_Up.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

        self.buttonPlotUp = QPushButton('Start Plot')  # Just some button connected to `plot` method
        self.buttonPlotUp.clicked.connect(self.SingleImagefun(axes_Up))
        self.tab1_layout_R.addWidget(self.buttonPlotUp)

        self.buttonStopPlotUp = QPushButton('Stop Plot')  # Just some button connected to `plot` method
        self.buttonStopPlotUp.clicked.connect(self.StopPlotUp)
        self.tab1_layout_R.addWidget(self.buttonStopPlotUp)

        self.tab1_layout_Up.addLayout(self.tab1_layout_L)
        # self.tab1_layout.addStretch()
        self.tab1_layout_Up.addLayout(self.tab1_layout_R)

        self.tab1_layout.addLayout(self.tab1_layout_Up)

        self.tab1.setLayout(self.tab1_layout)  # set tab1.layout to be the layout of tab_1

    def initalUI_tab_2(self):
        #################### Create Plot cavas widget ###################################################
        # Create first tab
        self.tab2_layout = QHBoxLayout(self)# create a Layout, which will be setted for tab_2

        # left side of Table 2
        self.tab2_layout_L = QHBoxLayout(self)


        self.SaveFrameLayout("SaveFrame panel")
        self.tab2_layout_L.addWidget(self.SaveFrameGroupBox)

        # right side of Table 2
        self.tab2_layout_R =QHBoxLayout(self)

            # show the databox of experiment
        self.datatextshow = QPlainTextEdit(self)
        self.datatextshow.insertPlainText("...")
        databox = QVBoxLayout()
        databox.addWidget(self.datatextshow)
        self.datatextGroupBox = QGroupBox("The experiment data info: ")
        self.datatextGroupBox.setLayout(databox)

            # add the note for experiment
        self.notetextshow = QPlainTextEdit(self)
        self.notetextshow.insertPlainText("")
        notebox = QVBoxLayout()
        notebox.addWidget(self.notetextshow)
        self.notetextGroupBox = QGroupBox("The experiment notes: ")
        self.notetextGroupBox.setLayout(notebox)


        self.tab2_layout_R.addWidget(self.datatextGroupBox)
        self.tab2_layout_R.addWidget(self.notetextGroupBox)

        self.tab2_layout.addLayout(self.tab2_layout_L)
        self.tab2_layout.addLayout(self.tab2_layout_R)


        self.tab2.setLayout(self.tab2_layout)  # set tab1.layout to be the layout of tab_1

    def initalUI_tab_3(self):
        #################### Create Plot cavas widget ###################################################
        # Create first tab
        self.tab3_layout = QHBoxLayout(self)# create a Layout, which will be setted for tab_1

        ######################   left side of Table 3
        self.tab3_layout_L = QVBoxLayout(self)

        self.buttonopenfile = QPushButton('Open File')  # Just some button connected to `plot` method
        self.buttonopenfile.clicked.connect(self.OpenFile)

        self.buttonPostProcess = QPushButton('Post Process Data')  # Just some button connected to `plot` method
        self.buttonPostProcess.clicked.connect(self.PostProcess)

        self.buttonCoherent = QPushButton('Coherent Plot')  # Just some button connected to `plot` method
        self.buttonCoherent.clicked.connect(self.CoherentPlot)



        self.tab3_layout_L.addWidget(self.buttonopenfile)
        self.tab3_layout_L.addWidget(self.buttonCoherent)

        self.tab3_layout_L.addWidget(self.buttonPostProcess)


        ########################  right side of Table 3
        self.tab3_layout_R = QVBoxLayout(self)

        ###### right top
        self.tab3_layout_R_top = QHBoxLayout(self)

        self.tab3_layout_R_top_L = QVBoxLayout(self)
        self.tab3_layout_R_top_R = QVBoxLayout(self)


        self.plotFirstOrd = plt.figure("First Order Imaging")
        #axesTopL = self.plotFirstOrd.add_subplot(111)
        self.add_plotfigure(self.plotFirstOrd, self.tab3_layout_R_top_L)

        self.buttonplotFirstOrd = QPushButton('First Order Imaging Plot')  # The button connected to `plot` method
        self.buttonplotFirstOrd.clicked.connect(self.PlotFirstOrdrfun(self.plotFirstOrd))
        self.tab3_layout_R_top_L.addWidget(self.buttonplotFirstOrd)


        self.plotHighOrd = plt.figure("High Order Imaging")
        #axesTopR = self.plotHighOrd.add_subplot(111)
        self.add_plotfigure(self.plotHighOrd, self.tab3_layout_R_top_R)

        self.buttonplotHighOrd = QPushButton('High Order Imaging Plot')  # The button connected to `plot` method
        self.buttonplotHighOrd.clicked.connect(self.PlotSecondOrdrfun(self.plotHighOrd))

        self.NOrder_spinbox = QSpinBox()
        self.NOrder_spinbox.setRange(2, 10)
        self.NOrder_spinbox.setValue(2)

        gridLayout_TopR = QGridLayout()
        gridLayout_TopR.addWidget(self.NOrder_spinbox,0,0)
        gridLayout_TopR.addWidget(self.buttonplotHighOrd, 0, 1)

        self.tab3_layout_R_top_R.addLayout(gridLayout_TopR)


        self.tab3_layout_R_top.addLayout(self.tab3_layout_R_top_L)
        self.tab3_layout_R_top.addLayout(self.tab3_layout_R_top_R)

        ####### right bottom
        self.tab3_layout_R_bot = QVBoxLayout(self)

        self.plotDistri = plt.figure("Distribution Plot")
        #axesBot = self.plotDistri.add_subplot(111)
        self.add_plotfigure(self.plotDistri, self.tab3_layout_R_bot)

        self.buttonplotDistri = QPushButton('Distribution Plot')  # Just some button connected to `plot` method
        self.buttonplotDistri.clicked.connect(self.PlotDistrifun(self.plotDistri))

        self.xpixel_spinbox = QSpinBox()
        self.xpixel_spinbox.setRange(0, 1280)
        self.xpixel_spinbox.setValue(1)

        self.ypixel_spinbox = QSpinBox()
        self.ypixel_spinbox.setRange(0, 1024)
        self.ypixel_spinbox.setValue(1)

        gridLayout_Bot = QGridLayout()
        gridLayout_Bot.addWidget(QLabel('X pixel'), 0, 0)
        gridLayout_Bot.addWidget(self.xpixel_spinbox,0,1)
        gridLayout_Bot.addWidget(QLabel('y pixel'), 0, 2)
        gridLayout_Bot.addWidget(self.ypixel_spinbox, 0, 3)
        gridLayout_Bot.addWidget(self.buttonplotDistri, 0, 4)

        self.tab3_layout_R_bot.addLayout(gridLayout_Bot)

        self.tab3_layout_R.addLayout(self.tab3_layout_R_top)
        self.tab3_layout_R.addLayout(self.tab3_layout_R_bot)

        self.tab3_layout.addLayout(self.tab3_layout_L)
        # self.tab3_layout.addStretch()
        self.tab3_layout.addLayout(self.tab3_layout_R)

        self.tab3.setLayout(self.tab3_layout)  # set tab1.layout to be the layout of tab_1


    def add_plotfigure(self, figureName, plot_layout):
        # self.figureName = plt.figure()                      # a figure instance to plot on
        # if put "plt.ion" on the head, which will make two more figures idependently.

        # this is the Canvas Widget that displays the `figure`, it takes the `figure` instance as a parameter to __init__
        canvas_figureName = FigureCanvas(figureName)
        toolbar_figureName = NavigationToolbar(canvas_figureName,
                                               self)  # this is the Navigation widget, it takes the Canvas widget and a parent

        plot_layout.addWidget(toolbar_figureName)  # this also needed to show the Navigation of plot
        plot_layout.addWidget(canvas_figureName)  # add Canvas Widget(plot widget) onto tab_2

    def createGridLayout(self, layout_name):
        self.horizontalGroupBox = QGroupBox(layout_name)
        layout = QGridLayout()
        # layout.setColumnStretch(1, 4)
        # layout.setColumnStretch(2, 4)

        self.ConnectCamera_bt = QPushButton('Connect Camera', self)
        self.ConnectCamera_bt.clicked.connect(self.ConnectCamera)

        self.cmos_para_bt = QPushButton('Set Camera', self)
        self.cmos_para_bt.clicked.connect(self.SetCamera)

        self.expose_spinbox = QSpinBox()
        self.expose_spinbox.setRange(1, 66000)
        self.expose_spinbox.setValue(1)

        self.xpixs_spinbox = QSpinBox()
        self.xpixs_spinbox.setRange(1, 1280)
        self.xpixs_spinbox.setValue(1280)

        self.xoffset_spinbox = QSpinBox()
        self.xoffset_spinbox.setRange(0, 1280)
        self.xoffset_spinbox.setValue(0)

        self.ypixs_spinbox = QSpinBox()
        self.ypixs_spinbox.setRange(1, 1024)
        self.ypixs_spinbox.setValue(1024)

        self.yoffset_spinbox = QSpinBox()
        self.yoffset_spinbox.setRange(0, 1024)
        self.yoffset_spinbox.setValue(0)

        layout.addWidget(QLabel('Expose time(us)'), 0, 0)
        layout.addWidget(self.expose_spinbox, 0, 1)

        layout.addWidget(QLabel('X pixels'), 1, 0)
        layout.addWidget(self.xpixs_spinbox, 1, 1)
        layout.addWidget(QLabel('X offset'), 1, 2)
        layout.addWidget(self.xoffset_spinbox, 1, 3)

        layout.addWidget(QLabel('Y pixels'), 2, 0)
        layout.addWidget(self.ypixs_spinbox, 2, 1)
        layout.addWidget(QLabel('Y offset'), 2, 2)
        layout.addWidget(self.yoffset_spinbox, 2, 3)


        layout.addWidget(self.ConnectCamera_bt, 5, 0)

        layout.addWidget(self.cmos_para_bt, 5, 1)
        self.horizontalGroupBox.setLayout(layout)


    def SaveFrameLayout(self, layout_name):
        self.SaveFrameGroupBox = QGroupBox(layout_name)
        layout = QGridLayout()

        self.cmos_run_bt = QPushButton('Run to Get Multi-Image Data', self)
        self.cmos_run_bt.clicked.connect(self.MultiImagefun)

        self.cmos_save_bt = QPushButton('Save Data', self)
        self.cmos_save_bt.clicked.connect(self.Savedata)

        self.FrameNumber_spinbox = QSpinBox()
        self.FrameNumber_spinbox.setRange(1, 100000)
        self.FrameNumber_spinbox.setValue(100)

        self.SegmentNumber_spinbox = QSpinBox()
        self.SegmentNumber_spinbox.setRange(1, 1000)
        self.SegmentNumber_spinbox.setValue(50)

        self.TotleTime_spinbox = QSpinBox()
        self.TotleTime_spinbox.setRange(0, 100)
        self.TotleTime_spinbox.setValue(0)


        layout.addWidget(QLabel('Frame Number'), 0, 0)
        layout.addWidget(self.FrameNumber_spinbox, 0, 1)

        layout.addWidget(QLabel('Segment Number'), 1, 0)
        layout.addWidget(self.SegmentNumber_spinbox, 1, 1)


        layout.addWidget(QLabel('Totle Time'), 2, 0)
        layout.addWidget(self.TotleTime_spinbox, 2, 1)

        layout.addWidget(self.cmos_run_bt, 3, 0)
        layout.addWidget(self.cmos_save_bt, 4, 0)

        self.SaveFrameGroupBox.setLayout(layout)

    def ConnectCamera(self):
        """
        connect the camera

        :return:
        """
        #try:
        self.Cam = ThorlabsCamer()
        self.Cam.ConnectCamera()
        self.infotextshow.appendPlainText("Camera connected!")

    def SetCamera(self):
        """
        set the camera parameters
        :return:
        """
        xshift = self.xoffset_spinbox.value()
        width = self.xpixs_spinbox.value()

        yshift = self.yoffset_spinbox.value()
        high =  self.ypixs_spinbox.value()

        exposeTime = self.expose_spinbox.value()
        #self.expose_spinbox.value()

        print("xshift, yshift, width , high, exposeTime", xshift, yshift, width, high, exposeTime)
        self.infotextshow.appendPlainText("xshift, yshift: (" + str(xshift) + "," + str(yshift) +")")
        self.infotextshow.appendPlainText("width, high: (" + str(width) + "," + str(high) +")")
        self.infotextshow.appendPlainText("exposeTime: " + str(exposeTime) + " us" )

        self.Cam.SetCamera(yshift = yshift, xshift = xshift, high = high, width = width, exposeTime = exposeTime)

    def SingleImagefun(self, ax):

        """
        1) get each frame and plot it
        2) auto-update the plot

        :param ax: plt.addsubplot(111)
        :return: auto-update the plot
        """

        def inner_SingleImage_fun():

            def update_data():
                #print("AutoFresh  the figure !")

                #print("begin to get SingleImageData data ... ")
                singledata = self.Cam.SingleImageData(self.infotextshow)
                #print("The image data shape is: ", np.shape(singledata))
                cax.set_data(singledata)

                #We need to draw *and* flush
                self.plotUp.canvas.draw()
                self.plotUp.canvas.flush_events()

            self.timer = QtCore.QTimer(self)
            #print("begin to plot !")
            self.infotextshow.appendPlainText("Plot start!")

            try:
                self.cbar.remove()
                #print("clear self.cbar !")
            except:
                pass
                #print("fail to clear self.cbar !")

            ax.cla()
            singledata = self.Cam.SingleImageData(self.infotextshow)
            cax = ax.imshow(singledata, interpolation='nearest')
            ax.set_title('CMOS Camera')
            self.cbar = self.plotUp.colorbar(cax, orientation='vertical')

            #cbar.ax.set_xticklabels(['Low', 'Medium', 'High'])  # horizontal colorbar
            self.timer.timeout.connect(update_data)
            self.timer.start(500)

        return inner_SingleImage_fun

    def StopPlotUp(self):
        """
        Stop the auto-plot
        """
        self.timer.stop()
        self.infotextshow.appendPlainText("Plot stop!")


    def MultiImagefun(self):
        """
        get the multi-fram image data, which are saved into *.npy files

        """

        frameNumber = self.FrameNumber_spinbox.value()
        segmentNumber = self.SegmentNumber_spinbox.value()
        print("frameNumber, segmentNumber is: ", frameNumber, segmentNumber)
        print("begin to get MultiImageData data ... ")
        self.Cam.MultiImageData(infoObj = self.datatextshow,  frame_number_expected = frameNumber, segment_frame = segmentNumber)


    def Savedata(self):

        """
        1, transfer *.npy to *.nc data, which includes the data dimension info and experiment notes
        2, delete *.npy file
        2, save the *.nc file
        """

        frameNumber = self.FrameNumber_spinbox.value()
        segmentNumber = self.SegmentNumber_spinbox.value()
        width = self.xpixs_spinbox.value()
        high =  self.ypixs_spinbox.value()
        print("frameNumber, segmentNumber, width, high is: ", frameNumber, segmentNumber, width, high)
        app = ReadData(noteObj = self.notetextshow, frameNumber=frameNumber, segmentFrame=segmentNumber, width=width, high=high)
        self.multiFrameData = app.ImageData()

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        # it just provides the name of file that you want to write into
        fileName, _= QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;NC Files (*.nc)", options=options)
        if fileName:
            print(fileName)

        self.multiFrameData.to_netcdf(fileName + '.nc')

        self.datatextshow.appendPlainText("the data has saved as .nc file! ")


    def OpenFile(self): 
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.nc)", options=options)
        if self.fileName:
            print(self.fileName)
        self.APP_dataprocess = DataProcess(self.fileName)



    def PlotFirstOrdrfun(self, fig):

        def inner_PlotFirstOrdrfun():

            # As self.firstOrdImaging will be used later, so we have to save as self.
            self.firstOrdImaging = self.APP_dataprocess.Average_Fluctuation() 

            
            #try:
            #    self.firstOrdImaging = self.APP_dataprocess.Average_Fluctuation()
            #    print(np.shape(self.firstOrdImaging))
            #except Exception:
            #    print("self.firstOrdImaging error!")

            # plot the Averge imaging
            ax = fig.add_subplot(111)

            try:
                self.cbar_FOrder.remove()
                ax.cla()
                #print("clear self.cbar !")
            except:
                pass
                #print("fail to clear self.cbar !")


            im = ax.imshow(self.firstOrdImaging)
            # create an axes on the right side of ax. The width of cax will be 5%
            # of ax and the padding between cax and ax will be fixed at 0.05 inch.
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.05)
            self.cbar_FOrder =  plt.colorbar(im, cax=cax)
            #plt.colorbar(im, cax=cax, ticks=[0, 5, 10])
            ax.set_title('1th Order')

            plt.savefig('1th Order Imaing.eps', format='eps', dpi=100)
            plt.close()
        
        return inner_PlotFirstOrdrfun



    def PlotSecondOrdrfun(self, fig):

        def inner_PlotSecondOrdrfun():
            NorderValue = self.NOrder_spinbox.value()

            #secondOrdImaging = self.APP_dataprocess.SecondOrder()
            print("The ", self.NOrder_spinbox.value(), "th Order Imaging")
            secondOrdImaging = self.APP_dataprocess.NOrder(NorderValue)
            print(np.shape(secondOrdImaging))
            
            #try:
            #    self.firstOrdImaging = self.APP_dataprocess.Average_Fluctuation()
            #    print(np.shape(self.firstOrdImaging))
            #except Exception:
            #    print("self.firstOrdImaging error!")
            # plot the Averge imaging

            ax = fig.add_subplot(111)

            try:
                self.cbar_NOrder.remove()
                ax.cla()
                #print("clear self.cbar !")
            except:
                pass
                #print("fail to clear self.cbar !")


            im = ax.imshow(secondOrdImaging)
            # create an axes on the right side of ax. The width of cax will be 5%
            # of ax and the padding between cax and ax will be fixed at 0.05 inch.
            divider = make_axes_locatable(ax)

            cax = divider.append_axes("right", size="5%", pad=0.05)
            self.cbar_NOrder = plt.colorbar(im, cax=cax)
            #plt.colorbar(im, cax=cax, ticks=[0, 5, 10])
            ax.set_title('{}th Order'.format(NorderValue))

            plt.savefig('2th Order Imaing.eps', format='eps', dpi=100)
            plt.close()
                    
        
        return inner_PlotSecondOrdrfun


    def PlotDistrifun(self, fig):

        def BoseEinstein(Nbar, n = 51):
            nList = np.linspace(0, n, n+1, dtype = int)
            result = 1/(1+Nbar)*(Nbar/(1+Nbar))**nList
            return result


        def G2(FirstArray1d, SecondArray1d):

            Frames = len(FirstArray1d)
            #print("Frames is: " , Frames)
            FirstAverage = np.sum(FirstArray1d)/Frames
            SecondAverage = np.sum(SecondArray1d)/Frames
            
            result = np.sum(FirstArray1d*SecondArray1d)/ Frames /(FirstAverage * SecondAverage)
            return result

        def inner_PlotDistrifun():

            """
            Plot the photon number distribution ...
            """
                    
            font = {'family': 'serif',
                    'color':  'darkred',
                    'weight': 'normal',
                    'size': 16}

            Nmax = 100
            bins = np.linspace(0, Nmax, Nmax+1)
            nList = np.linspace(0, Nmax, Nmax+1, dtype = int)

            y_location = self.ypixel_spinbox.value()
            x_location = self.xpixel_spinbox.value()

            # get pixel intensity data
            Array1 = self.APP_dataprocess.PixelData(y_location, x_location)
            Array2 = Array1
            g2 = G2(Array1, Array2)
            print("g2 is:", g2)

            arr = []
            rv = poisson(self.firstOrdImaging[y_location, x_location])
            for num in range(0,40):
                arr.append(rv.pmf(num))

            ax = fig.add_subplot(111)

            try:
                ax.cla()
                #print("clear self.cbar !")
            except:
                pass
                #print("fail to clear self.cbar !")
            
            ax.hist(Array1 , bins, normed=True, label = "Data distribution") 
            ax.plot(nList, BoseEinstein(self.firstOrdImaging[y_location, x_location], Nmax), label ="BoseEinstein distribution")
            ax.plot(arr, linewidth=2.0, label ="Possion distribution")
            ax.set_title("Pixel Position({},{}); <$I$>:{}".format(x_location , y_location, self.firstOrdImaging[y_location, x_location]), fontdict=font)
            
            ax.text(22, .08, r"g2:{}".format(g2), fontdict=font)
            ax.legend() 
            
            fig.savefig('PixelPosition({},{})PhotDist.eps'.format(x_location , y_location), format='eps', dpi=300)
            plt.close()

        return inner_PlotDistrifun


    def CoherentPlot(self):

        fig = plt.figure()
        ax = fig.add_subplot(111)

        xCorr, yCorr = self.APP_dataprocess.SpatialCorrelation([self.ypixel_spinbox.value(), self.xpixel_spinbox.value()])
        ax.plot(xCorr)
        ax.set_title("G2 @({}{})".format(self.ypixel_spinbox.value(), self.xpixel_spinbox.value()))
        fig.savefig("G2 @({}{}).eps".format(self.ypixel_spinbox.value(), self.xpixel_spinbox.value()), format="eps", dpi = 100)
        plt.show()

        
        
    def PostProcess(self):
        app = DataProcess()   # which read the data only
        app.PlotFrames()

        # calculated the first order which will be used at photon distribution, high order imaging, so do it firstly.
        # and plot it
        app.PlotFirstOdr()    

        app.PlotPhotonDistribution()

        app.PlotSecondOdr()


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())