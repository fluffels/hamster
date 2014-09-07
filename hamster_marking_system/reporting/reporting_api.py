from io import BytesIO
import csv
import json

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.pagesizes import portrait
from reportlab.platypus import Image #Might need to add images to the document
from reportlab.platypus import Table, TableStyle

from django.http import HttpResponse
from django.shortcuts import render



class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'



def generate_student_mark_pdf(data, student):
    """
    Generates a PDF document with a student's  marks,
    then allowes for it to be downloaded by the student.
    
    Arguments
    Mraks : An associative array of marks for a student
    module : The module the marks are for
    """
    
    #Extract student information to paint onto the document
    for ass in marks:
        print "--: " + str(ass)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename= Marks.pdf'
    
    buffer = BytesIO()
    
    # Create the PDF object, using the BytesIO object as its "file."
    c = canvas.Canvas(buffer)
    
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    c.setFont("Helvetica-Bold",24,leading=None)
    c.drawCentredString(300, 750, "Student : u10534505")
    c.setFont("Helvetica",24,leading=None)
    c.drawCentredString(300, 700, "Module : " + module)
    c.setFont("Helvetica", 18, leading=None)
    #print "ass2-------------------: " + str(ass2[1]) +' '+ str(ass2[4]) +' '+ str(ass2[5]) +' '+ str(ass2[6])
    #data = [['Assessment','Final Mark','Mark obtained', 'Percentage'],
    #        [str(ass2[1]), str(ass2[4]), str(ass2[5]), str(ass2[6])]]
    #table = Table(data, colWidths=None, rowHeights=None)
    #table.setStyle(TableStyle([('GRID',(0,0), (1,-1),2)]))
    #t=Table(data, colWidths=100, rowHeights=50)
    table.wrapOn(c,300, 650)
    table.drawOn(c,250,600)
        
    
    # Close the PDF object cleanly.
    c.showPage()
    c.save()
    
    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def generate_student_mark_csv(data,student):
    module = data[0]['assessment'][0]
    filename = student + "_" + module + "_marks.csv"
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    
    #Extract user information
    
    writer = csv.writer(response)
    writer.writerow(['Student',student])
    writer.writerow(['Module',module])
    writer.writerow(['Assessment', 'Mark obtained', 'Total Mark', 'Percentage'])
    for mark in data[0]['assessment'][1:]:
        assessment_name = mark[0]
        assessment_obtained_mark = mark[1]
        assessment_total_mark = mark[2]
        assessment_percenatge_obtained = '{0:.3g}'.format(mark[3])
        writer.writerow([assessment_name, assessment_obtained_mark, assessment_total_mark, assessment_percenatge_obtained])

    return response