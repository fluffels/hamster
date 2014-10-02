from __future__ import division
import time                     
import datetime
import json
import __builtin__
import __future__
from operator import itemgetter
from django.db import models
from django.http import HttpResponse
from polymorphic import PolymorphicModel
from django.utils import timezone
from django.contrib.auth.models import Group

from ldap_interface.ldap_api import *

def login(request, username, password):
  personInfo = authenticateUser(username, password)
  
def getSessionPerson(request) :
  information = request.session["user"]
  return getPersonFromArr(information)

def getPersonFromArr(uid) :
  person = sourceDemographics(uid)
  print person
  
  '''
  information = request.session["user"]
  
  objPerson = Person(data["cn"],data["sn"],data["uid"])
  
  for x in data["studentOf"] :
    sessionPerson.studentOfInsert(item[x])
  
  for x in data["tutorFor"] :
    sessionPerson.tutorOfInsert(x)
  
  for x in data["teachingAssistantOf"] :
    sessionPerson.teachingAssistantOfInsert(x)
  
  for x in data["lectureOf"] :
    sessionPerson.lectureOfInsert(x)
  '''
  return person

class Aggregator(PolymorphicModel):
    aggregator_name = models.CharField(max_length=65)
    assessment = models.ForeignKey('Assessment')
  
    def setname(self, name):
      self.aggregator_name = name
      self.save()
 
    def getname(self):
      return self.aggregator_name
    
    def getAssessmentId(self):
      return self.assessment
 
    def __unicode__(self):
      return self.aggregator_name

def insertSimpleSumAggregator(assess):
  a = SimpleSumAggregator(aggregator_name = 'SimpleSum', assessment=assess)
  a.save()
  
  return a

def insertBestOfAggregator(assess, numC):
  a = BestOfAggregator(aggregator_name = 'BestOf', assessment=assess, numContributors=numC)
  a.save()
  
  return a

def insertWeightedSumAggregator(assess):
  a = WeightedSumAggregator(aggregator_name = 'WeightedSum', assessment=assess)
  a.save()
  
  return a

'''
        BEST-OF AGGREGATOR - FOR STUDENT
'''

class BestOfAggregator(Aggregator):
  numContributors = models.IntegerField()
  
  def aggregateMarksLecturer(self, assess_id, student_id):
    assess_obj = Assessment.objects.get(id=assess_id)
    assess_agg = Aggregator.objects.get(assessment=assess_obj)
    numContributors = assess_agg.numContributors
    children = Assessment.objects.filter(parent=assess_id)
    list_of_children = []
    agg_mark = 0.0
    agg_total = 0
    agg_perc = 0.0
    mod = assess_obj.mod_id
    
    if assess_obj.assessment_type == 'Aggregate':
      for child in children:
          list_of_children.append(aggregateChild(child.id, student_id))
 
      list_of_children.sort(key=lambda x:x[6], reverse=True) 
    
      list_of_chosen_children= []
      for i in range(0,numContributors):
        list_of_chosen_children.append(list_of_children[i])

      for child in list_of_chosen_children:
        agg_mark += child[4]
        agg_total += child[5]
      
      if agg_total == 0:
        print "AGG TOTAL IS 0 MAAAAN"
        agg_total = 1
        
      agg_perc = (agg_mark/agg_total) *100
      
      list =[]
      list.append(assess_obj.id)
      list.append(assess_obj.assess_name)
      list.append(assess_obj.published)
      list.append(assess_obj.assessment_type)
      list.append(agg_mark)
      list.append(agg_total)
      list.append(agg_perc)
      
      return list
    
    elif assess_obj.assessment_type == 'Leaf':
      print "Error, trying best of on a leaf: " +str(assess_obj)
  
  def aggregateMarksStudent(self, assess_id, student_id):
    assess_obj = Assessment.objects.get(id=assess_id)
    assess_agg = Aggregator.objects.get(assessment=assess_obj)
    numContributors = assess_agg.numContributors
    children = Assessment.objects.filter(parent=assess_id)
    list_of_children = []
    agg_mark = 0.0
    agg_total = 0
    agg_perc = 0.0
    mod = assess_obj.mod_id
    
    if assess_obj.assessment_type == 'Aggregate':
      for child in children:
        if child.published == True:
          list_of_children.append(aggregateChild(child.id, student_id)) 
      list_of_children.sort(key=lambda x:x[6], reverse=True) 

      list_of_chosen_children= []
      for i in range(0,numContributors):
        list_of_chosen_children.append(list_of_children[i])

      for child in list_of_chosen_children:
        agg_mark += child[4]
        agg_total += child[5]
      
      if agg_total == 0:
        print "AGG TOTAL IS 0 MAAAAN"
        agg_total = 1
        
      agg_perc = (agg_mark/agg_total) *100
      
      list =[]
      list.append(assess_obj.id)
      list.append(assess_obj.assess_name)
      list.append(assess_obj.published)
      list.append(assess_obj.assessment_type)
      list.append(agg_mark)
      list.append(agg_total)
      list.append(agg_perc)
      
      return list
    
    elif assess_obj.assessment_type == 'Leaf':
      print "Error, trying best of on a leaf: " +str(assess_obj)
  
  def __unicode__(self):
    assess = self.assessment
    return self.aggregator_name + " " + assess.assess_name

