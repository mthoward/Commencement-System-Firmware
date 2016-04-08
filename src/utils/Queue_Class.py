import collections

class Queue_Class():
   def __init__(self):
      self.deque = collections.deque()
   
   def addToBottomOfQueue(self,data):
      if self.AlreadyExists(data) == False:	
      	 self.deque.append(data)
      
   def removeFromTopOfQueue(self):
      if len(self.deque) < 1:
         raise KeyError
      else:
         return self.deque.popleft()

   def AlreadyExists(self, data):
      for item in self.deque:
         if item == data:
	    return True
      return False


'''Example Usage'''
#deque = Queue_Class()   
#deque.addToBottomOfQueue("sethkara")
#deque.addToBottomOfQueue("sethkara")
#deque.addToBottomOfQueue("sethkara")
#deque.addToBottomOfQueue("mthoward")
#deque.addToBottomOfQueue("adbooth")

#print deque.deque
#deque.RemoveFromTopOfQueue()
#print deque.deque