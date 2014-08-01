
class Report:
  def __init__(self, doc_heading, column_headings, body):
    self.doc_heading = doc_heading
    self.column_headings = column_headings
    self.body = body
  
  def createReport(self):
    test = ""   #N.B. remove this line when you put in your code
    
  
    
  def average(self,array):
    return sum(array) * 1.0 / len(array)
    

  def stdDeviation(self,array):
    import math
    dev = 0.0
    sum2 = 0.0
    size = 0
    
    for s in array:
      sum2 += pow((s-self.average(array)), 2)
      size += 1
    dev = math.sqrt(sum2/(size-1))
    return dev
    
    
    
    
    #avg = self.average(array)
    #variance = map(lambda x: (x - avg)**2, s)
    
    #standard_deviation = math.sqrt(self.average(variance))
    #return standard_deviation
    
    
    
    
    
