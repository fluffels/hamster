from django.test import TestCase
import unittest
from mock import MagicMock
import datetime
import json
from web_interface import views
# Create your tests here.

class testViews(unittest.TestCase):
    def test_home(self):
        mock_request = MagicMock()
        mock_render_to_response=MagicMock()
        
        views.home = MagicMock(return_value=mock_render_to_response)
        views.home(mock_request)
        views.home.assert_called_once_with(mock_request)
        views.home.assert_return_value(mock_render_to_response)
        
    def test_reCaptchaLogin(self):
        mock_request = MagicMock()
        mock_render_to_response=MagicMock()
        
        views.reCaptchaLogin = MagicMock(return_value=mock_render_to_response)
        views.reCaptchaLogin(mock_request)
        views.reCaptchaLogin.assert_called_once_with(mock_request)
        views.reCaptchaLogin.assert_return_value(mock_render_to_response)
        
    def test_login(self):
        mock_request = MagicMock()
        mock_render_to_response=MagicMock()
        
        views.login = MagicMock(return_value=mock_render_to_response)
        views.login(mock_request)
        views.login.assert_called_once_with(mock_request)
        views.login.assert_return_value(mock_render_to_response)
        
    def test_backHome(self):
        mock_request = MagicMock()
        mock_render_to_response=MagicMock()
        
        views.backHome = MagicMock(return_value=mock_render_to_response)
        views.backHome(mock_request)
        views.backHome.assert_called_once_with(mock_request)
        views.backHome.assert_return_value(mock_render_to_response)
        
    def test_use_as(self):
        mock_request = MagicMock()
        mock_render_to_response=MagicMock()
        
        views.use_as = MagicMock(return_value=mock_render_to_response)
        views.use_as(mock_request)
        views.use_as.assert_called_once_with(mock_request)
        views.use_as.assert_return_value(mock_render_to_response)
        
    def test_logout(self):
        mock_request = MagicMock()
        mock_render_to_response=MagicMock()
        
        views.logout = MagicMock(return_value=mock_render_to_response)
        views.logout(mock_request)
        views.logout.assert_called_once_with(mock_request)
        views.logout.assert_return_value(mock_render_to_response)
        
    def test_getAllAssessmentOfModule(self):
        mock_request = MagicMock()
        mock_render_to_response=MagicMock()
        
        views.getAllAssessmentOfModule = MagicMock(return_value=mock_render_to_response)
        views.getAllAssessmentOfModule(mock_request)
        views.getAllAssessmentOfModule.assert_called_once_with(mock_request)
        views.getAllAssessmentOfModule.assert_return_value(mock_render_to_response)

    def test_personDetails(self):
        mock_request = MagicMock()
        mock_render_to_response=MagicMock()
        
        views.personDetails = MagicMock(return_value=mock_render_to_response)
        views.personDetails(mock_request)
        views.personDetails.assert_called_once_with(mock_request)
        views.personDetails.assert_return_value(mock_render_to_response)
        
    def test_getAllSessionsForAssessment(self):
        mock_request = MagicMock()
        mock_render_to_response=MagicMock()
        
        views.getAllSessionsForAssessment = MagicMock(return_value=mock_render_to_response)
        views.getAllSessionsForAssessment(mock_request)
        views.getAllSessionsForAssessment.assert_called_once_with(mock_request)
        views.getAllSessionsForAssessment.assert_return_value(mock_render_to_response)
        
    def test_createSession(self):
        mock_request = MagicMock()
        mock_render_to_response=MagicMock()
        
        views.createSession = MagicMock(return_value=mock_render_to_response)
        views.createSession(mock_request)
        views.createSession.assert_called_once_with(mock_request)
        views.createSession.assert_return_value(mock_render_to_response)
        
    def test_getAllStudentOfModule(self):
        mock_request = MagicMock()
        mock_render_to_response=MagicMock()
        
        views.getAllStudentOfModule = MagicMock(return_value=mock_render_to_response)
        views.getAllStudentOfModule(mock_request)
        views.getAllStudentOfModule.assert_called_once_with(mock_request)
        views.getAllStudentOfModule.assert_return_value(mock_render_to_response)
        
    def test_getAllPersonOfSession(self):
        mock_request = MagicMock()
        mock_render_to_response=MagicMock()
        
        views.getAllPersonOfSession = MagicMock(return_value=mock_render_to_response)
        views.getAllPersonOfSession(mock_request)
        views.getAllPersonOfSession.assert_called_once_with(mock_request)
        views.getAllPersonOfSession.assert_return_value(mock_render_to_response)

    def test_addStudentToSession(self):
        mock_request = MagicMock()
        mock_render_to_response=MagicMock()
        
        views.addStudentToSession = MagicMock(return_value=mock_render_to_response)
        views.addStudentToSession(mock_request)
        views.addStudentToSession.assert_called_once_with(mock_request)
        views.addStudentToSession.assert_return_value(mock_render_to_response)
        
    def test_getLeafAssessmentPage(self):
        mock_request = MagicMock()
        mock_render_to_response=MagicMock()
        
        views.getLeafAssessmentPage = MagicMock(return_value=mock_render_to_response)
        views.getLeafAssessmentPage(mock_request)
        views.getLeafAssessmentPage.assert_called_once_with(mock_request)
        views.getLeafAssessmentPage.assert_return_value(mock_render_to_response)
        
    def test_createLeafAssessment(self):
        mock_request = MagicMock()
        mock_render_to_response=MagicMock()
        
        views.createLeafAssessment = MagicMock(return_value=mock_render_to_response)
        views.createLeafAssessment(mock_request)
        views.createLeafAssessment.assert_called_once_with(mock_request)
        views.createLeafAssessment.assert_return_value(mock_render_to_response)
    
    def test_updateMarkForStudent(self):
        mock_request = MagicMock()
        mock_render_to_response=MagicMock()
        
        views.updateMarkForStudent = MagicMock(return_value=mock_render_to_response)
        views.updateMarkForStudent(mock_request)
        views.updateMarkForStudent.assert_called_once_with(mock_request)
        views.updateMarkForStudent.assert_return_value(mock_render_to_response)
        
    def test_deleteAssessment(self):
        mock_request = MagicMock()
        mock_render_to_response=MagicMock()
        
        views.deleteAssessment = MagicMock(return_value=mock_render_to_response)
        views.deleteAssessment(mock_request)
        views.deleteAssessment.assert_called_once_with(mock_request)
        views.deleteAssessment.assert_return_value(mock_render_to_response)