from django.test import TestCase
import unittest
from mock import MagicMock

from .models import *
from .api import *
from business_logic import api
from business_logic import views

'''
=============Testing models===========
======================================
'''

class PersonTestCase(unittest.TestCase):
    def setUp(self):
        global foo, mock
        foo = Person()
        mock = Person()
        mock = MagicMock()
        Person._init_(foo, 'Cebo',
                              'Makeleni',
                              'u12345678')
        PersonTestCase.lectureOf_module = Person.lectureOf_module
        PersonTestCase.tutorOf_module = Person.tutorOf_module
        PersonTestCase.studentOf_module = Person.studentOf_module
        PersonTestCase.teachingAssistantOf_module = Person.teachingAssistantOf_module
                
    def test_getFirstName(self):
        nm = Person.getFirstName(foo)
        self.assertEqual(nm, 'Cebo')
        
    def test_getupId(self):
        uid = Person.getupId(foo)
        self.assertEqual(uid, 'u12345678')
        
    def test_getSurname(self):
        sn = Person.getSurname(foo)
        self.assertEqual(sn, 'Makeleni')
        
    def test_setFirstName(self):
        mock.setFirstName('Mabhebeza')
        mock.getFirstName.assert_return_value_is('Mabhebeza')
        
    def test_setupId(self):
        mock.setupId('uxxxxxxxx')
        mock.getupId.assert_return_value_is('uxxxxxxxx')
        
    def test_setSurname(self):
        mock.setSurname('Mamiki')
        mock.getSurname.assert_return_value_is('Mamiki')
        
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
    
    
class Person_dataOuterFunctionsTestCase(unittest.TestCase):
    def setUp(self):
        global mockInsert, mockGet, mockDelete
        mockInsert = MagicMock()
        mockGet = MagicMock()
        mockDelete = MagicMock()

    def test_insertPerson_data(self):
        mockInsert.insertPerson_data('u12345678', 'Some data')
        mockInsert.insertPerson_data.assert_called_once()
        
    def test_getAllPerson_data(self):
        mockGet.getAllPerson_data.assert_return_value_is('u12345678')
        
    def test_deletePerson_data(self):
        mockDelete.deletePerson_data()
        mockDelete.deletePerson_data.assert_called_once()
    

class ModuleTestCase(unittest.TestCase):
    #Test get and set module code
    def test_setModuleCode(self):
        thing = Module()
        thing.setModuleCode = MagicMock()
        thing.setModuleCode('COS 301')
        thing.setModuleCode.assert_called_once_with('COS 301')
    
    def test_getModuleCode(self):
        mock = Module()
        mock.getModuleCode = MagicMock(name = 'getModule', return_value = 'COS 301')
        mock.getModuleCode.assert_return_value_is('COS 301')
        
        mock.setModuleCode('COS 332')
        mock.getModuleCode.assert_return_value_is('COS 332')
    
    def test_setModuleName(self):
        thing = Module()
        thing.setModuleName = MagicMock()
        thing.setModuleName('COS 301')
        thing.setModuleName.assert_called_once_with('COS 301')
    
    def test_getModuleName(self):
        mock = Module()
        mock.getModuleName = MagicMock(name = 'getModuleName', return_value = 'COS 301')
        mock.getModuleName.assert_return_value_is('COS 301')
        
        mock.setModuleName('COS 332')
        mock.getModuleName.assert_return_value_is('COS 332')

class ModuleOuterFunctionsTestCase(unittest.TestCase):
    def setUp(self):
        global mockInsert, mockGet, mockDelete, assessment
        mockInsert = MagicMock(return_value = 'Insterted')
        mockGet = MagicMock()
        mockDelete = MagicMock()
        assessment = MagicMock(return_value = 'Class test')

    def test_insertModule(self):
        mockInsert.insertModule('COS332', 'Netw', '2014', assessment)
        mockInsert.insertModule.assert_return_value_is('Insterted')
        
    def test_getAllModules(self):
        mockGet.getAllModules.assert_return_value_is('COS332')
        
    def test_deleteModule(self):
        mockDelete.deleteModule('COS332')
        mockDelete.deleteModule.assert_called_once_with('COS332')
      
