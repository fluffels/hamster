from io import BytesIO
import csv
import json
import os

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.pagesizes import portrait
from reportlab.lib.units import cm, mm, inch
from reportlab.platypus import Image #Might need to add images to the document
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from django.http import HttpResponse
from django.shortcuts import render

styles = getSampleStyleSheet()

def generate_assessment_report(assess_name, full_marks, module, data, freq, student_list):
    filename = assess_name + "_"+module+"_report.pdf"
    logo = os.path.join(os.path.dirname(os.path.abspath(__file__)),"static/reporting/images/cs_header_image.jpg")
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename='+ filename
    
    buffer = BytesIO()
    
    # Create the PDF object, using the BytesIO object as its "file."
    c = canvas.Canvas(buffer)
    
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    c.setFont("Times-Roman",14,leading=None)
    c.drawString(30,750,"Assessment : " + assess_name)
    c.drawString(30,725,"Module : " + module)
    c.drawString(30,700,"Full Marks : " + str(full_marks))
    
    #Add image on the top right of document
    c.drawImage(logo, 400, 710, width=2.5*inch, height=1.0*inch)
    
    c.setFont("Helvetica-Bold", 12, leading=None)
    styleN = styles['Normal']
    
    tdata = [[Paragraph('<b>' + 'Statistics' + '</b>',styleN)
            ]]
    table = Table(tdata, colWidths=None, rowHeights=None)
    table.setStyle(TableStyle([
                                ('GRID',(0,0), (-1,0),1, colors.black),
                                ('BACKGROUND',(0,0),(-1,-1),colors.gray)#Give total a grey background
                              ]))
    table._argW[0]=7.0*inch
    table.wrapOn(c,100, 710)
    table.drawOn(c,50, 600)
    
    tdata = [[Paragraph('<b>Class Average</b>',styleN),
              Paragraph('<b>Median</b>',styleN),
              Paragraph('<b>Mode</b>',styleN),
              Paragraph('<b>Standard Deviation</b>',styleN)
            ]]
    table = Table(tdata, colWidths=None, rowHeights=None)
    table.setStyle(TableStyle([
                                ('GRID',(0,0), (-1,-1),1, colors.black)
                              ]))
    table._argW[0]=2.5*inch #Set the size(width) of the first collumn in the table
    table._argW[1]=1.5*inch
    table._argW[2]=1.5*inch
    table._argW[3]=1.5*inch
    
    #table=Table(tdata, colWidths=80, rowHeights=30)
    table.wrapOn(c,100, 650)
    table.drawOn(c,50,550)
    currPos = 550
    
    
    tdata = [data[0], data[1], data[2], data[3]],
    table = Table(tdata, colWidths=None, rowHeights=None)
    table.setStyle(TableStyle([
                                ('GRID',(0,0), (-1,-1),1, colors.black)
                              ]))
    #table=Table(tdata, colWidths=80, rowHeights=30)
    table._argW[0]=2.5*inch #Set the size(width) of the first collumn in the table
    table._argW[1]=1.5*inch
    table._argW[2]=1.5*inch
    table._argW[3]=1.5*inch
    table.wrapOn(c,75, 550)
    currPos -= 20
    table.drawOn(c,50, currPos)
    
    
    tdata = [[Paragraph('<b>' + 'Frequency Analysis' + '</b>',styleN)
            ]]
    table = Table(tdata, colWidths=None, rowHeights=None)
    table.setStyle(TableStyle([
                                ('GRID',(0,0), (-1,0),1, colors.black),
                                ('BACKGROUND',(0,0),(-1,-1),colors.gray)#Give total a grey background)
                              ]))
    table._argW[0]=7.0*inch
    table.wrapOn(c,100, currPos + 50)
    currPos -= 50
    table.drawOn(c,50, currPos)
    
    currPos -= 30
    tdata = [[Paragraph('<b>[0 .. 40)</b>',styleN),
              Paragraph('<b>[40 .. 50)</b>',styleN),
              Paragraph('<b>[50 .. 60)</b>',styleN),
              Paragraph('<b>[60 .. 75)</b>',styleN),
              Paragraph('<b>[75 .. 100]</b>',styleN)
            ]]
    table = Table(tdata, colWidths=None, rowHeights=None)
    table.setStyle(TableStyle([
                                ('GRID',(0,0), (-1,-1),1, colors.black)
                              ]))
    table._argW[0]=1.4*inch #Set the size(width) of the first column in the table
    table._argW[1]=1.4*inch
    table._argW[2]=1.4*inch
    table._argW[3]=1.4*inch
    table._argW[4]=1.4*inch
    
    #table=Table(tdata, colWidths=80, rowHeights=30)
    table.wrapOn(c,100, currPos)
    currPos -=20
    table.drawOn(c,50, currPos)
    
    tdata = [freq[0], freq[1], freq[2], freq[3], freq[4]],
    table = Table(tdata, colWidths=None, rowHeights=None)
    table.setStyle(TableStyle([
                                ('GRID',(0,0), (-1,-1),1, colors.black)
                              ]))
    #table=Table(tdata, colWidths=80, rowHeights=30)
    table._argW[0]=1.4*inch #Set the size(width) of the first collumn in the table
    table._argW[1]=1.4*inch
    table._argW[2]=1.4*inch
    table._argW[3]=1.4*inch
    table._argW[4]=1.4*inch
    
    table.wrapOn(c,75, currPos)
    currPos -= 20
    table.drawOn(c,50, currPos)
    
    tdata = [[Paragraph('<b>' + 'Students Information' + '</b>',styleN)]]
    table = Table(tdata, colWidths=None, rowHeights=None)
    table.setStyle(TableStyle([
                                ('GRID',(0,0), (-1,0),1, colors.black),
                                ('BACKGROUND',(0,0),(-1,-1),colors.gray)#Give total a grey background)
                              ]))
    table._argW[0]=7.0*inch
    table.wrapOn(c,100, currPos + 50)
    currPos -= 50
    table.drawOn(c,50, currPos)
    
    currPos -= 30
    tdata = [[Paragraph('<b>Uid</b>',styleN),
              Paragraph('<b>Name</b>',styleN),
              Paragraph('<b>Surname</b>',styleN),
              Paragraph('<b>Mark</b>',styleN),
              Paragraph('<b>Percentage</b>',styleN)
            ]]
    table = Table(tdata, colWidths=None, rowHeights=None)
    table.setStyle(TableStyle([
                                ('GRID',(0,0), (-1,-1),1, colors.black)
                              ]))
    table._argW[0]=1.4*inch #Set the size(width) of the first column in the table
    table._argW[1]=1.4*inch
    table._argW[2]=1.4*inch
    table._argW[3]=1.4*inch
    table._argW[4]=1.4*inch
    
    #table=Table(tdata, colWidths=80, rowHeights=30)
    table.wrapOn(c,100, currPos)
    currPos -=20
    table.drawOn(c,50, currPos)
    
    for student in student_list:
        uid = student[0]
        name = student[1]
        surname = student[2]
        mark = student[3]
        percentage = student[4]
        
        tdata = [uid, name, surname, mark, percentage],
        table = Table(tdata, colWidths=None, rowHeights=None)
        table.setStyle(TableStyle([
                                    ('GRID',(0,0), (-1,-1),1, colors.black)
                                  ]))
        #table=Table(tdata, colWidths=80, rowHeights=30)
        table._argW[0]=1.4*inch #Set the size(width) of the first collumn in the table
        table._argW[1]=1.4*inch
        table._argW[2]=1.4*inch
        table._argW[3]=1.4*inch
        table._argW[4]=1.4*inch
        table.wrapOn(c,75, currPos)
        currPos -= 20
        table.drawOn(c,50, currPos)
    
    # Close the PDF object cleanly.
    c.showPage()
    c.save()
    
    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
    
