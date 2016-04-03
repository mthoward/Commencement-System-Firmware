import socket
import time
import struct
import threading
import binascii
'''
sudo iptables -A INPUT -p udp --dport 15555 -j ACCEPT
sudo iptables -A INPUT -p udp --dport 15556 -j ACCEPT

Types of Messages:
   scanner to releaser - UBIT             <= MESS_ID = 0x0001
   releaser to scanner = acknowledgement  <= MESS_ID = 0x0010
   both - still connected?                <= MESS_ID = 0x0100
   both - response                        <= MESS_ID = 0x1000
'''

class UDP_Class():
   ### Home Testing - Lenovo
   def __init__(self, other_Pi_IP = '192.168.1.6',
                      other_Pi_Port = 15555,
                      localIP = '192.168.1.151',
                      localPort = 15556,
                      socketTimeout = 100):
   ### Home Testing - Server
   # def __init__(self, other_Pi_IP = '192.168.1.151',
                      # other_Pi_Port = 15556,
                      # localIP = '192.168.1.6',
                      # localPort = 15555,
                      # socketTimeout = 100):
   # ### Releaser Pi
   # def __init__(self, other_Pi_IP = '169.254.199.241',
                      # other_Pi_Port = 15556,
                      # localIP = '169.254.104.90',
                      # localPort = 15555,
                      # socketTimeout = 100):
   # ### Scanner Pi
   # def __init__(self, other_Pi_IP = '169.254.104.90',
                      # other_Pi_Port = 15555,
                      # localIP = '169.254.199.241',
                      # localPort = 15556,
                      # socketTimeout = 100):
      # Set UDP port and IP
      self.OTHER_PI_IP_ADDRESS = other_Pi_IP
      self.OTHER_PI_PORT = other_Pi_Port
      self.LOCAL_IP_ADDRESS = localIP
      self.LOCAL_PORT = localPort
    
      self.UBIT_SCANNED_MESS    = int("0001",16)
      self.UBIT_RESPONSE_MESS   = int("0010",16)
      self.STATUS_REQUEST_MESS  = int("0100",16)
      self.STATUS_RESPONSE_MESS = int("1000",16)
      
      self.CONNECTION = 0
      self.RCV_UBIT_FLAG = 0
      self.RCV_UBIT_BUFFER = ""
      self.UBIT_INCOMING_BUFFER = ""
      self.RCV_UBIT_FLAG_LOCK = threading.Lock()
      self.RCV_UBIT_BUFFER_LOCK = threading.Lock()
    
      # Sets internal socket timeout
      self.socketTimeout = socketTimeout

      # Initiate UDP receive and send sockets
      self.mainSocket = None
      self.sendSocket = None
      self.connectUDPSockets()

      self.UB_HEADER = [int("A1BA", 16),
                        int("F00D", 16), 
                        int("FEED", 16), 
                        int("BEEF", 16),
                        int("ABCD", 16),
                        int("0000", 16),
                        int("0000", 16),
                        int("0000", 16)]
      
      self.NUM_ALL_HEADER_WORDS = len(self.UB_HEADER)

 
   def connectUDPSockets(self):
      ##### Open my socket ####
      print "Opening UDP Socket..."
      self.mainSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      # Bind to my port/IP
      self.mainSocket.bind((self.LOCAL_IP_ADDRESS, self.LOCAL_PORT))
      # Setup my receive buffer
      self.mainSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1048576)
      # Set the asynchronous timeout to 100 seconds
      self.mainSocket.settimeout(self.socketTimeout)
      self.sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      print "Opened UDP Socket."
   
   
   ##########################
   ### ADD PROGRAM HEADER ###
   ##########################
   def addHeader(self, messageBody):
      packetHeader = [int("A1BA", 16),
                      int("F00D", 16), 
                      int("FEED", 16), 
                      int("BEEF", 16),
                      int("ABCD", 16),
                      int("0000", 16),
                      int("0000", 16),
                      int("0000", 16)]
      packetHeader.extend(messageBody)
      return packetHeader

   ### CONVERT STR to INT  ###
   def convertAsciiToInt(self, messageBody):
      int_messageBody = []
      double_char_array = []
      if len(messageBody)%2 == 1:
         messageBody = messageBody + " "
      for x in range(0, len(messageBody), 2):
         double_char_array.append(messageBody[x]+messageBody[x+1])
      for x in range(0, len(double_char_array)):
         int_messageBody.append(int(double_char_array[x].encode("hex"),16))
      return int_messageBody

   ### Creates array of type 'unsigned short' for sending over ethernet      
   def packageUpMessage(self, message):
      msgWordCount = len(message)
      structEncoding = "!" + str(msgWordCount) + "H" 
      packedString = struct.pack(structEncoding, *(message))
      return packedString
   
   ### Send a payload 
   def sendMessage(self, payload, messageType):
      int_payload = self.convertAsciiToInt(payload)
      totalMessage = self.addHeader(int_payload)                                                # Add Header
      totalMessage[7] = messageType
      packagedMessage = self.packageUpMessage(totalMessage)                                     # Create unsigned short array
      self.mainSocket.sendto(packagedMessage, (self.OTHER_PI_IP_ADDRESS, self.OTHER_PI_PORT))   # Send
     
   def receiveMessage(self):
      stop = 0
      while (stop == 0):
         try:
            # Read from the socket
            data, addr = self.mainSocket.recvfrom(2048)
            if len(data) > self.NUM_ALL_HEADER_WORDS*2:
               headerWords = struct.unpack("!"+str(self.NUM_ALL_HEADER_WORDS)+"H", data[0:self.NUM_ALL_HEADER_WORDS*2])	 
               # Check an ethernet header word
               if (format(headerWords[0], '04X') == format(self.UB_HEADER[0], '04X')):
                  '''UBIT_SCANNED_MESS'''
                  if int((format(headerWords[7], '04X')),16) == self.UBIT_SCANNED_MESS:
                     payload = struct.unpack("!"+str(len(data)/2 - self.NUM_ALL_HEADER_WORDS)+"H", data[self.NUM_ALL_HEADER_WORDS*2:])
                     message = ''
                     for i in range(0,len(payload)):
                        hex = format(payload[i], '04X')
                        message = message + (str(hex.decode("hex")))
                     #print "scanned ubit: ",message
                     self.RCV_UBIT_FLAG_LOCK.acquire()
                     self.RCV_UBIT_FLAG = 1
                     self.RCV_UBIT_FLAG_LOCK.release()
                     self.RCV_UBIT_BUFFER_LOCK.acquire()
                     self.RCV_UBIT_BUFFER = message
                     self.RCV_UBIT_BUFFER_LOCK.release()
                     self.sendMessage("Received Successfully", self.UBIT_RESPONSE_MESS)
                  
                  '''UBIT_RESPONSE_MESS'''
                  if int((format(headerWords[7], '04X')),16) == self.UBIT_RESPONSE_MESS:  
                     self.RECEIVED_UBIT = 1
                     payload = struct.unpack("!"+str(len(data)/2 - self.NUM_ALL_HEADER_WORDS)+"H", data[self.NUM_ALL_HEADER_WORDS*2:])
                     message = ''
                     for i in range(0,len(payload)):
                        hex = format(payload[i], '04X')
                        message = message + (str(hex.decode("hex")))
                     print message
                  
                  '''STATUS_REQUEST_MESS'''
                  if int((format(headerWords[7], '04X')),16) == self.STATUS_REQUEST_MESS:
                     self.sendMessage("I'm Alive...", self.STATUS_RESPONSE_MESS)
                  
                  '''STATUS_RESPONSE_MESS'''
                  if int((format(headerWords[7], '04X')),16) == self.STATUS_RESPONSE_MESS:
                     self.CONNECTION = 1
             
         except:
           print "timeout or error..."
   
   def checkConnection(self):
      while(1):
         self.CONNECTION = 0
         self.sendMessage("Are you Alive", self.STATUS_REQUEST_MESS)
         seconds = 0
         while(self.CONNECTION == 0):
            time.sleep(1.0)
            seconds = seconds + 1
            if seconds == 3:
               print "No Connection!"
               seconds = 0
               break;
         time.sleep(2)
   
   def UBIT_Recieved_Confirmation(self, timeout):
      seconds = 0
      while(self.RECEIVED_UBIT == 0):
         time.sleep(1.0)
         seconds = seconds + 1
         if(seconds>timeout):
            print "Timeout Error"
      time.sleep(2)

   
   def listenForMessages(self):
      self.listenThread = threading.Thread(target=self.receiveMessage)
      self.listenThread.daemon = True
      self.listenThread.start()
      
   def check_Connection(self):
      self.statusThread = threading.Thread(target=self.checkConnection)
      self.statusThread.daemon = True
      self.statusThread.start()