class AggregateAssessmentTestCase(unittest.TestCase):
	
	def test_add_child( child_id):
		assess_child = Assessment()
		assess_child = MagicMock()
		assess_parent = AggregateAssessment()
		assess_parent = MagicMock()
		assess_parent.add_child(assess_child.id)
		assess_parent.add_child.assert_called_once_with(assess_child.id) 
		
	def test_get_current_assessment(self):
		assess = AggregateAssessment()
		assess = MagicMock()

		assess2 = assess.get_current_assessment()
		assess.get_current_assessment.assertEqual(assess2.id, assess.id)
		
	def test_get_mark(self):
		assess = AggregateAssessment()
		assess = MagicMock()
		assess.mark = 5
		x = assess.get_mark()
		assess.get_mark.assertEqual(assess.get_mark, x)
		
	def test_get_subassessment( sub_name):
		assess = AggregateAssessment()
		subAssess = AggregateAssessment(assess.id)
		
		assess = MagicMock()
		subAssess = MagicMock()
		
		x = assess.get_subassessment(subAssess)
		
		assess.get_subassessment.assertEqual(x.id, subAssess.id)
		
	def test_get_children(self):
		assess = AggregateAssessment()
		subAssess = AggregateAssessment(assess.id)
		
		assess = MagicMock()
		subAssess = MagicMock()
		
		x = assess.get_subassessment(subAssess)
		
		assess.get_subassessment.assertEqual(x.id, subAssess.id)
		
	def test_get_aggregator_name(self):
		assess = AggregateAssessment()
		assess = MagicMock()
		assess.choose_aggregator(1)
		
		name_=assess.get_aggregator_name()
		
		assess.get_aggregator_name.assertEqual(name_, 'S')
		
		
	def test_is_root(self):
		assess = AggregateAssessment()
		non_rootAssess = AggregateAssessment(assess.id)
		
		assess = MagicMock()
		non_rootAssess = MagicMock()
		not_root = non_rootAssess.is_root() #false
		def_root = assess.is_root() #true
		
		assess.is_root.assertNotEqual(not_root, def_root)
		
	def test_get_aggregator(self):
		assess = AggregateAssessment()
		assess = MagicMock()
		
		assess.choose_aggregator(1)
		copy = assess.get_aggregator()
		
		assess.get_aggregator.assertEqual(assess, copy)
		
		
	def test_choose_aggregator(self):
		assess = AggregateAssessment()
		assess2 = AggregateAssessment()
		
		assess = MagicMock()
		assess2 = MagicMock()
		
		assess.choose_aggregator(1)
		assess2.choose_aggregator(2)
		
		first = assess.get_aggregator_name()
		second = assess2.get_aggregator_name()
		
		assess.choose_aggregator.assertNOtEqual(first, second)

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
		
	def test_checkStatus(self):
		session = Sessions()
		session.checkStatus = MagicMock(return_value = 1)
		session.checkStatus()
		session.checkStatus.assert_return_value(1)
		
	def test_addStudent(self):
		session = Sessions()
		session.addStudent = MagicMock()
		session.addStudent("12094847")
		session.addStudent.assert_called_once_with("12094847")
		
	def test_deleteStudent(self):
		session = Sessions()
		session.addStudent = MagicMock()
		session.addStudent("12345678")
		session.addStudent.assert_called_once_with("12345678")
		
	def test_addMarker(self):
		session = Sessions()
		session.addMarker = MagicMock()
		session.addMarker("12345678")
		session.addMarker.assert_called_once_with("12345678")
		
	def test_deleteMarker(self):
		session = Sessions()
		session.deleteMarker = MagicMock()
		session.deleteMarker("12345678")
		session.deleteMarker.assert_called_once_with("12345678")
		
	def test_getAssessmentname(self):
		session = Sessions()
		session.getAssessmentname = MagicMock(return_value = "Practical 1")
		session.getAssessmentname()
		session.getAssessmentname.assert_return_value("Practical 1")
		
	def test_setAssessmentname(self):
		session = Sessions()
		session.setAssessmentname = MagicMock()
		session.setAssessmentname("Practical2")
		session.setAssessmentname.assert_called_once_with("Practical2")
		
	def test_deleteSessions(self):
		models.deleteSessions = MagicMock()
		models.deleteSessions()
		models.deleteSessions.assert_called_once_with()
		
	def test_insertSessions(self):
		#insertSession = MagicMock()
		assessment = Assessment()
		module = Module()
		
		module.insertModule = MagicMock()
		assessment.insertAssessment = MagicMock()
		models.insertSessions = MagicMock()
		
		module.insertModule("COS 301")
		assessment.insertAssessment("practical1", "30", "type",module)
		models.insertSessions("Pract1Session1",assessment,"2014-06-06 12:00:00","2014-06-07 12:04:00")
		models.insertSessions.assert_called_once_with("Pract1Session1",assessment,"2014-06-06 12:00:00","2014-06-07 12:04:00")
		
	def test_getSessions(self):
		models.getSessions = MagicMock()
		models.getSessions()
		models.getSessions.assert_called_once_with()
		
	def test_getSessionsbyID(self):
		assessment = Assessment()
		session = Sessions()
		models.getSessions = MagicMock(return_value = session)
		models.getSessions(assessment)
		models.getSessions.assert_called_once_with(assessment)
		models.getSessions.assert_return_value(session)


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


class TestMarkAllocation(unittest.TestCase):
	def test_setcomment(self):
		mark = MarkAllocation()
		mark.setcomment = MagicMock()
		mark.setcomment("mark added")
		mark.setcomment.assert_called_once_with("mark added")
		
	def test_setLAssessment(self):
		mark = MarkAllocation()
		assessment = LeafAssessment()
		mark.setLAssessment = MagicMock()
		mark.setLAssessment(assessment)
		mark.setLAssessment.assert_called_once_with(assessment)
		
	def test_setmarker(self):
		mark = MarkAllocation()
		mark.setmarker = MagicMock()
		mark.setmarker("mamelo")
		mark.setmarker.assert_called_once_with("mamelo")
		
	def test_setstudent(self):
		mark = MarkAllocation()
		person = Person()
		mark.setstudent = MagicMock()
		mark.setstudent(person)
		mark.setstudent.assert_called_once_with(person)
		
	def test_getLAssessment(self):
		mark = MarkAllocation()
		assessment = Assessment()
		mark.getLAssessment = MagicMock(return_value = assessment)
		mark.getLAssessment()
		mark.getLAssessment.assert_return_value(assessment)
		
	def test_getstudent(self):
		mark = MarkAllocation()
		person = Person()
		mark.getstudent = MagicMock(return_value = person)
		mark.getstudent()
		mark.getstudent.assert_return_value(person)
		
	def test_settimeStamp(self):
		mark = MarkAllocation()
		mark.settimeStamp = MagicMock()
		mark.settimeStamp("2014-06-06 12:00:00")
		mark.settimeStamp.assert_called_once_with("2014-06-06 12:00:00")
		
	def test_getcomment(self):
		mark = MarkAllocation()
		mark.getcomment = MagicMock(return_value = "mark addad")
		mark.getcomment()
		mark.getcomment.assert_return_value("mark addad")
		
	def test_getmarker(self):
		mark = MarkAllocation()
		mark.getmarker = MagicMock(return_value = "mamelo")
		mark.getmarker()
		mark.getmarker.assert_return_value("mamelo")
		
	def test_gettimeStamp(self):
		mark = MarkAllocation()
		mark.gettimeStamp = MagicMock(return_value = "2014-06-06 12:00:00")
		mark.gettimeStamp()
		mark.gettimeStamp.assert_return_value("2014-06-06 12:00:00")
		
	def test_insertMarkerAllocation(self):
		assessment = LeafAssessment()
		models.insertMarkAllocation = MagicMock()
		models.insertMarkAllocation("mark entered", "2014-06-06 12:00:00",assessment)
		models.insertMarkAllocation.assert_called_once_with("mark entered", "2014-06-06 12:00:00",assessment)
		
	def test_getMarkAllocation(self):
		models.getMarkAllocation = MagicMock()
		models.getMarkAllocation()
		models.getMarkAllocation.assert_called_once_with()
		
	def test_getMarkAllocation(self):
		mark = MarkAllocation()
		models.getMarkAllocation = MagicMock(return_value = mark)
		models.getMarkAllocation(1)
		models.getMarkAllocation.assert_called_once_with(1)
		models.getMarkAllocation.assert_return_value(mark)
		
	def test_deleteMarkAllocation(self):
		models.deleteMarkAllocation = MagicMock()
		models.deleteMarkAllocation()
		models.deleteMarkAllocation.assert_called_once_with()
		
