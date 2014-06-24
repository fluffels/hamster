Android Documentation
=====================

Android API that documents all its functions
--------------------------------------------

| Function name         | Description                    | Parameters          | return            |
| ----------------------|--------------------------------|---------------------|-------------------|
| TimerMethod	       | This function runs the Runnable variable "Time_Tick" |   |  |
| setStopped | It sets the value of the stopped Boolean variable |A boolean value holding the new state of the stopped variable |
| setData    |Sets the the courses that the user is registered for, either as a lecture, tutor or student|
| openSettings| A function used to to redirect the application to the Settings page|
| performLogout|A function used to to redirect the application to the log-in page|
| openHelp|A function used to redirect the application to the Help page|
| performRefresh|A function used to refresh the application|
| setType|The function gets the json and course data passed to the activity and sets them to the type and course variables|
|openViewAssessments|A function used to redirect the application to the Assessment page|
|addAssessment|The function adds a new assessment to the database|A serialAssessment holding a new assessment to be added
|getAssessment|The function gets and return an assessment from the database|An integer holding the id of the assessment required|A serialAssessment holding the assessment required
|getAllAssessments|The function gets all the assessments in the database| | A list of serialAssessmsent holding all the assesment
|getAssessmentsCount|The function counts the number of assessment in the database| |An integer holding the number of assessment count
|updateAssessment|Updating an Assessment in the database|A serialAssessment holding an updated assessment|An integer indicating if the function was successful or not
|deleteAssessment|The function delete an Assessment in the database|A serialAssessment holding an assessment to be deleted
|deletaAllAssessments|The function all the assessment in the database
|setInstance|A function that create the instance of a session(singleton)|A string holding the username, A string holding the password, content holding an intent of the current Activity|A Session containing the instance of a session
|getInstance|The function gets the instance of the session| |An instance of a session
|DeleteSession|This function delete an instance of a session
|getFirstName|The fuction gets the current user's first name| |A string containing the user's name
|isSuccess|check the boolean variable isSet if the login was successfull| | A boolean value, its true if the login was successfull and false if not
|getUID| This function gets the current user ID(employee name)| |A String containing the user ID
|getSTCourses|The function gets all the courses that the user is enrolled for| |An array of string containing the courses
|getLECourses|The function gets all the courses that the user is a lecture for| |An array of string containing the courses
|getTACourses|The function gets all the courses that the user is a tutor for|An array of string containing the courses
|getAssessments|The function gets all the assessment of a course for the current user|A string holding the userID and a string holding the course that its assessment are being retrieved|a courseAsessmemt arrray containing all the assessment of the module
|getStudentsToMark|The function returns all the student that a user (tutor/lecture) is supposed to mark for an assessment|A string containing the user ID, a string containing the course name and a String containing the assessment ID|A student array contain all the student details
|pushMarks|The function pushes edited marks back to web services one at a time or save locally if offline|A serialAssessment holding the assessments whose mark is to be saved|true if pushed online and false if pushed offline
|unsyncedMarksExist|The function Test the database to see if there are any unsynced marks in it(marks that have been saved locally due to no internet access)||true if unsynced marks exist and false otherwise
|saveMarksLocally|This function saves marks locally if device is offline|A serialAssessment holding the assessments whose mark is to be saved
|getUnsyncedMarks|The function gets all of the marks currently in the database| |a serialAssessment array holding all the assessment whose marks are saved locally
|getTaskListByAssessment|The function gets the tasks of an assessment for a specific module|A string holding the module that its assessment task is to be retrieved,a string holding the assessment whose tasks are retrieved and a string holding the student whose assessment is viewed|Task array of all the assessment tasks
|getActiveAssessments|The function gets all the assessment of a module| A string holding the module whose assessment are retrieved|an array of serialSourseAssessment holding all the assessment of the course