def aggregateChild(assess_id, student_id ):
    root = Assessment.objects.get(id=assess_id)
    student_obj = Person.objects.get(upId=student_id)
    if root.assessment_type == 'Aggregate':
      children = Assessment.objects.filter(parent=assess_id)
      sum_agg_of_children = 0.0
      sum_total_of_children = 0
      for child in children:
        if child.assessment_type == 'Leaf':
          try:
            markAlloc = MarkAllocation.objects.get(assessment=child, student=student_obj)
            mark = markAlloc.getMark()
            sum_agg_of_children += mark
            sum_total_of_children += child.full_marks
          except Exception as e:
            print "Exception in aggregateChild - No mark allocation for leaf"
            mark = -1
            sum_agg_of_children = -1
            sum_total_of_children = child.full_marks
        elif child.assessment_type == 'Aggregate':
          sum_agg_of_children += getSumAggOfChildrenForStudent(child.id, student_id)
          sum_total_of_children += getSumTotalOfChildrenForStudent(child.id)
      if sum_total_of_children == 0.0:
        sum_total_of_children = 1
      percentage = (sum_agg_of_children/sum_total_of_children) *100
      list = []
      list.append(root.id)
      list.append(root.assess_name)
      list.append(root.published)
      list.append(root.assessment_type)
      list.append(sum_agg_of_children)
      list.append(sum_total_of_children)
      list.append(percentage)
    else:
      try:
        markAlloc = MarkAllocation.objects.get(assessment=root, student=student_obj)
        mark = markAlloc.getMark()
        total = root.full_marks
        perc = ((mark/total) *100)
      except Exception as e:
        print "Exception in aggregateChild - No mark allocation for leaf root"
        mark = -1
        total = root.full_marks
        perc = -1
      
      list = []
      list.append(root.id)
      list.append(root.assess_name)
      list.append(root.published)
      list.append(root.assessment_type)
      list.append(mark)
      list.append(total)
      list.append(perc)
    return list


'''
          WEIGHTED-SUM AGGGREGATOR - FOR STUDENT
'''
class WeightedSumAggregator(Aggregator):
    def aggregateMarksLecturer(self, assess_id, student_id):
      contributors = []
      root = Assessment.objects.get(id=assess_id)
      children = Assessment.objects.filter(parent=assess_id)
      for child in children:
        child_marks = aggregateChild(child.id, student_id)
        contributors.append(child_marks)
        
      root = Assessment.objects.get(id=assess_id)
      #[id,assess_name,published,type,mark,total,perc]
      totalPerc = 0
      totalTotal = 0
      totalAgg = 0
      for cont in contributors:
        perc = cont[6]
        id_ = cont[0]
        total = cont[5]
        agg = cont[4]
        assess_obj = Assessment.objects.get(id=id_)
        weight = assess_obj.weight
        totalPerc += (weight * perc) #where weight is 0.something
        totalTotal += total
        totalAgg += agg
      
      list =[]
      list.append(root.id)
      list.append(root.assess_name)
      list.append(root.published)
      list.append(root.assessment_type)
      list.append(totalAgg)
      list.append(totalTotal)
      list.append(totalPerc)
      
      return list
    
    def aggregateMarksStudent(self,assess_id, student_id):
      contributors = []
      root = Assessment.objects.get(id=assess_id)
      children = Assessment.objects.filter(parent=assess_id)
      for child in children:
        if child.published == True:
          child_marks = aggregateChild(child.id, student_id)
          contributors.append(child_marks)
        
      root = Assessment.objects.get(id=assess_id)
      #[id,assess_name,published,type,mark,total,perc]
      totalPerc = 0
      totalTotal = 0
      totalAgg = 0
      for cont in contributors:
        perc = cont[6]
        id_ = cont[0]
        total = cont[5]
        agg = cont[4]
        assess_obj = Assessment.objects.get(id=id_)
        weight = assess_obj.weight
        totalPerc += (weight * perc) #where weight is 0.something
        totalTotal += total
        totalAgg += agg
      
      list =[]
      list.append(root.id)
      list.append(root.assess_name)
      list.append(root.published)
      list.append(root.assessment_type)
      list.append(totalAgg)
      list.append(totalTotal)
      list.append(totalPerc)
      
      return list
       
    def __unicode__(self):
      assess = self.assessment
      return self.aggregator_name + " " + assess.assess_name
  