class TestAllocatePerson():
	def test_is_Student(slef):
		alloc = AllocatePerson()
		alloc.is_Student = MagicMock(return_value = 1)
		alloc.is_Student()
		alloc.is_Student.assert_return_value(1)
		
	def test_is_Marker(self):
		alloc = AllocatePerson()
		alloc.is_Marker = MagicMock(return_value = 1)
		alloc.is_Marker()
		alloc.is_Marker.assert_return_value(1)
		
	def test_getID(self):
		alloc = AllocatePerson()
		alloc.getID = MagicMock()
		alloc.getID()
		alloc.getID.assert_called_once_with()
		
	def test_getSessionID(self):
		alloc = AllocatePerson()
		sess = Sessions()
		
		alloc.getSessionID = MagicMock(return_value = sess)
		alloc.getSessionID()
		alloc.getSessionID.assert_return_value(sess)
		
	def test_getPersonId(self):
		alloc = AllocatePerson()
		person = Person()
		
		alloc.getPersonID = MagicMock(return_value = person)
		alloc.getPersonID()
		alloc.getPersonID.assert_return_value(person)
		
	def test_set_isStudent(self):
		alloc = AllocatePerson()
		alloc.set_isStudent = MagicMock()
		alloc.ste_isStudent(1)
		alloc.set_isStudent.assert_called_once_with(1)
		
	def test_set_isMarker(self):
		alloc = AllocatePerson()
		alloc.set_isMarker = MagicMock()
		alloc.ste_isMarker(1)
		alloc.set_isMarker.assert_called_once_with(1)
		
	def test_set_personID(self):
		alloc = AllocatePerson()
		person = Person()
		
		alloc.set_personID = MagicMock()
		alloc.set_personID(person)
		alloc.set_personID.assert_called_once_with(person)
		
	def test_set_sessionID(self):
		alloc = AllocatePerson()
		session = session()
		alloc.set_sessionID = MagicMock()
		alloc.set_sessionID(session)
		alloc.set_sessionID.assert_called_once_with(session)
		
	def test_insertPersonToSession(self):
		person = Person()
		session = Sessions()
		models.insertPersonToSession = MagicMock()
		models.insertPersonToSession(person,session,1,0)
		models.insertPersonToSession.assert_called_once_with(person,session,1,0)
		
	def test_getAllocatedPersonbyID(self):
		alloc = AllocatedPerson()
		models.getAllocatedPerson = MagicMock(return_value = alloc)
		models.getAllocatedPerson(1)
		models.getAllocatedPerson.assert_called_once_with(alloc)
		
	def test_getAllocatedPerson(self):
		models.getAllocatedPerson = MagicMock()
		models.getAllocatedPerson()
		models.getAllocatedperson.assert_called_once_with()
		
	def test_deleteAllcoatedPerson(self):
		models.deleteAllocatedPerson = MagicMock()
		models.delelteAllocatedPerson(1)
		models.deleteAllocatedPerson.assert_called_once_with(1)
		
class TestLeafAssessment(unittest.TestCase):
	def test_get_full_marks(self):
		leaf = LeafAssessment()
		leaf.get_full_marks = MagicMock(return_value= 20)
		leaf.get_full_marks()
		leaf.get_full_marks.assert_return_value(20)
		
	def test_set_full_marks(self):
		leaf = LeafAssessment()
		leaf.set_full_marks = MagicMock()
		leaf.set_full_marks(15)
		leaf.set_full_marks.assert_called_once_with(15)
		
	def test_award_mark(self):
		leaf = LeafAssessment()
		leaf.award_mark = MagicMock()
		leaf.award_mark(10)
		leaf.award_mark.assert_called_once_with(10)
		
	def test_get_awarded_mark(self):
		leaf = LeafAssessment()
		leaf.get_awarded_mark = MagicMock(return_value = 10)
		leaf.get_awarded_mark()
		leaf.get_awarded_mark.assert_return_value(10)
		
	def test_createLeafAssessment(self):
		models.createLeafAssessment = MagicMock()
		models.createLeafAssessment("task 1",0,20)
		models.createLeafAssessment.assert_called_once_with("task 1",0,20)
		
	def test_deleteLeafAssessment(self):
		models.deleteLeafAssessment = MagicMock()
		models.deleteLeafAssessment()
		models.deleteLeafAssessment.assert_called_once_with()
		
	def test_getLeafAssessment(self):
		models.getLeafAssessment = MagicMock()
		models.getLeafAssessment()
		models.getLeafAssessment.assert_called_once_with()


