
from ReportGenerator import ReportGenerator
from CSVReportGenerator import CSVReportGenerator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape
from reportlab.lib.pagesizes import A4

import csv

class PDFReportGenerator(ReportGenerator):
	def __init__(self):		#Constructor
		test = "" #N.B. Remove this line of code when you start


	csvGen = CSVReportGenerator()
	course_name = 'COS xxx'
	
	def generateAssessmentReport(self, module, assessment,response):  #Assessment Report
		report = self.csvGen.generateAssessmentReport(module, assessment)
		self.course_name = module
		c=self.create_report(report,response)
		return c

	def generateStudentMarksReport(self, module, studentNo, assessments,response):  #Student Marks Report
		report = self.csvGen.generateStudentMarksReport(module, studentNo, assessments)
		self.course_name = studentNo + ' ' + module
		c =self.create_report(report,response)
		return c

	def generateAuditReport(self, module, userID, alteredTable, dateFrom, dateTo,response):  #Audit Report
		report = self.csvGen.generateAuditReport( module, userID, alteredTable, dateFrom, dateTo)
		self.course_name = module + ' Audit Report'
		c =self.create_report(report,response)
		return c

	def create_report(self,report,response):
		pdf_name = self.course_name + ' Marksheet.pdf'
		fnt = 'Helvetica'
		sz = 12

		c = canvas.Canvas(response)
		c.setPageSize(A4)
		c.setFont(fnt, sz, leading=None)

		heighty = 720
		widthy = 100
		max_width = 800
		width_dec = 30


	#header text
		c.drawCentredString(110, 750, self.course_name + ' Marksheet')
		c.drawCentredString(800, 750, 'H')

	#tmp_data = csv.reader(open(report, "rb"))
		tmp_data = csv.reader(report)
		hdngs = next(tmp_data)
		num_cols = len(hdngs)

		if num_cols > 35:
			width_dec = 600/num_cols
			sz = 8
			c.setFont(fnt, sz, leading=None)
		elif num_cols > 20:
			width_dec = 600/num_cols
			sz = 10
			c.setFont(fnt, sz, leading=None)


	#print num_cols

	#marks_data = csv.reader(open(report, "rb"))
		marks_data = csv.reader(report)
		for row in marks_data:
			heighty -= 20
			c.drawCentredString(widthy, heighty, row[0])
			widthy += 70
			for k in range(1, num_cols):
				c.drawCentredString(widthy, heighty, row[k])
				widthy += width_dec
			widthy = 100
			if heighty <= 100:
				c.showPage()
				heighty = 750
				c.setFont(fnt, sz, leading=None)
		#save pdf page, use for each page
		c.showPage()
		#print 'created'
		c.save()
		return c