'''
          SIMPLE-SUM AGGREGATOR - FOR STUDENT
'''
class SimpleSumAggregator(Aggregator):
  
  def aggregateMarksLecturer(self,assess_id, student_id ):
    root = Assessment.objects.get(id=assess_id)
    children = Assessment.objects.filter(parent=assess_id)
    sum_agg_of_children = 0.0
    sum_total_of_children = 0

    student_obj = Person.objects.get(upId=student_id)
    if root.assessment_type == 'Aggregate':
      for child in children:
        if child.assessment_type == 'Leaf':
          try:
            markAlloc = MarkAllocation.objects.get(assessment=child, student=student_obj)
            mark = markAlloc.getMark()
            sum_agg_of_children += mark
            sum_total_of_children += child.full_marks
          except Exception as e:
            print "Exception aggregateMarksLecturer - SimpleSum (No mark allocation exists)"
            mark = -1
            sum_agg_of_children = mark
            sum_total_of_children += child.full_marks
  
        elif child.assessment_type == 'Aggregate':
          sum_agg_of_children += getSumAggOfChildrenForStudent(child.id, student_id)
          sum_total_of_children += float(getSumTotalOfChildrenForStudent(child.id))
 
      if sum_total_of_children == 0.0:
        sum_total_of_children = 1.0

      percentage = (sum_agg_of_children/sum_total_of_children) *100
      list = []
      list.append(root.id)
      list.append(root.assess_name)
      list.append(root.published)
      list.append(root.assessment_type)
      list.append(sum_agg_of_children)
      list.append(sum_total_of_children)
      list.append(percentage)
 
    else:
      try:
        markAlloc = MarkAllocation.objects.get(assessment=root, student=student_obj)
        mark = markAlloc.getMark()
        total = root.full_marks
        perc = ((mark/total) *100)
      except Exception as e:
        print "Exception aggregateMarksLecturer - SimpleSum -- Leaf (No mark allocation exists)"
        mark = -1
        total = root.full_marks
        perc = -1
      
      list = []
      list.append(root.id)
      list.append(root.assess_name)
      list.append(root.published)
      list.append(root.assessment_type)
      list.append(mark)
      list.append(total)
      list.append(perc)
    return list
  
     
  def aggregateMarksStudent(self, assess_id, student_id):
    root = Assessment.objects.get(id=assess_id)
    children = Assessment.objects.filter(parent=assess_id)
    sum_agg_of_children = 0.0
    sum_total_of_children = 0

    student_obj = Person.objects.get(upId=student_id)
    if root.assessment_type == 'Aggregate':
      for child in children:
        if child.assessment_type == 'Leaf':
          if child.published == True:
            try:
              markAlloc = MarkAllocation.objects.get(assessment=child, student=student_obj)
              mark = markAlloc.getMark()
              sum_agg_of_children += mark
              sum_total_of_children += child.full_marks
            except Exception as e:
              print "Exception aggregateMarksStudent - SimpleSum (No mark allocation exists)"
              mark = -1
              sum_agg_of_children = mark
              sum_total_of_children = child.full_marks
  
        elif child.assessment_type == 'Aggregate':
          if child.published == True:
            sum_agg_of_children += getSumAggOfChildrenForStudent(child.id, student_id)
            sum_total_of_children += float(getSumTotalOfChildrenForStudent(child.id))
 
      if sum_total_of_children == 0.0:
        sum_total_of_children = 1.0

      percentage = (sum_agg_of_children/sum_total_of_children) *100
      list = []
      list.append(root.id)
      list.append(root.assess_name)
      list.append(root.published)
      list.append(root.assessment_type)
      list.append(sum_agg_of_children)
      list.append(sum_total_of_children)
      list.append(percentage)
 
    else:
      try:
        markAlloc = MarkAllocation.objects.get(assessment=root, student=student_obj)
        mark = markAlloc.getMark()
        total = root.full_marks
        perc = (mark/total)*100
      except Exception as e:
        print "Exception aggregateMarksStudent - SimpleSum--- Leaf (No mark allocation exists)"
        mark = -1
        total = -1
        sum_total_of_children = child.full_marks
  
      list = []
      list.append(root.id)
      list.append(root.assess_name)
      list.append(root.published)
      list.append(root.assessment_type)
      list.append(mark)
      list.append(total)
      list.append(perc)
    return list
  
  def __unicode__(self):
    assess = self.assessment
    return self.aggregator_name + " " + assess.assess_name