def generate_student_mark_pdf(data, student):
    """
    Generates a PDF document with a student's  marks,
    then allowes for it to be downloaded by the student.
    
    Arguments
    Mraks : An associative array of marks for a student
    module : The module the marks are for
    """
    module = data[0]['assessment'][0]
    filename = student + "_" + module + "_marks.pdf"
    print "Location : " + str(os.path.abspath(__file__))
    logo = os.path.join(os.path.dirname(os.path.abspath(__file__)),"static/reporting/images/cs_header_image.jpg")
    
    #Extract student information to paint onto the document
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename='+ filename
    
    buffer = BytesIO()
    
    # Create the PDF object, using the BytesIO object as its "file."
    c = canvas.Canvas(buffer)
    
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    c.setFont("Times-Roman",14,leading=None)
    c.drawString(30,750,"Student : " + student)
    c.drawString(30,725,"Module : " + module)
    
    #Add image on the top right of document
    c.drawImage(logo, 400, 710, width=2.5*inch, height=1.0*inch)
    

    c.line(180,710,380,710)
    
    c.setFont("Helvetica-Bold", 12, leading=None)
    styleN = styles['Normal']
    
    #Get information on the assessment that was clicked
    assessment_clicked = data[0]['assessment'][1][0]
    assessment_clicked_obtained_mark = data[0]['assessment'][1][1]
    assessment_clicked_total_mark = data[0]['assessment'][1][2]
    assessment_clicked_percentage_obtained = '{0:.3}'.format(data[0]['assessment'][1][3])
    
    #create row above the table specifying the assessment clicked
    tdata = [[Paragraph('<b>' + assessment_clicked + '</b>',styleN)
            ]]
    table = Table(tdata, colWidths=None, rowHeights=None)
    table.setStyle(TableStyle([
                                ('GRID',(0,0), (-1,0),1, colors.black)
                              ]))
    table._argW[0]=7.0*inch
    table.wrapOn(c,100, 710)
    table.drawOn(c,50, 600)
    
    tdata = [[Paragraph('<b>Assessment</b>',styleN),
              Paragraph('<b>Final Mark</b>',styleN),
              Paragraph('<b>Mark obtained</b>',styleN),
              Paragraph('<b>Percentage</b>',styleN)
            ]]
    table = Table(tdata, colWidths=None, rowHeights=None)
    table.setStyle(TableStyle([
                                ('GRID',(0,0), (-1,-1),1, colors.black)
                              ]))
    table._argW[0]=2.5*inch #Set the size(width) of the first collumn in the table
    table._argW[1]=1.5*inch
    table._argW[2]=1.5*inch
    table._argW[3]=1.5*inch
    
    #table=Table(tdata, colWidths=80, rowHeights=30)
    table.wrapOn(c,100, 650)
    table.drawOn(c,50,550)
    currPos = 550
    
    
    c.setFont("Helvetica", 11, leading=None)
    
    #Create new table for the marks
    tdata = []
    
    for mark in data[0]['assessment'][2:]:
        assessment_name = mark[0]
        assessment_obtained_mark = mark[1]
        assessment_total_mark = mark[2]
        assessment_percentage_obtained = '{0:.3}'.format(mark[3])
        
        tdata = [assessment_name, assessment_obtained_mark, assessment_total_mark, assessment_percentage_obtained],
        table = Table(tdata, colWidths=None, rowHeights=None)
        table.setStyle(TableStyle([
                                    ('GRID',(0,0), (-1,-1),1, colors.black)
                                  ]))
        #table=Table(tdata, colWidths=80, rowHeights=30)
        table._argW[0]=2.5*inch #Set the size(width) of the first collumn in the table
        table._argW[1]=1.5*inch
        table._argW[2]=1.5*inch
        table._argW[3]=1.5*inch
        table.wrapOn(c,75, 550)
        currPos -= 20
        table.drawOn(c,50, currPos)
        
    #Adding total mark of marks shown above. This is the assessment that was clicked
    tdata = [[Paragraph('<b>' + assessment_clicked + '</b>',styleN),
              Paragraph('<b>' + str(assessment_clicked_obtained_mark) + '</b>',styleN),
              Paragraph('<b>' + str(assessment_clicked_total_mark) + '</b>',styleN),
              Paragraph('<b>' + str(assessment_clicked_percentage_obtained) + '</b>',styleN)
            ]]
    table = Table(tdata, colWidths=None, rowHeights=None)
    table.setStyle(TableStyle([
                                ('GRID',(0,0), (-1,-1),1, colors.black),
                                ('BACKGROUND',(0,0),(-1,-1),colors.gray)#Give total a grey background
                                ]))
    #table=Table(tdata, colWidths=80, rowHeights=30)
    table._argW[0]=2.5*inch #Set the size(width) of the first collumn in the table
    table._argW[1]=1.5*inch
    table._argW[2]=1.5*inch
    table._argW[3]=1.5*inch
    table.wrapOn(c,75, 550)
    currPos -= 30
    table.drawOn(c,50, currPos)
    
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
    
    #Information on the assessment that was clicked
    assessment_clicked = data[0]['assessment'][1][0]
    assessment_clicked_obtained_mark = data[0]['assessment'][1][1]
    assessment_clicked_total_mark = data[0]['assessment'][1][2]
    assessment_clicked_percentage_obtained = '{0:.3}'.format(data[0]['assessment'][1][3])
    
    
    #Create writer object, this is what we use to append data to the file
    writer = csv.writer(response)
    
    #Write student information at the top
    writer.writerow(['Student',student])
    writer.writerow(['Module',module])
    writer.writerow([]) #Skipping a row
    
    
    writer.writerow(['Assessment', 'Mark obtained', 'Total Mark', 'Percentage'])
    for mark in data[0]['assessment'][2:]:
        assessment_name = mark[0]
        assessment_obtained_mark = mark[1]
        assessment_total_mark = mark[2]
        assessment_percentage_obtained = '{0:.3}'.format(mark[3])
        writer.writerow([assessment_name, assessment_obtained_mark, assessment_total_mark, assessment_percentage_obtained])
        
    #Finally write the total marks for the clicked assessment
    writer.writerow([]) #Skip row
    writer.writerow([assessment_clicked, assessment_clicked_obtained_mark,
                     assessment_clicked_total_mark, assessment_clicked_percentage_obtained]
                    )

    return response

