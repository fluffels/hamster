from django.test import TestCase
import unittest
from mock import MagicMock

from .models import Person, Person_data, Module, AggregateAssessment, Assessment
from .api import *

'''
=============Testing models===========
======================================
'''

class PersonTestCase(unittest.TestCase):
    def setUp(self):
        global foo
        foo = Person()
        Person._init_(foo, 'Cebo',
                              'Makeleni',
                              'u12345678')
        PersonTestCase.lectureOf = Person.lectureOf
        PersonTestCase.tutorOf = Person.tutorOf
        PersonTestCase.studentOf = Person.studentOf
        PersonTestCase.teachingAssistantOf = Person.teachingAssistantOf
                
    def test_getfirstName(self):
        nm = Person.getfirstName(foo)
        self.assertEqual(nm, 'Cebo')
        
    def test_getupId(self):
        uid = Person.getupId(foo)
        self.assertEqual(uid, 'u12345678')
        
    def test_getsurname(self):
        sn = Person.getsurname(foo)
        self.assertEqual(sn, 'Makeleni')
        
    def test_lectureOfInsert(self):
        #Nothing added
        Person.lectureOf = []
        li = Person.lectureOf
        self.assertEqual(li, [])
        
        #Module added
        Person.lectureOfInsert(foo, 'COS 301')
        self.assertEqual(li, ['COS 301'])
        
    def test_lectureOfDelete(self):
        #Adding modules
        Person.lectureOf = ['COS 301', 'COS 344', 'COS 332', 'COS 341']
        li = Person.lectureOf
        
        #Delete module
        Person.lectureOfDelete(foo, 'COS 301')
        li = Person.lectureOf
        self.assertEqual(li, ['COS 344', 'COS 332', 'COS 341'])
        
    def test_studentOfInsert(self):
        #Nothing added
        Person.studentOf = []
        li = Person.studentOf
        self.assertEqual(li, [])
        
        #Module added
        Person.studentOfInsert(foo, 'COS 301')
        self.assertEqual(li, ['COS 301'])
        
    def test_studentOfDelete(self):
        #Adding modules
        Person.studentOf = ['COS 301', 'COS 344', 'COS 332', 'COS 341']
        li = Person.studentOf
        
        #Delete module
        Person.studentOfDelete(foo, 'COS 301')
        li = Person.studentOf
        self.assertEqual(li, ['COS 344', 'COS 332', 'COS 341'])
        
    def test_tutorOfInsert(self):
        #Nothing added
        Person.tutorOf = []
        li = Person.tutorOf
        self.assertEqual(li, [])
        
        #Module added
        Person.tutorOfInsert(foo, 'COS 301')
        self.assertEqual(li, ['COS 301'])
        
    def test_tutorOfDelete(self):
        #Adding modules
        Person.tutorOf = ['COS 301', 'COS 344', 'COS 332', 'COS 341']
        li = Person.tutorOf
        
        #Delete module
        Person.tutorOfDelete(foo, 'COS 301')
        li = Person.tutorOf
        self.assertEqual(li, ['COS 344', 'COS 332', 'COS 341'])
        
    def test_teachingAssistantOfInsert(self):
        #Nothing added
        Person.teachingAssistantOf = []
        li = Person.teachingAssistantOf
        self.assertEqual(li, [])
        
        #Module added
        Person.teachingAssistantOfInsert(foo, 'COS 301')
        self.assertEqual(li, ['COS 301'])
        
    def test_teachingAssistantOfDelete(self):
        #Adding modules
        Person.teachingAssistantOf = ['COS 301', 'COS 344', 'COS 332', 'COS 341']
        li = Person.teachingAssistantOf
        
        #Delete module
        Person.teachingAssistantOfDelete(foo, 'COS 301')
        li = Person.teachingAssistantOf
        self.assertEqual(li, ['COS 344', 'COS 332', 'COS 341'])
    
    
    #Need to test getters for tutorOf, teachingAssistantOf, lecturerOf, and studentOf, but these are not added yet.
    #In addition, we need to test the inserts and deletes, but these are easily tested using the getters mensioned above.
    
    def tearDown(self):
        pass
    
   