def aggregateTotalMarkForLecture( assess_id):
  root = Assessment.objects.get(id=assess_id)
  if root.assessment_type == "Leaf":
    sum_total_of_children = root.full_marks
  else:
    children = Assessment.objects.filter(parent=assess_id)
    sum_total_of_children = 0.0

    for child in children:
      if child.assessment_type == 'Leaf':
        sum_total_of_children += child.full_marks
        
      elif child.assessment_type == 'Aggregate':
        sum_total_of_children += getSumTotalOfChildren(child.id)
        
  return sum_total_of_children
 
def getSumTotalOfChildren(assess_id):
    total =0
    assess = Assessment.objects.get(id=assess_id)
    children = Assessment.objects.filter(parent=assess_id)

    for child in children:
        if child.assessment_type == 'Leaf':
          mark = child.full_marks
          total += mark
        else:
          total += getSumTotalOfChildren(child.id)

    return total

def getSumTotalOfChildrenForStudent(assess_id):
    total =0
    assess = Assessment.objects.get(id=assess_id)
    children = Assessment.objects.filter(parent=assess_id)

    for child in children:
      if child.assessment_type == 'Leaf':
        mark = child.full_marks
        total += mark
      else:
        total += getSumTotalOfChildrenForStudent(child.id)

    return total
  
def getSumAggOfChildrenForStudent(assess_id, student_id):
    student_obj = Person.objects.get(upId=student_id)
    total =0
    assess = Assessment.objects.get(id=assess_id)
    children = Assessment.objects.filter(parent=assess_id)
    
    for child in children:
      if child.assessment_type == 'Leaf':
        try:
          markAlloc = MarkAllocation.objects.get(assessment=child, student=student_obj)
          mark = markAlloc.getMark()
          total += mark
        except Exception as e:
          mark = -1
          total = -1
      else:
        total += getSumAggOfChildrenForStudent(child.id, student_id)
    return total


class Module(models.Model):
    module_code = models.CharField(max_length=6)
    id = models.CharField(max_length = 6, primary_key = True) #module code is used as primary. format COSXXX
    presentation_year = models.DateField(auto_now = True)
    module_name = models.CharField(max_length = 255) #i.e Artificial Intelligence
    
    def getModuleCode(self):
        return self.module_code
    def setModuleCode(self,value):
        self.module_code=value
        self.save()
        
    def setModuleName(self, value):
      self.module_name = value
      self.save()
    
    def getModuleName(self):
      return self.module_name
    
    def __unicode__(self):
        return u'%s %s' %(self.module_code, self.module_name)
      
#===============================Module Function================================

def insertModule(code,name,year,assessments_):
    module = Module(moduleCode=code,moduleName=name,presentationYear=year,assessments=assessments_)
    module.save()
    return module

def getAllModules():
    modules = Module.objects.all()
    return modules

def deleteModule(self):
    Module.delete(self)
    
#===============================End of Module Function================================

