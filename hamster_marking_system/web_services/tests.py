from django.test import TestCase
import unittest
from mock import MagicMock
import datetime
import json
from web_services import views
# Create your tests here.

class testViews(unittest.TestCase):
    def test_getAllPersonOfSession(self):
        mock_request = MagicMock()
        mock_response = MagicMock()
        data ={
        'session_id':1
        }
        views.getAllPersonOfSession = MagicMock(return_value =mock_response)
        views.getAllPersonOfSession(mock_request,json.dumps(data))
        views.getAllPersonOfSession.assert_called_once_with(mock_request,json.dumps(data))
        views.getAllPersonOfSession.assert_return_value(mock_response)
        
    def test_getAllChildrenOfAssessment(self):
        mock_request = MagicMock()
        mock_response = MagicMock()
        data = {
        'assess_id':1,
        'mod':"COS333"
        }
        views.getAllChildrenOfAssessment = MagicMock(return_value=mock_response)
        views.getAllChildrenOfAssessment(mock_request,json.dumps(data))
        views.getAllChildrenOfAssessment.assert_called_once_with(mock_request,json.dumps(data))
        views.getAllChildrenOfAssessment.assert_return_value(mock_response)
        
    def test_getAllChildrenOfAssessmentForLeaf(self):
        mock_request =MagicMock()
        mock_response = MagicMock()
        data_mod = {
        'mod':"COS233",
        'assess_id':1
        }
        views.getAllChildrenOfAssessmentForLeaf = MagicMock(return_value=mock_response)
        views.getAllChildrenOfAssessmentForLeaf(mock_request,json.dumps(data_mod))
        views.getAllChildrenOfAssessmentForLeaf.assert_called_once_with(mock_request,json.dumps(data_mod))
        views.getAllChildrenOfAssessmentForLeaf.assert_return_value(mock_response)
        
    def test_updateMarkForStudent(self):
        mock_request =MagicMock()
        mock_response = MagicMock()
        
        data = {
        'leaf_id':1,
        'mark':12,
        'student':"u12345678",
        'mod':"COS333",
        'reason':"mistake made while marking"
        }
        views.updateMarkForStudent = MagicMock(return_value=mock_response)
        views.updateMarkForStudent(mock_request,json.dumps(data))
        views.updateMarkForStudent.assert_called_once_with(mock_request,json.dumps(data))
        views.updateMarkForStudent.assert_return_value(mock_response)
        
    def test_createLeafAssessment(self):
        mock_request =MagicMock()
        mock_response = MagicMock()
        
        data = {
                'name':"Assignment 1",
                'mod':"COS333",
                'fullmark':12,
                'assess_id': 1
        }
        
        views.createLeafAssessment = MagicMock(return_value=mock_response)
        views.createLeafAssessment(mock_request,json.dumps(data))
        views.createLeafAssessment.assert_called_once_with(mock_request,json.dumps(data))
        views.createLeafAssessment.assert_return_value(mock_response)
        
    def test_deleteAssessment(self):
        mock_request =MagicMock()
        mock_response = MagicMock()
        data = {
            'assess_id':1,
        }
        
        views.deleteAssessment = MagicMock(return_value = mock_response)
        views.deleteAssessment(mock_request,json.dumps(data))
        views.deleteAssessment.assert_called_once_with(mock_request,json.dumps(data))
        views.deleteAssessment.assert_return_value(mock_response)
        
    def test_deleteSession(self):
        mock_request =MagicMock()
        mock_response = MagicMock()
        data = {
        'sessionId':1
        }
        
        views.deleteSession = MagicMock(return_value=mock_response)
        views.deleteSession(mock_request,json.dumps(data))
        views.deleteSession.assert_called_once_with(mock_request,json.dumps(data))
        views.deleteSession.assert_return_value(mock_response)
        
    def test_changeAssessmentFullMark(self):
        mock_request =MagicMock()
        mock_response = MagicMock()
        data = {
        'assess_id':1,
        'full_mark':14
       }
        
        views.changeAssessmentFullMark = MagicMock(return_value = mock_response)
        views.changeAssessmentFullMark(mock_request,json.dumps(data))
        views.changeAssessmentFullMark.assert_called_once_with(mock_request,json.dumps(data))
        views.changeAssessmentFullMark.assert_return_value(mock_response)
        
    def test_changeAssessmentName(self):
        mock_request =MagicMock()
        mock_response = MagicMock()
        data = {
        'assess_id':1,
        'assess_name':"Practical 1"
       }
        
        views.changeAssessmentName = MagicMock(return_value=mock_response)
        views.changeAssessmentName(mock_request,json.dumps(data))
        views.changeAssessmentName.assert_called_once_with(mock_request,json.dumps(data))
        views.changeAssessmentName.assert_return_value(mock_response)
        
    def test_openOrCloseSession(self):
        mock_request =MagicMock()
        mock_response = MagicMock()
        data = {
        'assess_id':1,
        'sess_id':2,
        'status':1
       }
        
        views.openOrCloseSession = MagicMock(return_value=mock_response)
        views.openOrCloseSession(mock_request,json.dumps(data))
        views.openOrCloseSession.assert_called_once_with(mock_request,json.dumps(data))
        views.openOrCloseSession.assert_return_value(mock_response)
        
    def test_setPublishedStatus(self):
        mock_request =MagicMock()
        mock_response = MagicMock()
        data = {
        'assess_id':1,
        'status':1,
        'module':"COS333"
       }
        views.setPublishedStatus = MagicMock(return_value = mock_response)
        views.setPublishedStatus(mock_request,json.dumps(data))
        views.setPublishedStatus.assert_called_once_with(mock_request,json.dumps(data))
        views.setPublishedStatus.assert_return_value(mock_response)
        
    def test_viewSessionForMarker(self):
        mock_request =MagicMock()
        mock_response = MagicMock()
        data ={
            'mod':"COS333"
        }
        views.viewSessionForMarker = MagicMock(return_value=mock_response)
        views.viewSessionForMarker(mock_request,json.dumps(data))
        views.viewSessionForMarker.assert_called_once_with(mock_request,json.dumps(data))
        views.viewSessionForMarker.assert_return_value(mock_response)
        
    def test_viewAssessmentForMarker(self):
        mock_request =MagicMock()
        mock_response = MagicMock()
        data = {
        'sessions':1
        }
        views.viewAssessmentForMarker = MagicMock(return_value=mock_response)
        views.viewAssessmentForMarker(mock_request,json.dumps(data))
        views.viewAssessmentForMarker.assert_called_once_with(mock_request,json.dumps(data))
        views.viewAssessmentForMarker.assert_return_value(mock_response)
        
    def test_viewStudentsForAssessment(self):
        mock_request =MagicMock()
        mock_response = MagicMock()
        data = {
        'session':1,
        'assess_id':2
        }
        views.viewStudentsForAssessment = MagicMock(return_value=mock_response)
        views.viewStudentsForAssessment(mock_request,json.dumps(data))
        views.viewStudentsForAssessment.assert_called_once_with(mock_request,json.dumps(data))
        views.viewStudentsForAssessment.assert_return_value(mock_response)
    
    def test_updateMarkForStudentMarker(self):
        mock_request =MagicMock()
        mock_response = MagicMock()
        data = {
        'leaf_id':1,
        'mark':12,
        'student':"u12345678",
        'mod':"COS333",
        'session':2,
        'reason':"remarking"
       }
        views.updateMarkForStudentMarker = MagicMock(return_value=mock_response)
        views.updateMarkForStudentMarker(mock_request,json.dumps(data))
        views.updateMarkForStudentMarker.assert_called_once_with(mock_request,json.dumps(data))
        views.updateMarkForStudentMarker.assert_return_value(mock_response)
        
    def test_viewStudentAssessment(self):
        mock_request =MagicMock()
        mock_response = MagicMock()
        data = {
        'mod_code':"COS33",
        'uid': "u12345678"
        }
        views.viewStudentAssessment = MagicMock(return_value=mock_response)
        views.viewStudentAssessment(mock_request,json.dumps(data))
        views.viewStudentAssessment.assert_called_once_with(mock_request,json.dumps(data))
        views.viewStudentAssessment.assert_return_value(mock_response)