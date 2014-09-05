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

@csrf_exempt
def get_student_marks_pdf(request):
    mod = request.POST['module']
    data ={
        'module':mod
    }
    arr = []
    result = views.testingStudentAssessmentForModule(request,json.dumps(data))
    res = json.loads(result.content)
    if res[0]['type'] == '1':
        root = res[0]['root']
        first = res[0]['first']
        second = res[0]['second']
        third = res[0]['third']
        
    arr.append(root)
    arr.append(first)
    arr.append(second)
    arr.append(third)
    
    return generate_student_mark_pdf(arr,mod)

@csrf_exempt
def get_student_marks_csv(request):
    mod = request.POST['module']
    data ={
        'module':mod
    }
    arr = []
    result = views.testingStudentAssessmentForModule(request,json.dumps(data))
    res = json.loads(result.content)
    if res[0]['type'] == '1':
        root = res[0]['root']
        first = res[0]['first']
        second = res[0]['second']
        third = res[0]['third']
        
    arr.append(root)
    arr.append(first)
    arr.append(second)
    arr.append(third)
    
    return generate_student_mark_csv(arr,mod)
    