class Assessment(PolymorphicModel):
    assess_name = models.CharField(max_length=65)
    published = models.BooleanField()
    mod_id = models.ForeignKey(Module)
    parent = models.IntegerField(null=True, blank=True) #the assess_id of the parent will be passed
    assessment_type = models.CharField(max_length=65)
    isroot = models.BooleanField( default= True) 
    weight = models.FloatField(default=0) #for weighted sum aggregation
    
    def getname(self):
        return self.assess_name
  
    def getpublished(self):
        return self.published
   
    def get_mod_id(self):
        return self.mod_id

    def get_parent(self):
      return self.parent
    
    def set_parent(self,ass_id):
      self.parent = ass_id
      return True
    
    def is_root(self):
      return self.isroot

    def __unicode__(self):
      return self.assess_name
      
#================================Additional Assessment Function===============================
def getAllAssessmentsForModule(module): #returns all the assessments stored in the database
    asses = Assessment.objects.filter(mod_id=module)
    return asses
  
def deleteAssessment(self):
    Assessment.delete(self)

#===================================End of Assessment Function============================

#Inherits from Assessment using django-polymorphism
class AggregateAssessment(Assessment):      
    def get_children(self):
      #make a list of all the children of this assessment and returns that list
      list_ = Assessment.objects.filter(parent=self.id)
      return list_
      
    def get_aggregator_name(self):
      #get the name from the database
      #return self.aggregator_name
      pass
    
    def choose_aggregator(self, aggregatorname_chosen):
      statement = 'Aggregator changed to: '
      if aggregatorname_chosen == 'SimpleSum':
        self.aggregator = SimpleSumAggregator(aggregator_name='SimpleSum')
        statement += 'SimpleSum Aggregator'
        
      elif aggregatorname_chosen == 'BestOf':
        self.aggregator = BestOfAggregator(aggregator_name='BestOf')
        statement += 'BestOf Aggrgator'
        
      elif aggregatorname_chosen == 'WeightedSum':
        self.aggregator = WeightedSeumAggregator(aggregator_name='WeightedSum')
        statement += 'WeightedSum Aggregator'
        
      else:
        statement = 'Was unable to change aggregator'
       
      self.save() 
      return statement
    
    def __unicode__(self):
      return self.assess_name


#================================AggregateAssessment Function============================
def insertAggregateAssessment(name_,published_, module_code, parent_id,assessment_type_,assessment_weight):
  if parent_id is None:
    a = AggregateAssessment(assess_name=name_,assessment_type=assessment_type_,mod_id=module_code, published = published_, weight=assessment_weight)
    a.save()

  else:
    a = AggregateAssessment(assess_name = name_,assessment_type=assessment_type_,mod_id=module_code, published = published_, weight=assessment_weight, parent=parent_id, isroot=False)
    a.save()

  agg = insertSimpleSumAggregator(a)

  return a

def getAggregateAssessmentsForModule(): #gets all aggregate assessments
  aggregate_assessments = AggregateAssessment.objects.all()
  return aggregate_assessments

def deleteAggregateAssessment(self):
  AggregateAssessment.delete(self)

#================================End of AggregateAssessment Function============================

class LeafAssessment(Assessment):
    full_marks = models.IntegerField()
    
    def get_full_marks(self):
      return self.full_marks
    
    def __unicode__(self):
      return self.assess_name

#=================================LeafAssessment Function==============================
def insertLeafAssessment(name_,assessment_type_, module_code, published_, fullMarks_, parent_):
    if parent_ is None:
      a = LeafAssessment(assess_name = name_,assessment_type=assessment_type_, mod_id=module_code, published=published_, full_marks=fullMarks_, weight=0) 
    else:
      a = LeafAssessment(assess_name = name_,assessment_type=assessment_type_, mod_id=module_code, published=published_, full_marks=fullMarks_, parent =parent_,isroot=False, weight=0) 
      
    a.save()
    return a

def deleteLeafAssessment(self):
    LeafAssessment.delete(self)

def getLeafAssessmentsForModule(module):
    leaf = LeafAssessment.objects.filter(mod_id=module)
    return leaf
#=================================End of LeafAssessment Function==============================

