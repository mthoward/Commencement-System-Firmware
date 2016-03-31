import collections

class Queue_Class():
   def __init__(self):
      self.deque = collections.deque()
   
   def addToBottomOfQueue(self,data):
      self.deque.append(data)
      
   def RemoveFromTopOfQueue(self):
      if len(self.deque) < 1:
         print("Error")
      else:
         self.deque.popleft()



'''Example Usage'''
#deque = Queue_Class()   
#deque.addToBottomOfQueue("sethkara")
#deque.addToBottomOfQueue("mthoward")
#deque.addToBottomOfQueue("adbooth")

#print deque.deque
#deque.RemoveFromTopOfQueue()
#print deque.deque