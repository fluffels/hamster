class StudentMarksReport:

	def __init__(self,name,headings,totals,data):

		self.name = name
		self.headings = headings
		self.totals = totals
		self.data = data
		

	def getReportName(self):
		return self.name

	def getHeadings(self):
		return self.headings

	def getData(self):
		return self.data
		
	def getTotals(self):
		return self.totals




