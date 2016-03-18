import socket
import struct
import threading
import binascii

#sudo iptables -A INPUT -p udp --dport 15555 -j ACCEPT
#sudo iptables -A INPUT -p udp --dport 15556 -j ACCEPT

class UDP_Class():
   def __init__(self, other_Pi_IP = '169.254.104.90',
                      other_Pi_Port = 15555,
                      localIP = '169.254.199.241',
                      localPort = 15556,
                      socketTimeout = 100):
      # Set UDP port and IP
      self.OTHER_PI_IP_ADDRESS = other_Pi_IP
      self.OTHER_PI_PORT = other_Pi_Port
      self.LOCAL_IP_ADDRESS = localIP
      self.LOCAL_PORT = localPort
    
      # Sets internal socket timeout
      self.socketTimeout = socketTimeout

      # Initiate UDP receive and send sockets
      self.mainSocket = None
      self.sendSocket = None
      self.connectUDPSockets()

      self.UB_HEADER = [int("0000", 16),
                        int("0000", 16), 
                        int("0000", 16), 
                        int("F00D", 16),
                        int("BEEF", 16),
                        int("A1BA", 16),
                        int("FEED", 16),
                        int("ABCD", 16)]
      
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
      packetHeader = [int("0000", 16),
                      int("0000", 16),
                      int("0000", 16),
                      int("F00D", 16),
                      int("BEEF", 16),
                      int("A1BA", 16),
                      int("FEED", 16),
                      int("ABCD", 16)]
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
   def sendMessage(self, payload):
      int_payload = self.convertAsciiToInt(payload)
      totalMessage = self.addHeader(int_payload)                                                # Add Header
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
               if (format(headerWords[4], '04X') == format(self.UB_HEADER[4], '04X')):
                  payload = struct.unpack("!"+str(len(data)/2 - self.NUM_ALL_HEADER_WORDS)+"H", data[self.NUM_ALL_HEADER_WORDS*2:])
                  message = ''
                  for i in range(0,len(payload)):
                     hex = format(payload[i], '04X')
                     message = message + (str(hex.decode("hex")))
                  #self.mainSocket.sendto(data, (self.OTHER_PI_IP_ADDRESS, self.OTHER_PI_PORT))
                  print message
         except:
           print "listening..."
            
   def listenForMessages(self):
      self.listenThread = threading.Thread(target=self.receiveMessage)
      self.listenThread.start()
