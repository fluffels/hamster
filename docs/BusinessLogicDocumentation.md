BusinessLogicDocumentation
==========================

### This documents only the Business logic API and classes used. It does not document the database API or the 

## API

|Function                   | Description                 | Params                | Return                |
|---------------------------|:---------------------------:|:---------------------:|----------------------:|
|`getAllLecturers`|Retrieves all lecturers in the department|_None_|
|`getAllMarkers`|Retrieves all markers of all modules|_None_|
|`getAllStudents`|Retrieves all students of all modules in the department|_None_|
|`getAllModules`|Retrieves all modules of in the department|_None_|
|`getAllStudentsOfModule`|Retrieves all students enroled for the specified module|+ mod_code : String|
|`getAllMarkersOfModule`|Retrieves all personel who are markers for the specified module|+ mod_code : String|
|`getAllLecturersOfModule`|Retrieves all personel who are lecturers for the specified module|+ mod_code : String|
|`getAllAssessmentsForModule`|Retrieves all assessments created in the module|+ mod_code : String|
|`getAllOpenAssessmentsForModule`|Retrieves all assessments that are available for evauting students on|+ mod_code : String|
|`getAllModulesForStudent`|Retrieves all modules the student is enroled for|+ mod_code : String|
|`getAllModulesForMarker`|Retrieves all modules the person is a marker in|+ mod_code : String|
|`getAllModulesForLecturer`|Retrieves all modules the person is a lecturer in|+ mod_code : String|
|`getAllLeafAssessmentsForAssessment`|Retrieves all leaf assessments associated with an assessment|+ mod_code : String|
|`getAllAssementsForStudent`|Retrieves all assessments a student has access to|+ modcode : String + empl_no : String|
|`getAllAggregatedResultsForStudentOfModule`|Retrieves all aggregated results of module for student|+ modcode : String + empl_no : String + level : String|

## Classes

##### Classes used to access information of users

###### Class : `Module`
###### Methods
1. getModuleCode
2. getModuleCode
3. deleteModule
4. insertModule
5. getModule
6. Assessment
7. setName
8. setWeight
9. setType
10. setModule
11. getID
12. getName
13. getWeight
14. getType
15. getModule
16. deleteAssessment
17. insertAssessment
18. getAssessment

###### Class : `Sessions`
###### Methods : 
1. setAssessmentID
2. setOpenedDate
3. setClosedDate
4. setOpen
5. setClose
6. setName
7. getID
8. getAssessmentID
9. getClosedDate
10. getStatus
12. getOpenedDate
13. deleteSessions
14. insertSessions
15. getSessions
16. StudentSessions
17. getSess_id
18. getStudent_id
19. insertStudentSessions
20. deleteStudentSessions

###### Class : `MarkerSessions`
###### Methods :
1. setMarker
2. setID
3. getMarker
4. getID
5. getSessionID
6. deleteMarkerSessions
7. insertMarkSession
8. getMarkerSessions

###### Class : `MarkerModule`
###### Methods : 
1. deleteMarkerModule
2. insertMarkerModule
3. getMarkerModule

###### Class : `LeafAssessment`
###### Methods : 
1. setName
2. setAssessment_id
3. setMax_mark
4. setPublished
5. getID
6. getName
7. getAssessment_id
8. getMax_mark
9. getPublished
10. deleteLeafAssessment
11. insertLeafAssessment
12. getLeafAssessment

###### Class : `MarkAllocation`
###### Methods : 
1. setLeaf_id
2. setMark
3. setSession_id
4. setMarker
5. setStudent
6. setTimeStamp
7. getID
8. getLeaf_id
9. getMark
10. getSession_id
11. getMarker
12. getStudent
13. getTimeStamp
14. deleteMarkAllocation
15. insertMarkAllocation
16. getMarkAllocation

###### Class `Aggregator`
###### Methods : 
1. aggregateMarks

###### Class `BestOfAggregator`
###### Methods : 
1. aggregateMarks
2. getnumContributors
3. setnumContributors
4. createBestOfAggregator

###### Class `WeightedSumAggregator`
###### Methods : 
1. aggregateMarks
2. insertWeight

###### Class `SimpleSumAggregator`
###### Methods : 
1. aggregateMarks

##### The documented code is still to be modified as the project proceeds. Changes and additions will be added to the documentation, this also includes information pertaining to the above documented API and classes.