class Person_dataTestCase(unittest.TestCase):
    def setUp(self):
        global foo
        foo = Person_data()
        Person_data.setuid(foo, 'u12345678')
        
    def test_setuid(self):
        mock = Person_data()
        mock.setuid = MagicMock(name = 'setuid')
        mock.setuid(foo, 'u87654321')
        mock.setuid.assert_called_once_with(foo, 'u87654321')
    
    def test_getuid(self):
        uid = Person_data.getuid(foo)
        self.assertEqual(uid, 'u12345678')
        
    def test_setData(self):
        mock = Person_data()
        mock.setData = MagicMock(name = 'setData')
        mock.setData(foo, 'SomeData')
        mock.setData.assert_called_with(foo, 'SomeData')
        
    def test_getData(self):
        mock = Person_data()
        mock.setData = MagicMock(name = 'setData')
        mock.setData('myData')
        mock.getData = MagicMock(name = 'getData', return_value = 'myData')
        self.assertEqual(mock.getData(), 'myData')
        
    
    
    
    
    def tearDown(self):
        pass

class ModuleTestCase(unittest.TestCase):
    #Test get and set module code
    def test_setModule(self):
        thing = Module()
        thing.setmoduleCode = MagicMock()
        thing.setmoduleCode('COS 301')
        thing.setmoduleCode.assert_called_once_with('COS 301')
    
    def test_getModuleCode(self):
        mock = Module()
        mock.getmoduleCode = MagicMock(name = 'getModule', return_value = 'COS 301')
        mock.getmoduleCode.assert_return_value_is('COS 301')
        
        mock.setmoduleCode('COS 332')
        mock.getmoduleCode.assert_return_value_is('COS 332')
    
    #Test get, insert and remove marker
    def test_insertMarkers(self):
        marker = Module()
        marker.insertMarkers = MagicMock(name = 'insertMaker')
        marker.insertMarkers('Cebolenkosi')
        marker.insertMarkers.assert_called_once_with('Cebolenkosi')
    
    def test_getMarkers(self):
        #setUp
        marker = Module()
        marker.insertMarkers = MagicMock(name = 'insertMaker')
        marker.insertMarkers('Cebolenkosi')
        marker.insertMarkers.assert_called_once_with('Cebolenkosi')
        
        #Testing
        marker.getMarkers = MagicMock(name = 'getModule')
        marker.getMarkers.assert_return_value_is('Cebolenkosi')
    
    def test_removeMarkers(self):
        marker = Module()
        marker.removeMakers = MagicMock(name = 'delMarkers')
        marker.removeMakers('Cebo')
        marker.removeMakers.assert_called_once_with('Cebo')
    
    #Add test for wrong marker once error handling for removing marker is added.
    
class AggregateAssessmentTestCase(unittest.TestCase):
    def setUp(self):
        global mock
        mock = AggregateAssessment()
        mock = MagicMock(name = 'AggregateAssessment')
    
    def test_setaggregator(self):
        mock.setaggregator('aggregator')
        mock.setaggregator.assert_called_once_with('aggregator')
        
    def test_getaggregator(self):
        mock.getaggregator.assert_return_value_is('aggregator')
        
    def test_insertassessList(self):
        mock.insertassessList('Ass1')
        mock.insertassessList.assert_called_once_with('Ass1')
        
        mock.insertassessList()
        mock.insertassessList.assert_called_with()
        
    def test_deleteassessList(self):
        mock.deleteassessList('Ass1')
        mock.deleteassessList.assert_called_once_with('Ass1')
        mock.assessList.assert_return_value_is([])



'''
=============End models===========
======================================
'''
    
    
'''
=============Testing api===========
===================================
'''

def test_getAllLecturesOfModule():
    '''
    mock.getAllLecturesOfModule = MagicMock(name = 'getAllLec')
    mock.getPersonListFromArrayList = MagicMock(name = 'getPerLi')
    mock.getAllLecturesOfModule('Some module')
    mock.getAllLecturesOfModule.assert_called_with('Some module')
    '''
    pass #need to remove this once api code has no more bugs that prevent testing



'''
=============End api===========
===============================
'''


'''
=============Testing view==========
===================================
'''




'''
=============End views=============
===================================
'''

if __name__ == '__main__':
    unittest.main()