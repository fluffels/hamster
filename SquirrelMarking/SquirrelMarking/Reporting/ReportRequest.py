#Below is a class that contains details of a report request

class ReportRequest:
  def __init__(self, _personDetail, _assessment, _task, _outputType):
    self.personDetail = _personDetail 		#Array of two elements. First one indicates whether this is a student or lecturer, second one has their personnel id.
    self.assessment = _assessment 		#Array with 2 elements, for the different levels of granularity. E.g. ('Semester Test, 1') or ('Practical', '9')
    self.task = _task 				#A string representing the task a user wants to do. E.g. Student Marks Report, Assessment Report, Audit Report 
    self.outputType = _outputType		#A string specifying output document. E.g. CSV, PDF, etc
    
  