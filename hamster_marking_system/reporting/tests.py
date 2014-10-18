from django.test import TestCase
import unittest
from mock import MagicMock
from reporting import views
from reporting import reporting_api as rapi

class testViews(unittest.TestCase):
    def test_get_assessment_report(self):
        mock_request = MagicMock()
        function = MagicMock()
        views.get_assessment_report = MagicMock(return_value=function)
        views.get_assessment_report(mock_request)
        views.get_assessment_report.assert_called_once_with(mock_request)
        views.get_assessment_report.assert_return_value(function)
        
    def test_get_student_marks_pdf(self):
        mock_request = MagicMock()
        function =  MagicMock()
        
        views.get_student_marks_pdf = MagicMock(return_value=function)
        views.get_student_marks_pdf(mock_request)
        views.get_student_marks_pdf.assert_called_once_with(mock_request)
        views.get_student_marks_pdf.assert_return_value(function)
        
    def test_get_student_marks_csv(self):
        mock_request = MagicMock()
        function = MagicMock()
        
        views.get_student_marks_csv = MagicMock(return_value=function)
        views.get_student_marks_csv(mock_request)
        views.get_student_marks_csv.assert_called_once_with(mock_request)
        views.get_student_marks_csv.assert_return_value(function)
        
    def test_import_csv(self):
        mock_request = MagicMock()
        mock_render_to_responce = MagicMock()
        
        views.import_csv = MagicMock(return_value = mock_render_to_responce)
        views.import_csv(mock_request)
        views.import_csv.assert_called_once_with(mock_request)
        views.import_csv.assert_return_value(mock_render_to_responce)
        

class ReportingAPITestCase(unittest.TestCase):
       
    def test_generate_assessment_report(self):
        mock_request = MagicMock()
        mock_render_to_responce = MagicMock()
        
        rapi.generate_assessment_report = MagicMock(return_value = mock_render_to_responce)
        rapi.generate_assessment_report(mock_request)
        rapi.generate_assessment_report.assert_called_once_with(mock_request)
        rapi.generate_assessment_report.assert_return_value(mock_render_to_responce)
    
    def test_generate_student_mark_pdf(self):
        mock_request = MagicMock()
        mock_render_to_responce = MagicMock()
        
        rapi.generate_student_mark_pdf = MagicMock(return_value = mock_render_to_responce)
        rapi.generate_student_mark_pdf(mock_request)
        rapi.generate_student_mark_pdf.assert_called_once_with(mock_request)
        rapi.generate_student_mark_pdf.assert_return_value(mock_render_to_responce)
    
    def test_generate_student_mark_csv(self):
        mock_request = MagicMock()
        mock_render_to_responce = MagicMock()
        
        rapi.generate_student_mark_csv = MagicMock(return_value = mock_render_to_responce)
        rapi.generate_student_mark_csv(mock_request)
        rapi.generate_student_mark_csv.assert_called_once_with(mock_request)
        rapi.generate_student_mark_csv.assert_return_value(mock_render_to_responce)
    
    def test_read_from_csv_file(self):
        mock_request = MagicMock()
        mock_render_to_responce = MagicMock()
        
        rapi.read_from_csv_file = MagicMock(return_value = mock_render_to_responce)
        rapi.read_from_csv_file(mock_request)
        rapi.read_from_csv_file.assert_called_once_with(mock_request)
        rapi.read_from_csv_file.assert_return_value(mock_render_to_responce)    
