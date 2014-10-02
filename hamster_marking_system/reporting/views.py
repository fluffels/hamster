from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.shortcuts import render
from web_services import views
from .reporting_api import *
from django.views.decorators.csrf import csrf_exempt

def hello_view(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def get_assessment_report(request):
    assess_id = request.POST['assess_id']
    data = {
        'assess_id':assess_id
    }
    
    result = views.assessmentReport(request, json.dumps(data))
    res = json.loads(result.content)
    data = res['data']
    module = data[0]
    assess_name = data[1]
    full_marks = data[2]
    stats = data[3]
    stat = []
    stat.append(stats[0])
    stat.append(stats[1])
    stat.append(stats[2])
    stat.append(stats[3])
    freq = stats[4]
    student_list = data[4]
    
    return generate_assessment_report(assess_name,full_marks,module, stats, freq, student_list)

@csrf_exempt
def get_student_marks_pdf(request):
    mod = request.POST['module']
    assessment = request.POST['assessment']
    student = request.session['user']['uid'][0]
    data ={
        'module':mod,
        'assessment':assessment,
        'student':student
    }
    result = views.StudentAssessmentAggregated(request,json.dumps(data))
    res = json.loads(result.content)
    
    return generate_student_mark_pdf(res,student)

@csrf_exempt
def get_student_marks_csv(request):
    mod = request.POST['module']
    assessment = request.POST['assessment']
    student = request.session['user']['uid'][0]
    data ={
        'module':mod,
        'assessment':assessment,
        'student':student
    }
    result = views.StudentAssessmentAggregated(request,json.dumps(data))
    res = json.loads(result.content)
    print "res : " + str(res)
    
    return generate_student_mark_csv(res,student)
############################################### CSV IMPORT #############################

@csrf_exempt
def import_csv(request):
    #filepath = "C:/Users/Sipho/Documents/GitHub/hamster/hamster_marking_system/reporting/files/test.csv"
    filepath = request.POST['filename']
    marker = request.session['user']['uid'][0]
    assess_id = request.POST['assess_id']

    marklist = read_from_csv_file(assess_id, filepath)
    
    data ={
        'assess_id':assess_id,
        'marklist':marklist,
        'marker':marker,
    }
    result = views.studentMarksFromCSV(request,json.dumps(data))
    return HttpResponseRedirect('assessment_center')
    
