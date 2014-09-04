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



def generate_student_mark_pdf(marks, module):
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
    writePoint = 750
    ass2 = marks[0][0]
    print "ass2-------------------: " + str(ass2[1]) +' '+ str(ass2[4]) +' '+ str(ass2[5]) +' '+ str(ass2[6])
    data = [['Assessment','Final Mark','Mark obtained', 'Percentage'],
            [str(ass2[1]), str(ass2[4]), str(ass2[5]), str(ass2[6])]]
    table = Table(data, colWidths=None, rowHeights=None)
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

def generate_student_mark_csv(marks,module):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Marks.csv"'
    
    ass2 = marks[0][0]
    print "ass2-------------------: " + str(ass2[1]) +' '+ str(ass2[4]) +' '+ str(ass2[5]) +' '+ str(ass2[6])

    writer = csv.writer(response)
    writer.writerow(['Student','u10534505'])
    writer.writerow(['Module',module])
    writer.writerow(['Assessment','Final Mark','Mark obtained', 'Percentage'])
    writer.writerow([str(ass2[1]), str(ass2[4]), str(ass2[5]), str(ass2[6])])

    return response