'''
=============End models===========
======================================
'''
    
    
'''
=============Testing api===========
===================================
'''
class ApiTestCase(unittest.TestCase):
	
	def test_getAllModules(self):
		module = Module()
		api.getAllModules = MagicMock(return_value = module)
		api.getAllModules()
		api.getAllModules.assert_return_value(module)
		
	def test_getpersonListFromArrayList(self):
		list = ["12345678", "13245678"]
		person1 = Person()
		person2 = Person()
		person = [person1,person2]
		api.getpersonListFromArrayList = MagicMock(return_value=person)
		api.getpersonListFromArrayList(list)
		api.getpersonListFromArrayList.assert_called_once_with(list)
		api.getpersonListFromArrayList.assert_return_value(person)
		
	def test_getAllLecturesOfModule(self):
		person1 = Person()
		person2 = Person()
		person = [person1,person2]
		api.getAllLecturesOfModule = MagicMock(return_value = person)
		api.getAllLecturesOfModule("cos 301")
		api.getAllLecturesOfModule.assert_called_once_with("cos 301")
		api.getAllLecturesOfModule.assert_return_value(person)
		
	def test_getAllStudentsOfModule(self):
		person1 = Person()
		person2 = Person()
		person = [person1,person2]
		api.getAllStudentsOfModule = MagicMock(return_value=person)
		api.getAllStudentsOfModule("cos 212")
		api.getAllStudentsOfModule.assert_called_once_with("cos 212")
		api.getAllStudentsOfModule.assert_return_value(person)
		
	def test_getAllTeachingAssistanceOfModule(self):
		person1 = Person()
		person2 = Person()
		person = [person1,person2]
		api.getAllTeachingAssistanceOfModule = MagicMock(return_value=person)
		api.getAllTeachingAssistanceOfModule("cos 212")
		api.getAllTeachingAssistanceOfModule.assert_called_once_with("cos 212")
		api.getAllTeachingAssistanceOfModule.assert_return_value(person)
	
	def test_getAllTutorsOfModule(self):
		person1 = Person()
		person2 = Person()
		person = [person1,person2]
		api.getAllTutorsOfModule = MagicMock(return_value=person)
		api.getAllTutorsOfModule("cos 212")
		api.getAllTutorsOfModule.assert_called_once_with("cos 212")
		api.getAllTutorsOfModule.assert_return_value(person)
		
	def test_getAllNamesOf(self):
		person1 = Person()
		person2 = Person()
		person = [person1,person2]
		name = ["mamelo", "koketso"]
		api.getAllNamesOf = MagicMock(return_value = name)
		api.getAllNamesOf(person)
		api.getAllNamesOf.assert_called_once_with(person)
		api.getAllNamesOf.assert_return_value(name)
		
	def test_getAllMarkersOfModule(self):
		list = ["12435687", "13456782"]
		api.getAllMarkerOfModule = MagicMock(return_value = list)
		api.getAllMarkerOfModule("cos 332")
		api.getAllMarkerOfModule.assert_called_once_with("cos 332")
		api.getAllMarkerOfModule.assert_return_value(list)
		
	def test_getAssessment(self):
		assessment = Assessment()
		api.getAssessment = MagicMock(return_value = assessment)
		api.getAssessment()
		api.getAssessment.assert_return_value(assessment)
		
	def test_createLeafAssessment(self):
		assessment = Assessment()
		api.createLeafAssessment = MagicMock()
		api.createLeafAssessment("http://","task 1",assessment,20)
		api.createLeafAssessment.assert_called_once_with("http://","task 1",assessment,20)
		
	def test_getAssessmentForModuleByName(self):
		assessment = Assessment()
		api.getAssessmentForModuleByName = MagicMock(return_value = assessment)
		api.getAssessmentForModuleByName("cos 301", "practical 1")
		api.getAssessmentForModuleByName.assert_called_once_with("cos 301", "practical 1")
		api.getAssessmentForModuleByName.assert_return_value(assessment)
		
	def test_getLeafAssessmentOfAssessmentForModuleByName(self):
		leaf = LeafAssessment()
		api.getLeafAssessmentOfAssessmentForModuleByName = MagicMock(return_value = leaf)
		api.getLeafAssessmentOfAssessmentForModuleByName("cos 301","Practical 1", "task 1")
		api.getLeafAssessmentOfAssessmentForModuleByName.assert_called_once_with("cos 301","Practical 1", "task 1")
		api.getLeafAssessmentOfAssessmentForModuleByName.assert_return_value(leaf)
		
	def test_getAllOpenSessionsForModule(self):
		session = Sessions()
		session1 = Sessions()
		list = [session,session1]
		api.getAllOpenSessionsForModule = MagicMock(return_value = list)
		api.getAllOpenSessionsForModule("COS 332")
		api.getAllOpenSessionsForModule.assert_called_once_with("COS 332")
		api.getAllOpenSessionsForModule.assert_return_value(list)
		
	def test_getAllModulesForStudent(self):
		list = ["COS 332","COS 301","COS 212"]
		api.getAllModulesForStudent = MagicMock(return_value = list)
		api.getAllModulesForStudent("12345678")
		api.getAllModulesForStudent.assert_called_once_with("12345678")
		api.getAllModulesForStudent.assert_return_value(list)
		
	def test_getAllModulesForMarker(self):
		list = ["COS 345","COS 121","COS 301"]
		api.getAllModulesForMarker = MagicMock( return_value = list)
		api.getAllModulesForMarker("12345678")
		api.getAllModulesForMarker.assert_called_once_with("12345678")
		api.getAllModulesForMarker.assert_return_vaule(list)
		
	def test_getAllModulesForLecturer(self):
		list = ["COS 332", "COS 301"]
		api.getAllModulesForLecturer = MagicMock(return_value = list)
		api.getAllModulesForLecturer("12345678")
		api.getAllModulesForLecturer.assert_called_once_with("12345678")
		api.getAllModulesForLecturer.assert_return_value(list)
		
	def test_getAllLeafAssessmentsForAssessment(self):
		leaf1 = LeafAssessment()
		leaf2 = LeafAssessment()
		LObject = [leaf1,leaf2]
		assessment = Assessment()
		api.getAllLeafAssessmentsForAssessment = MagicMock(return_value = LObject)
		api.getAllLeafAssessmentsForAssessment(assessment)
		api.getAllLeafAssessmentsForAssessment.assert_called_once_with(assessment)
		api.getAllLeafAssessmentsForAssessment.assert_return_value(LObject)
		
	def test_getAllAssementsForStudent(self):
		assessment1 = Assessment()
		assessment2 = Assessment()
		list = [assessment1,assessment2]
		api.getAllAssementsForStudent = MagicMock(return_value = list)
		api.getAllAssementsForStudent("12345678","COS 332")
		api.getAllAssementsForStudent.assert_called_once_with("12345678","COS 332")
		api.getAllAssementsForStudent.assert_return_value(list)
		
	def test_getAllSessionsForModule(self):
		sess1 = Sessions()
		sess2 =Sessions()
		list = [sess1,sess2]
		api.getAllSessionsForModule = MagicMock(return_value = list)
		api.getAllSessionsForModule("COS 332")
		api.getAllSessionsForModule.assert_called_once_with("COS 332")
		api.getAllSessionsForModule.assert_return_value(list)
		
	def test_getAllSessionsForAssessment(self):
		ass = Assessment()
		sess1 = Sessions()
		sess2 = Sessions()
		list = [sess1,sess2]
		api.getAllSessionsForAssessment = MagicMock(return_value = list)
		api.getAllSessionsForAssessment(ass)
		api.getAllSessionsForAssessment.assert_called_once_with(ass)
		api.getAllSessionsForAssessment.assert_return_value(list)
		
	def test_createSession(self):
		ass = Assessment()
		api.createSession = MagicMock(return_value = True)
		api.createSession("https://","task1",ass,"2014-06-06 12:00:00","2014-06-10 12:00:00")
		api.createSession.assert_called_once_with("https://","task1",ass,"2014-06-06 12:00:00","2014-06-10 12:00:00")
		api.createSession.assert_return_value(True)
	
	def test_closeSession(self):
		sess = Sessions()
		api.closeSession = MagicMock(return_value = True)
		api.closeSession("https://",sess)
		api.closeSession.assert_called_once_with("https://",sess)
		api.closeSession.assert_return_value(True)
		
	def test_openSession(self):
		sess = Sessions()
		api.openSession = MagicMock(return_value = True)
		api.openSession("https://",sess)
		api.openSession.assert_called_once_with("https://",sess)
		api.openSession.assert_return_value(True)
		
	def test_removeSession(self):
		sess = Sessions()
		api.removeSession = MagicMock(return_value = True)
		api.removeSession("https://",sess)
		api.removeSession.assert_called_once_with("https://",sess)
		api.removeSession.assert_return_value(True)
		
	def test_removeMarkerFromSession(self):
		sess  = Sessions()
		api.removeMarkerFromSession = MagicMock(return_value= True)
		api.removeMarkerFromSession("https://",sess,"12345678")
		api.removeMarkerFromSession.assert_called_once_with("https://",sess,"12345678")
		api.removeMarkerFromSession.assert_return_value(True)
		
	def test_removeMarkerFromModule(self):
		api.removeMarkerFromModule = MagicMock(return_value = True )
		api.removeMarkerFromModule("https://","COS 301","12345678")
		api.removeMarkerFromModule.assert_called_once_with("https://","COS 301","12345678")
		api.removeMarkerFromModule.assert_return_value(True)
		
	def test_login(self):
		list = {"name": "mamelo","surname":"seopela"}
		api.login = MagicMock(return_value = list)
		api.login("https://","12345678","12345")
		api.login.assert_called_once_with("https://","12345678","12345")
		api.login.assert_return_value(list)
		
	def test_getSessionPerson(self):
		person = Person()
		api.getSessionPerson = MagicMock(return_value = person)
		api.getSessionPerson("https://")
		api.getSessionPerson.assert_called_once_with("https://")
		api.getSessionPerson.assert_return_value(person)
		
	def test_setTeachingAssistantForModule(self):
		api.setTeachingAssistantForModule = MagicMock(return_value = True)
		api.setTeachingAssistantForModule("https://","12345678","COS 301")
		api.setTeachingAssistantForModule.assert_called_once_with("https://","12345678","COS 301")
		api.setTeachingAssistantForModule.assert_return_value(True)
		
	def test_setTutorForModule(self):
		api.setTutorForModule = MagicMock(return_value = True)
		api.setTutorForModule("https://","12345678","COS 332")
		api.setTutorForModule.assert_called_once_with("https://","12345678","COS 332")
		api.setTutorForModule.assert_return_value(True)
		
	def test_setMarkerForSession(self):
		sess = Sessions()
		api.setMarkerForSession = MagicMock(return_value = True)
		api.setMarkerForSession("https://","u12345678",sess)
		api.setMarkerForSession.assert_called_once_with("https://","u12345678",sess)
		api.setMarkerForSession.assert_return_value(True)
		
	def test_getOpenSessions(self):
		sess=Assessment()
		ses1 = Sessions()
		ses2 = Sessions()
		list = [ses1,ses2]
		api.getOpenSessions = MagicMock(return_value = list)
		api.getOpenSessions(sess)
		api.getOpenSessions.assert_called_once_with(sess)
		api.getOpenSessions.assert_return_value(list)
		
	def test_getOpenSessionsForMarker(self):
		person = Person()
		ass = Assessment()
		sess1 = Sessions()
		Sess2 = Sessions()
		list = [sess1,Sess2]
		api.getOpenSessionsForMarker = MagicMock(return_value = list)
		api.getOpenSessionsForMarker(ass,person)
		api.getOpenSessionsForMarker.assert_called_once_with(ass,person)
		api.getOpenSessionsForMarker.assert_return_value(list)
		
	
	def test_populateModules(self):
		api.populateModules = MagicMock()
		api.populateModules()
		api.populateModules.assert_called_once_with()
		
	def test_searchBySurname(self):
		per1 = Person()
		per2 = Person()
		list = [per1,per2]
		api.searchBySurname = MagicMock(return_value = list)
		api.searchBySurname("Seopela")
		api.searchBySurname.assert_called_once_with("Seopela")
		api.searchBySurname.assert_return_value(list)
		
	def test_searchByName(self):
		per1 = Person()
		per2 = Person()
		list = [per1,per2]
		api.searchByName = MagicMock(return_value = list)
		api.searchByName("Mamelo")
		api.searchByName.assert_called_once_with("Mamelo")
		api.searchByName.assert_return_value(list)
		
	def test_getSessionByName(self):
		ses1 =Sessions()
		ses2 = Sessions()
		list = [ses1,ses2]
		api.getSessionByName = MagicMock(return_value = list)
		api.getSessionByName("COS 301","TASK 1")
		api.getSessionByName.assert_called_once_with("COS 301","TASK 1")
		api.getSessionByName.assert_return_value(list)
		
	def test_createMarkAllocation(self):
		mark = MarkAllocation()
		leaf = LeafAssessment()
		sess = Sessions()
		per = Person()
		api.createMarkAllocation = MagicMock(return_value = mark)
		api.createMarkAllocation("https://",leaf,sess,"Mamelo",per,"2014-06-06 12:00:00")
		api.createMarkAllocation.assert_called_once_with("https://",leaf,sess,"Mamelo",per,"2014-06-06 12:00:00")
		api.createMarkAllocation.assert_return_value(mark)
		
	def test_updateMarkAllocation(self):
		mark = MarkAllocation()
		api.updateMarkAllocation = MagicMock(return_value = True)
		api.updateMarkAllocation("https://",mark,13)
		api.updateMarkAllocation.assert_called_once_with("https://",mark,13)
		api.updateMarkAllocation.assert_return_value(True)
		
	def test_removeMarkAlloccation(self):
		mark = MarkAllocation()
		api.removeMarkAlloccation = MagicMock(return_value = mark)
		api.removeMarkAlloccation(mark)
		api.removeMarkAlloccation.assert_called_once_with(mark)
		api.removeMarkAlloccation.assert_return_value(True)
		
	def test_removeLeafAssessment(self):
		leaf = LeafAssessment()
		api.removeLeafAssessment =MagicMock()
		api.removeLeafAssessment("https://",leaf)
		api.removeLeafAssessment.assert_called_once_with("https://",leaf)
		
	def test_removeAssessment(self):
		ass = Assessment()
		api.removeAssessment = MagicMock(return_value = True)
		api.removeAssessment("https://",ass)
		api.removeAssessment.assert_called_once_with("https://",ass)
		api.removeAssessment.assert_return_value(True)
		
	def test_getAssessmentFromID(self):
		ass = Assessment()
		api.getAssessmentFromID = MagicMock(return_value = ass)
		api.getAssessmentFromID(1)
		api.getAssessmentFromID.assert_called_once_with(1)
		api.getAssessmentFromID.assert_return_value(ass)
		
	def test_getLeafAssessmentFromID(self):
		leaf = LeafAssessment()
		api.getLeafAssessmentFromID = MagicMock(return_value= leaf)
		api.getLeafAssessmentFromID(1)
		api.getLeafAssessmentFromID.assert_called_once_with(1)
		api.getLeafAssessmentFromID.assert_return_value(leaf)
		
	def test_getMarkAllocationFromID(self):
		mark = MarkAllocation()
		api.getMarkAllocationFromID = MagicMock(return_value= mark)
		api.getMarkAllocationFromID(10)
		api.getMarkAllocationFromID.assert_called_once_with(10)
		api.getMarkAllocationFromID.assert_return_value(mark)
		
	def test_getModuleFromID(self):
		mod = Module()
		api.getModuleFromID = MagicMock(return_value = mod)
		api.getModuleFromID("COS 323")
		api.getModuleFromID.assert_called_once_with("COS 323")
		api.getModuleFromID.assert_return_value(mod)
		
	def test_getSessionsFromID(self):
		sess = Sessions()
		api.getSessionsFromID = MagicMock(return_value = sess)
		api.getSessionsFromID(10)
		api.getSessionsFromID.assert_called_once_with(10)
		api.getSessionsFromID.assert_return_value(sess)
		
	def test_getAuditLogFromID(self):
		act = AuditAction()
		log = AuditLog()
		api.getAuditLogFromID = MagicMock(return_value = log)
		api.getAuditLogFromID(act)
		api.getAuditLogFromID.assert_called_once_with(act)
		api.getAuditLogFromID.assert_return_value(log)
		
	def test_getAuditLogFromAction(self):
		log = AuditLog()
		api.getAuditLogFromAction = MagicMock(return_value = log)
		api.getAuditLogFromAction("deleted")
		api.getAuditLogFromAction.assert_called_once_with("deleted")
		api.getAuditLogFromAction.assert_return_value(log)
		
	def test_getAuditLogFromUsername(self):
		log = AuditLog()
		api.getAuditLogFromUsername = MagicMock(return_value = log)
		api.getAuditLogFromUsername("12345678")
		api.getAuditLogFromUsername.assert_called_once_with("12345678")
		api.getAuditLogFromUsername.assert_return_value(log)
		
	def test_getAuditLogFromTimeRange(self):
		log = AuditLog()
		api.getAuditLogFromTimeRange = MagicMock(return_value = log)
		api.getAuditLogFromTimeRange("2014-01-06 12:00:00","2014-04-04 12:00:00")
		api.getAuditLogFromTimeRange.assert_called_once_with("2014-01-06 12:00:00","2014-04-04 12:00:00")
		api.getAuditLogFromTimeRange.assert_return_value(log)
		
	def test_getAuditLogFromTimeRangeAndUser(self):
		log = AuditLog()
		api.getAuditLogFromTimeRangeAndUser = MagicMock(return_value = log)
		api.getAuditLogFromTimeRangeAndUser("12345678","2014-01-06 12:00:00","2014-04-04 12:00:00")
		api.getAuditLogFromTimeRangeAndUser.assert_called_once_with("12345678","2014-01-06 12:00:00","2014-04-04 12:00:00")
		api.getAuditLogFromTimeRangeAndUser.assert_return_value(log)
		
	def test_getStudentsForASession(self):
		list = ["12345678","13245678"]
		sess=Sessions()
		api.getStudentsForASession = MagicMock(return_value = sess)
		api.getStudentsForASession(sess)
		api.getStudentsForASession.assert_called_once_with(sess)
		api.getStudentsForASession.assert_return_value(list)
		
	def test_addStudentToSession(self):
		sess = Sessions()
		api.addStudentToSession = MagicMock(return_value = True)
		api.addStudentToSession("12345678",sess)
		api.addStudentToSession.assert_called_once_with("12345678",sess)
		api.addStudentToSession.assert_return_value(True)
		
	def test_removeStudentFromSession(self):
		sess = Sessions()
		api.removeStudentFromSession = MagicMock(return_value = sess)
		api.removeStudentFromSession("12345678",sess)
		api.removeStudentFromSession.assert_called_once_with("12345678",sess)
		api.removeStudentFromSession.assert_return_value(True)
		
	def test_getMarkAllocationForLeafOfStudent(self):
		per = Person()
		leaf  = LeafAssessment()
		api.getMarkAllocationForLeafOfStudent = MagicMock(return_value = True)
		api.getMarkAllocationForLeafOfStudent(per,leaf)
		api.getMarkAllocationForLeafOfStudent.assert_called_once_with(per,leaf)
		api.getMarkAllocationForLeafOfStudent.assert_return_value(True)
		
	def test_getSessionForStudentForAssessmentOfModule(self):
		per = Person()
		leaf  = LeafAssessment()
		sess = Sessions()
		api.getSessionForStudentForAssessmentOfModule = MagicMock(return_value = sess)
		api.getSessionForStudentForAssessmentOfModule(per,leaf)
		api.getSessionForStudentForAssessmentOfModule.assert_called_once_with(per,leaf)
		api.getSessionForStudentForAssessmentOfModule.assert_return_value(sess)
		
	def test_getAuditLogFromTableName(self):
		log = AuditLog()
		api.getAuditLogFromTableName = MagicMock(return_value = log)
		api.getAuditLogFromTableName("MarkAllocation")
		api.getAuditLogFromTableName.assert_called_once_with("MarkAllocation")
		api.getAuditLogFromTableName.assert_return_value(log)
		
	def test_logout(self):
		api.logout = MagicMock()
		api.logout("https://")
		api.logout.assert_called_once_with("https://")
		
	def test_getTableAudit(self):
		log1 = AuditLog()
		log2 = AuditLog()
		list = [log1,log2]
		api.getTableAudit = MagicMock(return_value = list)
		api.getTableAudit("MarkAllocation","12345678","2014-01-06 12:00:00","2014-04-04 12:00:00")
		api.getTableAudit.assert_called_once_with("MarkAllocation","12345678","2014-01-06 12:00:00","2014-04-04 12:00:00")
		api.getTableAudit.assert_return_value(list)
		
	def test_getUserTableAudit(self):
		log1 = AuditLog()
		log2 = AuditLog()
		list = [log1,log2]
		per = Person()
		api.getUserTableAudit = MagicMock(return_value = list)
		api.getUserTableAudit(per,"MarkAllocation","12345678","2014-01-06 12:00:00","2014-04-04 12:00:00")
		api.getUserTableAudit.assert_called_once_with(per,"MarkAllocation","12345678","2014-01-06 12:00:00","2014-04-04 12:00:00")
		api.getUserTableAudit.assert_return_value(list)
		
	def test_checkLeafAssessmentExists(self):
		leaf = LeafAssessment()
		api.checkLeafAssessmentExists = MagicMock(return_value = True)
		api.checkLeafAssessmentExists(leaf)
		api.checkLeafAssessmentExists.assert_called_once_with(leaf)
		api.checkLeafAssessmentExists(True)
		
	def test_checkSessionExists(self):
		ses = Sessions()
		api.checkSessionExists =MagicMock(return_value = True)
		api.checkSessionExists(ses)
		api.checkSessionExists.assert_called_once_with(ses)
		api.checkSessionExists.assert_return_value(True)
		
	def test_checkSessionBelongsToAssessment(self):
		ses = Sessions()
		ass = Assessment()
		api.checkSessionBelongsToAssessment = MagicMock(return_value = True)
		api.checkSessionBelongsToAssessment(ses,ass)
		api.checkSessionBelongsToAssessment.assert_called_once_with(ses,ass)
		api.checkSessionBelongsToAssessment.assert_return_value(True)
		
	def test_isStudentInSession(self):
		per = Person()
		ses = Sessions()
		api.isStudentInSession = MagicMock(return_value = True)
		api.isStudentInSession(ses,per)
		api.isStudentInSession.assert_called_once_with(ses,per)
		api.isStudentInSession.assert_return_value(True)
		
	def test_isMarkerInSession(self):
		per = Person()
		ses = Sessions()
		api.isMarkerInSession= MagicMock(return_value = True)
		api.isMarkerInSession(ses,per)
		api.isMarkerInSession.assert_called_once_with(ses,per)
		api.isMarkerInSession.assert_return_value(True)
		
	def test_checkMarkAllocationExists(self):
		per = Person()
		ass = Assessment()
		api.checkMarkAllocationExists = MagicMock(return_value = True)
		api.checkMarkAllocationExists(per,ass)
		api.checkMarkAllocationExists.assert_called_once_with(per,ass)
		api.checkMarkAllocationExists.assert_return_value(True)

	'''def test_getLeafAssessmentOfAssessmentForModuleByName(mod_code, assess_name, leaf_name_):
	    assessment = Assessment()
	    assessment = MagicMock()
	    leaf = LeafAssessment()
	    leaf = MagicMock()
	    leaf.parent = assessment
	    
	
	def test_getAllAssessmentsForModule(mod_code):
	    assess = Assessment()
	    assess = MagicMock()
	def test_getAllOpenAssessmentsForModule(mod_code):
	    pass
	def test_getAllLeafAssessmentsForAssessment(assess_code):
	    pass
	def test_getAllAssementsForStudent(empl_no,mod_code):
	    pass
	def test_getLeafAssessmentMarksOfAsssessmentForStudent(uid, assess_id):
	    pass
	def test_getAllAssessmentTotalsForStudent(uid, mod_code):
	    pass
	def test_getAssessmentTotalForStudent(uid, mod_code, assess_id):
	    pass
	def test_removeLeafAssessment(request,leaf_id):
	    pass
	def test_removeAssessment(request,assess_id):
	    pass
	def test_getAssessmentFromID(row_id):
	    pass
	def test_getLeafAssessmentFromID(row_id):
	    pass
	def test_checkLeafAssessmentExists(leafAssessmentID):
	    pass'''
