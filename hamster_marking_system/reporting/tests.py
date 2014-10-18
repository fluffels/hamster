from django.test import TestCase
import unittest
from mock import MagicMock
from reporting import views


# Create your tests here.
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
        

        
        
