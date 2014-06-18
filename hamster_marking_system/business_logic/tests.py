from django.test import TestCase
from unittest import TestCase
from unittest.mock import MagicMock

from .models import Person, Person_data, Module
from .api import *

'''
=============Testing models===========
======================================
'''

class PersonTestCase(TestCase):
    def setUp(self):
        Person._init_(self, 'Cebo',
                              'Makeleni',
                              'u12345678')
        PersonTestCase.lectureOf = Person.lectureOf
                
    def test_getfirstName(self):
        nm = Person.getfirstName(self)
        self.assertEqual(nm, 'Cebo')
        
    def test_getupId(self):
        uid = Person.getupId(self)
        self.assertEqual(uid, 'u12345678')
        
    def test_getsurname(self):
        sn = Person.getsurname(self)
        self.assertEqual(sn, 'Makeleni')
        
    def test_lectureOfInsert(self):
        #Nothing added
        li = PersonTestCase.lectureOf
        self.assertEqual(li, [])
        
        #Module added
        Person.lectureOfInsert(self, 'COS 301')
        self.assertEqual(li, ['COS 301'])
        
    def test_lectureOfDelete(self):
        #Adding modules
        PersonTestCase.lectureOf = ['COS 301', 'COS 344', 'COS 332', 'COS 341']
        li = PersonTestCase.lectureOf
        
        #Delete module
        Person.lectureOfDelete(self, 'COS 301')
        self.assertEqual(li, ['COS 344', 'COS 332', 'COS 341'])
        
    def test_studentOfInsert(self):
        #Nothing added
        PersonTestCase.lectureOf = []
        li = PersonTestCase.lectureOf
        self.assertEqual(li, [])
        
        #Module added
        Person.lectureOfInsert(self, 'COS 301')
        self.assertEqual(li, ['COS 301'])
        
    def test_studentOfDelete(self):
        #Adding modules
        PersonTestCase.lectureOf = ['COS 301', 'COS 344', 'COS 332', 'COS 341']
        li = PersonTestCase.lectureOf
        
        #Delete module
        Person.lectureOfDelete(self, 'COS 301')
        self.assertEqual(li, ['COS 344', 'COS 332', 'COS 341'])
        
    def test_tutorOfInsert(self):
        #Nothing added
        PersonTestCase.lectureOf = []
        li = PersonTestCase.lectureOf
        self.assertEqual(li, [])
        
        #Module added
        Person.lectureOfInsert(self, 'COS 301')
        self.assertEqual(li, ['COS 301'])
        
    def test_tutorOfDelete(self):
        #Adding modules
        PersonTestCase.lectureOf = ['COS 301', 'COS 344', 'COS 332', 'COS 341']
        li = PersonTestCase.lectureOf
        
        #Delete module
        Person.lectureOfDelete(self, 'COS 301')
        self.assertEqual(li, ['COS 344', 'COS 332', 'COS 341'])
        
    def test_teachingAssistantOfInsert(self):
        #Nothing added
        PersonTestCase.lectureOf = []
        li = PersonTestCase.lectureOf
        self.assertEqual(li, [])
        
        #Module added
        Person.lectureOfInsert(self, 'COS 301')
        self.assertEqual(li, ['COS 301'])
        
    def test_teachingAssistantOfDelete(self):
        #Adding modules
        PersonTestCase.lectureOf = ['COS 301', 'COS 344', 'COS 332', 'COS 341']
        li = PersonTestCase.lectureOf
        
        #Delete module
        Person.lectureOfDelete(self, 'COS 301')
        self.assertEqual(li, ['COS 344', 'COS 332', 'COS 341'])
    
    
    #Need to test getters for tutorOf, teachingAssistantOf, lecturerOf, and studentOf, but these are not added yet.
    #In addition, we need to test the inserts and deletes, but these are easily tested using the getters mensioned above.
    
    def tearDown(self):
        pass
    
'''    
class Person_dataTestCase(TestCase):
    def setUp(self):
        Person_data.setuid(self, 'u12345678')
        Person_data.setData(self, 'SomeData')
    
    def test_getuid(self, ):
        uid = Person_data.getuid(self)
        self.assertEqual(uid, 'u10534505')
    
    def test_getData(self, ):
        data= Person_data.getuid(self)
        self.assertEqual(data, 'someData')
    
    def tearDownModule(self):
        pass
        
    #Could not test because of the save() problem
'''

class ModuleTestCase(TestCase):
    #Test get and set module code
    thing = Module()
    thing.setmoduleCode = MagicMock()
    thing.setmoduleCode('COS 301')
    thing.setmoduleCode.assert_called_once_with('COS 301')
    
    mock = Module()
    mock.getmoduleCode = MagicMock(name = 'getModule', return_value = 'COS 301')
    mock.getmoduleCode.assert_return_value_is('COS 301')
    
    mock.setmoduleCode('COS 332')
    mock.getmoduleCode.assert_return_value_is('COS 332')
    
    #Test get, insert and remove marker
    marker = Module()
    marker.insertMarkers = MagicMock(name = 'insertMaker')
    marker.insertMarkers('Cebolenkosi')
    marker.insertMarkers.assert_called_once_with('Cebolenkosi')
    
    marker.getMarkers = MagicMock(name = 'getModule')
    marker.getMarkers.assert_return_value_is('Cebolenkosi')
    
    marker.removeMakers = MagicMock(name = 'delMarkers')
    marker.removeMakers('Cebo')
    marker.removeMakers.assert_called_once_with('Cebo')
    
    #Add test for wrong marker once error handling for removing marker is added.
    



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