class Person(models.Model):
    firstName = models.CharField(max_length = 20, null = False)
    upId = models.CharField(max_length = 9, null = False, unique=True)
    surname = models.CharField(max_length = 30, null = False)
    studentOf_module  = models.ManyToManyField(Module, related_name = 'studentOf_module', blank = True)
    tutorOf_module  = models.ManyToManyField(Module, related_name = 'tutorOf_module', blank = True)
    teachingAssistantOf_module  = models.ManyToManyField(Module, related_name = 'teachingAssistantOf_module', blank = True)
    lectureOf_module = models.ManyToManyField(Module, related_name = 'lectureOf_module', blank = True)
    
    def _init_(self,fn, sn, uid):
            self.firstName = fn
            self.upId = uid
            self.surname = sn
    def getFirstName(self):
            return self.firstName
    def getupId(self):
            return self.upId
    def getSurname(self):
            return self.surname
          
    def setFirstName(self,value):
            self.firstName=value
            self.save()
    def setupId(self,value):
            self.upId=value
            self.save()
    def setSurname(self,value):
            self.surname=value
            self.save()
            
    def lectureOfInsert(self,value):
            self.lectureOf_module.add(value)
            self.save()
    def lectureOfDelete(self,value):
            self.lectureOf_module.remove(value)
            self.save()
            
    def studentOfInsert(self,value):
            self.studentOf_module.add(value)
            self.save()
    def studentOfDelete(self,value):
            self.studentOf_module.remove(value)
            self.save()
            
    def tutorOfInsert(self,value):
            self.tutorOf_module.add(value)
            self.save()
    def tutorOfDelete(self,value):
            self.tutorOf_module.remove(value)
            self.save()
            
    def teachingAssistantOfInsert(self,value):
            self.teachingAssistantOf_module.add(value)
            self.save()
    def teachingAssistantOfDelete(self,value):
            self.teachingAssistantOf_module.remove(value)
            self.save()
    
    def isEnrolled(self, mod_code):
            is_true = studentOf_module.objects.filter(module_id=mod_code)
            if is_true is None:
              return False
            return True
            
    def __unicode__(self):
            return u'%s %s %s' % (self.firstName, self.surname, self.upId)


class Person_data(models.Model):
    uid = models.CharField(max_length = 9,unique = True)
    data = models.TextField()
    
    def setuid(self, value):
      self.uid = value
    def getuid(self):
      return self.uid
    def setData(self, value):
      data = value
      self.save()
    def getData(self):
      return self.data
    
    class Meta:
      verbose_name_plural = "Person_data"
    
    def __unicode__(self):
      return self.uid
    

#==========================Person_data===============================
def insertPerson_data(upId_,data_):
    session = Person_data(uid=upId_,data=data_)
    session.save()
    return session

def getAllPerson_data():
    person = Person_data.objects.all()
    return person

def deletePerson_data(self):
    Person.delete(self)

#==========================Person_data===============================

class MarkAllocation(models.Model):
    comment =models.TextField()
    student = models.ForeignKey('Person')
    assessment =models.ForeignKey('LeafAssessment') 
    marker = models.CharField(max_length=100)
    timeStamp = models.DateTimeField()
    mark = models.IntegerField(max_length=3)
    
    def setMark(self,value):
      self.mark = value
      self.save()
    def getMark(self):
      return self.mark
    
    def setcomment(self,value):
        self.comment=value
        self.save()
    def setLAssessment(self,value):
        self.assessment = value
        self.save()
    def setmarker(self,value):
        self.marker=value
        self.save()
    def setstudent(self,value):
        self.student=value
        self.save()
    def getLAssessment(self):
        return self.assessment
    def getstudent(self):
        return self.student
    def settimeStamp(self,value):
        self.timeStamp=value
        self.save()
    def getcomment(self):
        return self.comment
    def getmarker(self):
        return self.marker
    def gettimeStamp(self):
        return self.timeStamp
      
    def __unicode__(self):
      return self.marker

#===============================MarkAllocation Function================================
def insertMarkAllocation(L_assessment,mark_,marker_,student_,timeStamp_,comment_):
    markAlloc = MarkAllocation(comment=comment_,marker=marker_,timeStamp=timeStamp_,student=student_,assessment = L_assessment,mark=mark_)
    markAlloc.save()
    return markAlloc

def getMarkAllocation():
    mark_allocation = MarkAllocation.objects.all()
    return mark_allocation
    