'''
=============End api tests===========
=====================================
'''


'''
=============Testing views==========
====================================
'''
class ViewsTestCase(unittest.TestCase):
    
    def test_createAssessments(request):
        views.createAssessments = MagicMock(return_value = 200)
        views.createAssessments("https://www.hamster.up.ac.za/createAssessments")
        views.createAssessments.assert_called_once_with("https://www.hamster.up.ac.za/createAssessments")
        views.createAssessments.assert_return_value(200)
        
    def test_assignMarkerInSession(request):
        views.assignMarkerInSession = MagicMock(return_value = 200)
        views.assignMarkerInSession("https://www.hamster.up.ac.za/assignMarkerInSession")
        views.assignMarkerInSession.assert_called_once_with("https://www.hamster.up.ac.za/assignMarkerInSession")
        views.assignMarkerInSession.assert_return_value(200)
        
    def test_awardMark(request):
        views.awardMark = MagicMock(return_value = 200)
        views.awardMark("https://www.hamster.up.ac.za/awardMarck")
        views.awardMark.assert_called_once_with("https://www.hamster.up.ac.za/awardMarck")
        views.awardMark.assert_return_value(200)

    def test_viewAllSessions(request):
        views.viewAllSessions = MagicMock(return_value = 200)
        views.viewAllSessions("https://www.hamster.up.ac.za/viewSessions")
        views.viewAllSessions.assert_called_once_with("https://www.hamster.up.ac.za/viewSessions")
        views.viewAllSessions.assert_return_value(200)
    
    def test_closeSession(request):
        views.closeSession = MagicMock(return_value = 200)
        views.closeSession("https://www.hamster.up.ac.za/closeSessions")
        views.closeSession.asset_called_once_with("https://www.hamster.up.ac.za/closeSessions")
        views.closeSession.assert_return_value(200)

    def test_login(self):
        views.Login = MagicMock(return_value = 200)
        views.Login("https://www.hamster.com/login")
        views.Login.assert_called_once_with("https://www.hamster.com/login")
        views.Login.assert_return_value(200)
    
    def test_CreateSession(self):
        views.CreateSession = MagicMock(return_value = 200)
        views.CreateSession("https://www.hamster.com/createSession")
        views.CreateSession.assert_called_once_with("https://www.hamster.com/createSession")
        views.CreateSession.assert_return_value(200)
    
    def test_AssignStudent(self):
        views.AssignStudent = MagicMock(return_value = 200)
        views.AssignStudent("https://www.hamster.com/AssignStudent")
        views.AssignStudent.assert_called_once_with("https://www.hamster.com/AssignStudent")
        views.AssignStudent.assert_return_value(200)
    
    def test_UpdateMArk(self):
        views.UpdateMArk = MagicMock(return_value = 200)
        views.UpdateMArk("https://www.hamster.com/updateMark")
        views.UpdateMArk.assert_called_once_with("https://www.hamster.com/updateMark")
        views.UpdateMArk.assert_return_value(200)
    
    def test_viewStudentForSession(self):
        views.viewStudentForSession = MagicMock(return_value = 200)
        views.viewStudentForSession("http://www.hamster.com/viewStudentForSession")
        views.viewStudentForSession.assert_called_once_with("http://www.hamster.com/viewStudentForSession")
        views.viewStudentForSession.assert_return_value(200)
'''
=============End views=============
===================================
'''

if __name__ == '__main__':
    unittest.main()