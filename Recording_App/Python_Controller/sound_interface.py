import pyaudio
import wave
import os

### Constants
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 176400
RECORD_SECONDS = 3


## Record WAV file to UBIT_name.WAV
def record_wav_file(UBIT_name):  
   WAVE_OUTPUT_FILENAME = os.path.join(os.getcwd(), "../Recordings/" + str(UBIT_name) + ".wav")
   WAVE_OUTPUT_FILENAME = os.path.normpath(WAVE_OUTPUT_FILENAME)
   
   ## Create PyAudio Object
   p = pyaudio.PyAudio()
   stream = p.open(format=FORMAT,
                   channels=CHANNELS,
                   rate=RATE,
                   input=True,
                   frames_per_buffer=CHUNK)
   
   ## Create Frames Array
   frames = []
   
   for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
      data = stream.read(CHUNK)
      frames.append(data)
      
   stream.stop_stream()
   stream.close()
   p.terminate()

   ## Write Frames to WAV File
   wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
   wf.setnchannels(CHANNELS)
   wf.setsampwidth(p.get_sample_size(FORMAT))
   wf.setframerate(RATE)
   wf.writeframes(b''.join(frames))
   wf.close()
      
   
## Play 'UBIT_name.WAV'
def play_wav_file(file):
   ## Open Filename
   filename = os.path.join(os.getcwd(), "../Recordings/" + file)
   filename = os.path.normpath(filename)
   wf = wave.open(filename, 'rb')
   
   ## Create PyAudio Object
   p = pyaudio.PyAudio()
   stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                        channels = wf.getnchannels(),
                        rate = wf.getframerate(),
                        output = True
   )

   ## Play WAV File
   data = wf.readframes(CHUNK)
   while data != '':
      stream.write(data)
      data = wf.readframes(CHUNK)