def getMarkAllocation(id):
	return MarkAllocation.object.get(assessment = id)

def deleteMarkAllocation(self):
    MarkAllocation.delete(self)

#===============================End of MarkAllocation Function================================

class Sessions(models.Model):
    session_name = models.CharField(max_length=100, null=False)
    assessment_id = models.ForeignKey('Assessment')
    open_time = models.DateTimeField()
    close_time = models.DateTimeField()
    status = models.IntegerField(default = 0)
    
    def checkStatus(self):
        if self.open_time < timezone.now()and self.close_time >= timezone.now():
                self.status = 1
                self.save()
                return self.status
        else:
          self.status = 0
          self.save()
          return self.status

    def setAssessmentID(self,id):
        self.assessment_id = id
        self.save()

    def setOpenedDate(self, date):
        self.open_time = date
        self.save()
    
    def setClosedDate(self, date):
        self.close_time = date
        self.save()
       
    def setOpen(self):
        self.open_time = datetime.datetime.now()
        endDate = self.open_time + datetime.timedelta(days=10)
        self.close_time = endDate
        self.status = 1
        self.save()
    
    def setClose(self):
        self.close_time = datetime.datetime.now()
        self.status = 0
        self.save()
    
    def setName(self,name):
        self.session_name = name
        self.save()
    
    #getters
    def getID(self):
        return self.id
    def getClosedDate(self):
        return self.close_time
    def getOpenedDate(self):
        return self.open_time
    def getAssessmentID(self):
        return self.assessment_id
    def getClosedDate(self):
        return self.closed
    def getStatus(self):
        return self.status
    def getOpenedDate(self):
        return self.opened
    def getName(self):
        return self.session_name
    
    def addStudent(self,studentID):
        insertPersonToSession(studentID,self.ID,1,0)
    
    def deleteStudent(self,value):
        deleteAllocatedPerson(value)
    
    def addMarker(self,markerID):
        insertPersonToSession(markerID,self.ID,0,1)
        
    def deleteMarker(self,vaule):
        deleteAllocatedPerson(value)
        
    def setAssessmentname(self,value):
        self.assessmentname=value
        self.save()
    def getsessionStatus(self):
        return self.status
    def setsessionStatus(self,value):
        self.status=value
        self.save()
    """
    def awardMark(self,value):
        if datetime.datetime.now() >= self.getsessionStatus().getClosed(self):
            self.markallocation.setmark(self,0)
            self.markallocation.setcomment(self,"Assessment session is closed")
            self.markallocation.settimeStamp(self,datetime.datetime.now())
        else:
            self.markallocation=value
     """
     
    class Meta:
      verbose_name_plural = "Sessions"
     
    def __unicode__(self):
          return u'%s' % (self.session_name)

def deleteSessions(self):
	Sessions.delete(self)

def insertSessions(session_name_, assessment_id_,opened_,closed_):
	temp = Sessions(session_name=session_name_,assessment_id=assessment_id_,open_time=opened_,close_time=closed_,status=0)
	temp.save()
	return temp

def getSessions():
	temp=Sessions.objects.all()
	return temp

def getSessions(Id):
	return Sessions.object.get(id= Id)


class AllocatePerson(models.Model):
	person_id = models.ForeignKey('Person')
	session_id = models.ForeignKey('Sessions')
	isStudent = models.BooleanField(default=0)
	isMarker = models.BooleanField(default=0)
	
	def is_Student(self):
		return isStudent
		
	def is_Marker(self):
		return isMarker
		
	def getID(self):
		return self.ID
		
	def getSessionID(self):
		return self.session_id
		
	def getPersonID(self):
		return self.person_id
		
	def set_isStudent(self,bool):
		isStudent = bool
		self.save()
		
	def set_isMarker(self, bool):
		isMarker = bool
		self.save()
		
	def set_personID(self, id):
		person_id = id
		self.save()
		
	def set_sessionID(self, id):
		session_id = id
		self.save()

	def __unicode__(self):
		return 'Allocated person'


#==============================AllocatePerson Function==============================
def insertPersonToSession(personID,sessionID,student,Marker):
	temp = AllocatePerson(person_id = personID, session_id = sessionID,isStudent = student, isMarker = Marker)
	temp.save()
	
def getAllocatedPerson():
	return AllocatePerson.object.all()
	
