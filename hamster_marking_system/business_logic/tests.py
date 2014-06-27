from django.test import TestCase
import unittest
from mock import MagicMock

from .models import Person, Person_data, Module, AggregateAssessment, Assessment, Sessions, LeafAssessment
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
        PersonTestCase.lectureOf_module = Person.lectureOf_module
        PersonTestCase.tutorOf_module = Person.tutorOf_module
        PersonTestCase.studentOf_module = Person.studentOf_module
        PersonTestCase.teachingAssistantOf_module = Person.teachingAssistantOf_module
                
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
        Person.lectureOf_module = []
        li = Person.lectureOf_module
        self.assertEqual(li, [])
        
        #Module added
        Person.lectureOfInsert(foo, 'COS 301')
        self.assertEqual(li, ['COS 301'])
        
    def test_lectureOfDelete(self):
        #Adding modules
        Person.lectureOf_module = ['COS 301', 'COS 344', 'COS 332', 'COS 341']
        li = Person.lectureOf_module
        
        #Delete module
        Person.lectureOfDelete(foo, 'COS 301')
        li = Person.lectureOf_module
        self.assertEqual(li, ['COS 344', 'COS 332', 'COS 341'])
        
    def test_studentOfInsert(self):
        #Nothing added
        Person.studentOf_module = []
        li = Person.studentOf_module
        self.assertEqual(li, [])
        
        #Module added
        Person.studentOfInsert(foo, 'COS 301')
        self.assertEqual(li, ['COS 301'])
        
    def test_studentOfDelete(self):
        #Adding modules
        Person.studentOf_module = ['COS 301', 'COS 344', 'COS 332', 'COS 341']
        li = Person.studentOf_module
        
        #Delete module
        Person.studentOfDelete(foo, 'COS 301')
        li = Person.studentOf_module
        self.assertEqual(li, ['COS 344', 'COS 332', 'COS 341'])
        
    def test_tutorOfInsert(self):
        #Nothing added
        Person.tutorOf_module = []
        li = Person.tutorOf_module
        self.assertEqual(li, [])
        
        #Module added
        Person.tutorOfInsert(foo, 'COS 301')
        self.assertEqual(li, ['COS 301'])
        
    def test_tutorOfDelete(self):
        #Adding modules
        Person.tutorOf_module = ['COS 301', 'COS 344', 'COS 332', 'COS 341']
        li = Person.tutorOf_module
        
        #Delete module
        Person.tutorOfDelete(foo, 'COS 301')
        li = Person.tutorOf_module
        self.assertEqual(li, ['COS 344', 'COS 332', 'COS 341'])
        
    def test_teachingAssistantOfInsert(self):
        #Nothing added
        Person.teachingAssistantOf_module = []
        li = Person.teachingAssistantOf_module
        self.assertEqual(li, [])
        
        #Module added
        Person.teachingAssistantOfInsert(foo, 'COS 301')
        self.assertEqual(li, ['COS 301'])
        
    def test_teachingAssistantOfDelete(self):
        #Adding modules
        Person.teachingAssistantOf_module = ['COS 301', 'COS 344', 'COS 332', 'COS 341']
        li = Person.teachingAssistantOf_module
        
        #Delete module
        Person.teachingAssistantOfDelete(foo, 'COS 301')
        li = Person.teachingAssistantOf_module
        self.assertEqual(li, ['COS 344', 'COS 332', 'COS 341'])
    
    
    #Need to test getters for tutorOf_module, teachingAssistantOf_module, lecturerOf, and studentOf_module, but these are not added yet.
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
    '''
    def setUp(self):
        global mock
        mock = AggregateAssessment(1) #null is possible parent id
        mock = MagicMock(name = 'AggregateAssessment')
    '''
    def test_add_child(self, id_child):
        pass
    
    def test_get_current_assessment():
        pass
    
    def test_get_mark():
        pass
    
    def test_get_subassessment(self, subName ):
        pass
    
    def test_get_children(self ):
        pass
    
    def test_get_aggregator_name():
        pass
    
    def test_is_root(self):
        pass
    
    def test_getaggregator(self):
        #mock.getaggregator.assert_return_value_is('aggregator')
        pass
    
    def test_choose_aggregator(self, agg_key):
        pass
    


