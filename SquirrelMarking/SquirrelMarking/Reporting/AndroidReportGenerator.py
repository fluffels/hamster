from class_modules.ReportRequest import ReportRequest
from class_modules.ReportGenerator import ReportGenerator

class AndroidReportGenerator(ReportGenerator):
  def __init__(self, _request):		#Constructor
    self.reportRequest = _request
	
  def __init__(self,report):		#Constructor
    self.report = report
  
  
  def generateReport(self,report):		#This method overrides the one in its superclass
    #implementation goes here
	return report
