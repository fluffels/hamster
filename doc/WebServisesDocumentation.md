Web Services Documentation
==========================

Web Services API documenting all the functions
----------------

|Function Name        |Description                                    |Parameters             |Resturn             |
|---------------------|-----------------------------------------------|-----------------------|--------------------|
|login|Authenticate users login details|A http request for validation of the users login details|A http responce containing required data if the user was successfuly login and return a confirmation of failer if the user was not successfuly login
|logout|The user is logged out of the  server|A http request to logout the user|A http responce confirming if the user was successfuly logout or not
|getAllMarksForModule|This function gets all the marks of a student for a specific module|The http request containing the user ID and module for which marks are to be retireved|The http responce containing all the modules mark
|getModules|Gets all the modules that the student is registered for|A http Get Request containing the student number|A http Responce containing the modules or a http error "page not found" if there student is not enrolled for any module
|saveMarks|the function saves the mark of the leaf assessment of a certain module|A http request that contains the student number, the course code, the leafAssessment ID and the mark that is to be saved|A http responce confirming if the mark was saved or not
|getStudents|Gets all the student that the user(marker) is supposed to mark fo a certain session|A http request containing the assessmentId and the marker's ID(employee number)|A http responce containing the students data for that session and an error message if not successful
|getTaskListByAssessment|Gets all the leaf Assessment of an assessment for a specific module| A http request containing the module, assessment and  student number for the leafAssessment required|A http responce containing the leaf Assessment and its marks and an error message of not successful
|getActiveAssessments|The function gets all the assessment of a certain module|A http request containing the module whose assessment are to be retrieved|A http responce containing the module's assessment and an error if it was unsuccessful 
|
