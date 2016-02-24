import sys
import threading
import atexit 
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

# class taken from the SciPy 2015 Vispy talk opening example 
# see https://github.com/vispy/vispy/pull/928
class MyList(QtGui.QListWidget):
    def __init__(self):
        QtGui.QListWidget.__init__(self)

    def addToList(self, item):   
        self.addItem(item)

    #def item_click(self, item):
     #  print item, str(item.text())

class MicrophoneRecorder(object):
    def __init__(self, rate=4000, chunksize=1024):
        self.rate = rate
        self.chunksize = chunksize
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.chunksize,
                                  stream_callback=self.new_frame)
        self.lock = threading.Lock()
        self.stop = False
        self.frames = []
        atexit.register(self.close)

    def new_frame(self, data, frame_count, time_info, status):
        data = np.fromstring(data, 'int16')
        with self.lock:
            self.frames.append(data)
            if self.stop:
                return None, pyaudio.paComplete
        return None, pyaudio.paContinue
    
    def get_frames(self):
        with self.lock:
            frames = self.frames
            self.frames = []
            return frames
    
    def start(self):
        self.stream.start_stream()

    def close(self):
        with self.lock:
            self.stop = True
        self.stream.close()
        self.p.terminate()


class MplFigure(object):
    def __init__(self, parent):
        self.figure = plt.figure(facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, parent)

class RecordingWidget(QtGui.QWidget):
    
    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        # customize the UI
        self.initUI()
        
        # init class data
        self.initData()       
        
        # connect slots
        self.connectSlots()
        
        # init MPL widget
        self.initMplWidget()
        

    def initUI(self):
        ##########################################
        #  _______    _____________              #
        # | list  |  |__show_name__|             #
        # |       |   _____   _________   _____  #
        # |       |  |_rec_| |___bar___| |_ply_| #
        # |       |   _________________________  #
        # |       |  |        waveform         | #
        # |_______|  |_________________________| #
        #                                        #
        ##########################################
        displayVbox = QtGui.QVBoxLayout()
        
        ### Show Name
        showNameBox = QtGui.QHBoxLayout()
        showNameLabel = QtGui.QLabel("Name Selected")
        showNameDisplay = QtGui.QHBoxLayout()
        self.showName = QtGui.QLabel("Select From List")
        showNameDisplay.addWidget(self.showName)
        showNameBox.addWidget(showNameLabel)
        showNameBox.addLayout(showNameDisplay)
        
        ### Buttons
        buttonBox = QtGui.QHBoxLayout()
        self.buttonRec = QtGui.QPushButton()
        self.buttonRec.setText("REC")
        self.buttonRec.clicked.connect(self.beginRec)
        
        self.buttonPlay = QtGui.QPushButton()
        self.buttonPlay.setText("PLAY")
        self.buttonPlay.clicked.connect(self.playback)
        
        buttonBox.addWidget(self.buttonRec)
        buttonBox.addWidget(self.buttonPlay)
        
        ### Add Name and Buttons to Layout
        displayVbox.addLayout(showNameBox)
        displayVbox.addLayout(buttonBox)

        ### PLOTS
        self.main_figure = MplFigure(self)
        displayVbox.addWidget(self.main_figure.toolbar)
        displayVbox.addWidget(self.main_figure.canvas)
        
        ### LIST
        listbox = QtGui.QVBoxLayout()
        listLabel = QtGui.QLabel('UBIT Names')
        self.list = MyList()
        listbox.addWidget(listLabel)
        listbox.addWidget(self.list)
        
        FrameBox = QtGui.QHBoxLayout()
        FrameBox.addLayout(listbox)
        FrameBox.addLayout(displayVbox)
        
        self.setLayout(FrameBox) 
        self.setGeometry(300, 300, 750, 700)
        self.setWindowTitle('Recording App')    
        self.show()
        
        
        # timer for calls, taken from:
        # http://ralsina.me/weblog/posts/BB974.html
        timer = QtCore.QTimer()
        timer.timeout.connect(self.handleNewData)
        timer.start(50)
        # keep reference to timer        
        self.timer = timer
        
    def beginRec(self):
        self.showName.setText("CHANGED")
                
    def playback(self):
        rec = MicrophoneRecorder()
    
    def initData(self):
        mic = MicrophoneRecorder()
        mic.start()  

        # keeps reference to mic        
        self.mic = mic
        
        # computes the parameters that will be used during plotting
        self.freq_vect = np.fft.rfftfreq(mic.chunksize, 
                                         1./mic.rate)
        self.time_vect = np.arange(mic.chunksize, dtype=np.float32) / mic.rate * 1000
                
    def connectSlots(self):
        pass
    
    def initMplWidget(self):
        """creates initial matplotlib plots in the main window and keeps 
        references for further use"""
        # top plot
        self.ax_top = self.main_figure.figure.add_subplot(211)
        self.ax_top.set_ylim(-2000, 2000)
        self.ax_top.set_xlim(0, self.time_vect.max())
        self.ax_top.set_xlabel(u'time (ms)', fontsize=6)

        # # bottom plot
        # self.ax_bottom = self.main_figure.figure.add_subplot(212)
        # self.ax_bottom.set_ylim(0, 1)
        # self.ax_bottom.set_xlim(0, self.freq_vect.max())
        # self.ax_bottom.set_xlabel(u'frequency (Hz)', fontsize=6)
        # line objects        
        self.line_top, = self.ax_top.plot(self.time_vect, 
                                         np.ones_like(self.time_vect))
        
        # self.line_bottom, = self.ax_bottom.plot(self.freq_vect,
                                               # np.ones_like(self.freq_vect))
                                               
                                               
        # tight layout
        #plt.tight_layout()
                                               
    def handleNewData(self):
        """ handles the asynchroneously collected sound chunks """        
        # gets the latest frames        
        frames = self.mic.get_frames()
        
        if len(frames) > 0:
            # keeps only the last frame
            current_frame = frames[-1]
            # plots the time signal
            self.line_top.set_data(self.time_vect, current_frame)
            # computes and plots the fft signal            
            # fft_frame = np.fft.rfft(current_frame)
            # #if self.autoGainCheckBox.checkState() == QtCore.Qt.Checked:
            # fft_frame /= np.abs(fft_frame).max()
            # #else:
            # #    fft_frame *= (1 + self.fixedGainSlider.value()) / 5000000.
                # #print(np.abs(fft_frame).max())
            #self.line_bottom.set_data(self.freq_vect, np.abs(fft_frame))            
            
            # refreshes the plots
            self.main_figure.canvas.draw()

            
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = RecordingWidget()

    ubit = QtGui.QListWidgetItem("sethkara")
    window.list.addToList(ubit)

    sys.exit(app.exec_())