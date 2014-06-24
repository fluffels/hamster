#Web Application
====================
Web Application is concerned with providing the GUI for the web application as well as providing a back-end infrastructure with which the server will communicate. 

Since there is no actual code within the views.py at the moment, the following are descriptions of what the existing functions are supposed to be doing (in our understanding). 

We do not intend for the functions to remain as they are, depending on future decisions we may change the entire structure of how the functions will be named and called. Thus this is a temporary description that will most likely change in the near future.

##Descriptions of back-end functions
-------------------------------------
### `login()`
This function will capture the details entered (username, password, usertype) and send to LDAP to be
authenticated. Appropriate error messages will be displayed for any incorrect input values.

### `homepage()`
This function will load the base template for the entire webpage, this is the landing page for all users.

### `studentReport()`
This function will load the report of a particular student,, at the level of granularity specified. It will load only the details of that student, and works under the assumption that the student has successfully logged in, and their details are captured and stored somewhere in the system.

### `auditReport()`
This function provides information of the audit log within the date-time range specified by the user. This function works under the assumption that only a lecturer is given access to the "button" or "link" that calls that function and that the said lecturer is already logged in and authenticated.

### `marker_home()`
Assumption is that this is the base homepage of a marker after they have logged in. The information available will most probably be that which should not be available to students i.e. information applicable only to markers.

### `assessment_view()`
This is the base page for the assessment page. This page will be viewed by the lecturer, its purpose is to facilitate the lecturer creating assessment sessions and assigning students and markers to sessions.

### `assessment_manager()`
This is the page that will facilitate the organization of assessments within a module. Only lecturers can create assessments, thus this page will be available only to lecturers logged in. 

### `session_manager()`
This page facilitates the managing of sessions for an assessment. Here the lecturer assigns students and markers to an assessment.

### `view_audit_report()`
The page where the audit report response will be displayed, following a request for an audit report.

### `reporting_main()`
The base page for reporting, every user gets redirected to this page when needing to request a report.

### `statistics()`
This is the page that was supposed to display all statistical information requested at a specific level of granularity for an assessment.

### `view_student()`
This page will show all information about a particular student.

### `view_all_students()`
This page will load a list of all registered students for a module.

### `student_report()`
This will load a report on a specific student along with their statistics at a level of granularity specified.

### `marks_management()`
This function loads the marks management page where lecturer willl manage the marks information about a particular assessment.

### `view_course()`
This function takes in the request and course  code and it allows the user to view the assessments available for that particular course.

### `Assessment_Manager()`
This function is the main function called when managing assessments. This is where a lecturer will create, delete and edit the contents of an assessment. (Possibly the page where sessions may be allocated to an assessment as well)