'''
########################## READ CSV FILE ####################################
'''
#file that has only STUDENT NUMBER AND ONE MARK
def read_from_csv_file(assess_id, filepath):
    dataReader = csv.reader(open(filepath), delimiter=',', quotechar='"')
    marklist = []
    for row in dataReader:
        list = []
        #whatever the header will be
        if row[0] != 'Marks': # Ignore the header row, import everything else 
            studentNumber = row[0]
            studentMark = row[1]
            list.append(studentNumber)
            list.append(studentMark)
            marklist.append(list)
     
    #when do I close the reader?       
    return marklist

'''
def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

def parse_columns(ifile, columns, type_name="Bububu"):
    try:
        row_type = namedtuple(type_name, columns)
        print "columns : " + str(columns)
        print "row_type : " + str(row_type)
    except ValueError:
        row_type = tuple
    rows = csv.reader(open(ifile), delimiter=',', quotechar='"')
    header = rows.next()
    print "ifile: " + str(ifile)
    dataReader = csv.reader(open(ifile), delimiter=',', quotechar='"')

    print "rows : " + str(rows)
    print 'HEADER : ' + str(header)
    mapping = [header.index(x) for x in columns]
    print "MAPPING:    ----" + str(mapping)
    for row in rows:
        row = row_type(*[row[i] for i in mapping])
     
        yield row
#file that has multiple columns to read from   
def read_named_columns_csv(assess_id, filepath, columns):
    student_marks_list = []    
    ifile = StringIO(filepath)
    print "StringIO: " + str(filepath)
    
    print "======== START printing CSV Contents ======\n"
    for row in parse_columns(filepath, columns.split()):
        list = []
        length = len(row)
        for i in range(length):
            list.append(row[i])    
        student_marks_list.append(list)
    print "======== END printing CSV Contents ======\n"
    
    return student_marks_list

########################## END READ CSV FILE ####################################
'''