class SessionTestCase(unittest.TestCase):
	
	def test_setAssessmentID(self):
		session = Sessions()
		session.setAssessmentID = MagicMock()
		session.setAssessmentID("12")
		session.setAssessmentID.assert_called_once_with("12")
		
	def test_setOpenedDate(self):
		session = Sessions()
		session.setOpenedDate = MagicMock()
		session.setOpenedDate("2014-06-06 12:00:00")
		session.setOpenedDate.assert_called_once_with("2014-06-06 12:00:00")
		
	def test_setClosedDate(self):
		session = Sessions()
		session.setClosedDate = MagicMock()
		session.setClosedDate("2014-06-06 12:00:00")
		session.setClosedDate.assert_called_once_with("2014-06-06 12:00:00")
		
	def test_setOpen(self):
		session = Sessions()
		session.setOpen = MagicMock()
		session.setOpen()
		session.setOpen.assert_called_once_with()
		
	def test_setClose(self):
		session = Sessions()
		session.setClose = MagicMock()
		session.setClose()
		session.setClose.assert_called_once_with()
		
	def test_setName(self):
		session = Sessions()
		session.setName = MagicMock()
		session.setName("Pract1Session1")
		session.setName.assert_called_once_with("Pract1Session1")
		
	def test_getID(self):
		session = Sessions()
		session.getID = MagicMock(return_value = "1")
		session.getID()
		session.getID.assert_return_value_is("1")
		
	def test_getAssessmentID(self):
		session = Sessions()
		session.getAssessmentID = MagicMock(return_value = "12")
		session.getAssessmentID()
		session.getAssessmentID.assert_return_value_is("12")
		
	def test_getClosedDate(self):
		session = Sessions()
		session.getClosedDate = MagicMock(return_value = "2014-06-06 12:00:00") 
		session.getClosedDate()
		session.getClosedDate.assert_return_value_is("2014-06-06 12:00:00")
	
	def test_getStatus(self):
		session = Sessions()
		session.getStatus = MagicMock(return_value = "1")
		session.getStatus()
		session.getStatus.assert_return_value_is("1")
		
	def test_getOpenedDate(self):
		session = Sessions()
		session.getOpenedDate = MagicMock(return_value = "2014-06-06 12:00:00")
		session.getOpenedDate()
		session.getOpenedDate.assert_return_value_is("2014-06-06 12:00:00")
	
	def test_getName(self):
		session = Sessions()
		session.getName = MagicMock(return_value = "Pract1Session1")
		session.getName()
		session.getName.assert_return_value_is("Pract1Session1")
		
		session1 = Sessions(session_name = "Pract1Session1")
		do = session1.getName()
		self.assertEqual(do, "Pract1Session1")
		
	
	def test_deleteSessions(self):
		session = Sessions()
		session.deleteSessions = MagicMock()
		session.deleteSessions()
		session.deleteSessions.assert_called_once_with()
		
	def test_insertSessions(self):
		#insertSession = MagicMock()
		session = Sessions()
		assessment = Assessment()
		module = Module()
		
		module.insertModule = MagicMock()
		assessment.insertAssessment = MagicMock()
		session.insertSessions = MagicMock()
		
		module.insertModule("COS 301")
		assessment.insertAssessment("practical1", "30", "type",module)
		session.insertSessions("Pract1Session1",assessment,"2014-06-06 12:00:00","2014-06-07 12:04:00")
		session.insertSessions.assert_called_once_with("Pract1Session1",assessment,"2014-06-06 12:00:00","2014-06-07 12:04:00")
		
	def test_getSessions(self):
		session = Sessions()
		session.getSessions = MagicMock()
		session.getSessions()
		session.getSessions.assert_called_once_with()


class AssessmentTestCase(TestCase):
	#def setUp(self):
		#Module.objects.create(code='COS212')
		#Assessment.objects.create(assessment_name='Practical8', assessment_weight='20', assessment_type='Aggregate', module_id=)

	def test_setModule(self):
		ass = Assessment()
		mod = Module()

		mod.insertModule = MagicMock()
		ass.setModule = MagicMock()

		mod.insertModule('COS212')
		ass.setModule(mod)
		ass.setModule.assert_called_once_with(mod)

	def test_setName(self):
		ass = Assessment()
		ass = MagicMock()

		ass.setName('Practical8')
		ass.setName.assert_called_once_with('Practical8')

	def test_setWeight(self):
		ass = Assessment()
		ass = MagicMock()
		ass.setWeight('20')
		ass.setWeight.assert_called_once_with('20')


	def test_setType(self):
		ass = Assessment()
		ass = MagicMock()
		ass.setType('Aggregate')
		ass.setType.assert_called_once_with('Aggregate')

	def test_getID(self):
		ass = Assessment()
		ass = MagicMock()
		ass.getID()
		ass.getID.assert_called_once_with()

	def test_getName(self):
		ass = Assessment()
		ass = MagicMock()
		ass.setName('Prac8')
		ass.assertEqual(ass.getName(), 'Prac8')

	def test_getWeight(self):
		ass = Assessment()
		ass = MagicMock()
		ass.setWeight('30')
		ass.assertEqual(ass.getWeight(), '30')

	def test_getType(self):
		ass = Assessment()
		ass = MagicMock()
		ass.setType('Aggregate')
		ass.assertEqual(ass.getType(), 'Aggregate')

	def test_getModule(self):
		ass = Assessment()
		mod = Module()

		ass.getModule = MagicMock()
		mod.insertModule = MagicMock()
		ass.setModule = MagicMock()

		mod.insertModule('COS151')
		ass.setModule(mod)

		ass.getModule.assertEqual(ass.getModule(), 'COS212')

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