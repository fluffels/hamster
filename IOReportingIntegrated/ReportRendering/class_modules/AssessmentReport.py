import csv
from ReportRequest import ReportRequest
from Report import Report

#from reportlab.graphics.shapes import Drawing
#from reportlab.graphics.charts.barcharts import VerticalBarChart
#from reportlab.lib import colors

#from Report import Report

class AssessmentReport(Report):
	def __init__(self,name,headings,totals,data):
		self.reportName = name
		self.headings = headings
		self.data = data
		self.marks = []
		self.studentNumbers = []
		self.totalHeadings = len(self.headings)
		self.totals = totals
		self.averages = []
		self.averages.append(0)
		tmpArray = []
		count = 0
		i = 0
		
		while count < len(data) :
			#print data[count]
			j = len(data[count])
			row = []
			c = 0
			for col in data[count] :
				if c > 0 :
					row.append(col)
				else:
					self.studentNumbers.append(col)
				c += 1
			tmpArray.append(row)
			i += 1
			count += 1
		count = 0
		i = 0
		
		while count < len(tmpArray) :
			tmpArray2 = []
		    
			for row in tmpArray :
				cols = len(row)
				if i < cols :
					tmpArray2.append(row[i])
			    
			i += 1
			count += 1
			if not tmpArray2 :
				print ""
			else :
				self.marks.append(tmpArray2)
		
		# calculate average and stdDeviation for each column
		for col in self.marks :
			self.averages.append(self.average(col))
			#self.stdDeviations.append(self.stdDeviation(col))
		    
		print self.averages 
  
	def getName(self):
		return self.reportName
	def getHeadings(self):
		return self.headings
	def getData(self):
		return self.data
	def getStdDeviation(self):
		return self.stdDeviation(self.marks)
	def getAverage(self):
		return self.averages
	def getTotals(self):
		return self.totals
    #~ def getChart(self):
        #~ d = Drawing(300, 200)
        #~ chart = VerticalBarChart()
        #~ chart.width = 260
        #~ chart.height = 160
        #~ chart.x = 50
        #~ chart.y = 50
        #~ chart.height = 125
        #~ chart.width = 300
        #~ chart.strokeColor = colors.black
        #~ chart.valueAxis.valueMin = 0
        #~ chart.valueAxis.valueMax = 100
        #~ chart.valueAxis.valueStep = 10
        #~ chart.categoryAxis.labels.boxAnchor = 'ne'
        #~ chart.categoryAxis.labels.dx = 8
        #~ chart.categoryAxis.labels.dy = -2
        #~ chart.categoryAxis.labels.angle = 0
        #~ chart.data = self.marks
        #~ chart.categoryAxis.categoryNames = self.studentNumbers
        
        #~ d.add(chart)
        #~ #d.save(fnRoot='test', formats=['png', 'pdf'])
        #~ return d

  

  