def getAllocatedPerson(sessionID):
	return AllocatePerson.object.filter(session_id = id)
	
def deleteAllocatedPerson(self):
	AllocatePerson.delete(self)
#==============================End of AllocatePerson Function==============================

#----------------------------------------------------------
#-------------------- Audit tables ------------------------
#----------------------------------------------------------


class AuditLogAssessment(models.Model):
    person_id = models.ForeignKey('Person')
    mod = models.ForeignKey('module')
    assessment = models.CharField(max_length = 50)
    action = models.CharField(max_length=255)
    time = models.DateTimeField()
    old_value = models.CharField(max_length=255,null=True)
    new_value = models.CharField(max_length=255,null=True)
    
    
def insertAuditLogAssessment(person,assess,act,old,new,modl):
  temp = AuditLogAssessment(person_id = person,assessment=assess,action=act,time=datetime.datetime.now(),old_value=old,new_value=new,mod=modl)
  temp.save()
  
class AuditLogSession(models.Model):
  person_id = models.ForeignKey('Person')
  mod = models.ForeignKey('module')
  assessment = models.CharField(max_length=50)
  session = models.CharField(max_length = 50)
  action = models.CharField(max_length=255)
  time = models.DateTimeField()
  old_value = models.CharField(max_length=255,null=True)
  new_value = models.CharField(max_length=255,null=True)
  
def insertAuditLogSession(person,assess,sess,act,old,new,modl):
  temp = AuditLogSession(person_id=person,session=sess,assessment=assess,action=act,time=datetime.datetime.now(),old_value=old,new_value=new,mod=modl)
  temp.save()
  
class AuditLogMarkAllocation(models.Model):
  person_id=models.ForeignKey('Person')
  student = models.CharField(max_length=255)
  mod = models.ForeignKey('module')
  markAllocation = models.ForeignKey('MarkAllocation')
  action = models.CharField(max_length=255)
  time=models.DateTimeField()
  old_value=models.CharField(max_length=255,null=True)
  new_value=models.CharField(max_length=255,null=True)

def insertAuditLogMarkAllocation(person,markalloc,stud,act,old,new,modl):
  temp = AuditLogMarkAllocation(person_id=person,student=stud,markAllocation=markalloc,action=act,time=datetime.datetime.now(),old_value=old,new_value=new,mod=modl)
  temp.save()
  
class AuditLogAllocatePerson(models.Model):
    person_id=models.ForeignKey('Person')
    mod = models.ForeignKey('module')
    allocatePerson = models.CharField(max_length=255)
    session = models.ForeignKey('Sessions')
    action = models.CharField(max_length=255)
    time=models.DateTimeField()
    
def insertAuditLogAllocatePerson(person,student,ses,act,modl):
  temp = AuditLogAllocatePerson(person_id=person,allocatePerson=student,time= datetime.datetime.now(),action=act,session=ses,mod=modl)
  temp.save()



#===================================End of AuditLog functions====================================
#This is to create the table shown in the master specification giving a
#general idea of how their MySQL database table for courses looks like
'''
class Course(models.Model):
    course_code = models.CharField(max_length = 20, null = False)
    name = models.CharField(max_length = 255, null = False)
    lecturer = models.CharField(max_length = 255, null = False, default = 0)
    description = models.TextField(null = True)
    semster = models.SmallIntegerField(max_length = 6, null = False, default = 0)
    has_webct = models.SmallIntegerField(max_length = 4, null = True)
    year_group = models.IntegerField(max_length = 11, null = True)
    hidden = models.SmallIntegerField(null = False, default = 0)
    last_updated = models.DateTimeField(auto_now_add = False, auto_now = True)
    discussion_board = models.SmallIntegerField(max_length = 4, null = True)
    tutors_allowed = models.SmallIntegerField(max_length = 2, null = True)
    
    def __unicode__(self):
        return self.course_code
    
    #Creating Groups for Users
    lecture_user = Group.objects.get_or_create(name='Lecturer Group')
    
    student_user = Group.objects.get_or_create(name='Student Group')
    
    teaching_ass_user = Group.objects.get_or_create(name='Teaching Assistant Group')
    
    tutor_user = Group.objects.get_or_create(name='Tutor Group')
    
    marker_user = Group.objects.get_or_create(name='Marker Group')
'''


