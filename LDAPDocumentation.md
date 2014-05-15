LDAP Documentation
==================

#### LDAP API, including what the functions do and what the are called


|Function                   | Description                 | Params                | Return                |
|---------------------------|:---------------------------:|:---------------------:|----------------------:|
|`initialize_ldap`|Creates a simple bind to the LDAP server to prepair for further connections|* LDAP session|Returns an array the information required based on the filter used|
|`authenticateUser`|Binds to the LDAP server, then searches for the passed user details. Then authentication of the user using the password and username pair is done if the user was found in the server.|* request : LDAP Object * username: String * password: String|Not sure yet|
|`getGroups`|An abstract function that is called by other functions with a specific filter such as students in a module or modules being take by a student. It is used to remove duplication of code by doing what every other functions would do.|*filterv: String * username: String |String array|
|`sourceEnrollments`|Returns an array consisting of the modules a student is enroled in.|* username: String|String array|
|`sourceTutorDesignations`|Returns an array consisting of the modules a student is a tutor for.|* username: String|String array|
|`sourceTeachingAssistantDesignations`|Returns an array consisting of the modules a student is a teaching assistant of.|* username: String|String array|
|`sourceLecturerDesignations`|Returns an array consisting of the modules a user is a lectuere of.|* username: String|String array|
|`sourceDemographics`|Returns an array consisting of a user's student number, title, initials, name, surname and email address.|* username: String|String array|
|`constructPersonDetails`|Returns an array consisting of a user's student number, title, initials, name, surname and email address.|* username: String|String array|
|`getAllModuleCodes`|Returns an array consisting of all the modules offered in the department|_None_|String array|
|`getMembers`|Abstract function to be used by other functions in order to curb code duplication retrieves students that apply to the passed filter|* groupName: String|String array|
|`getStudentsOf`|Access the LDAP server to retrieve the students in a module|* groupName: String|String array|
|`getTutorsOf`|Access the LDAP server to retrieve the students that are tutors in a module|* module: String|String array|
|`getTAsOf`|Access the LDAP server to retrieve the students that a teaching assistants in a module|* module: String|String array|
|`getLecturorsOf`|Access the LDAP server to retrieve lecturers of a module|* module: String|String array|
|`findPerson`|Access the LDAP server to retrieve a student using either, the student number, surname or name of the student|* filterName: String * filterValue: String|String array|

Further information will be documented. All functions have been documented, but more information will be added as we go along and changes that might occur.


