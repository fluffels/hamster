# Vision and Scope
----------------------------------

### **Background**

Lecturers make use of assistant lecturers and higher-level students to mark
assessments like practicals, assignments, tests and exams. The management
of marking sheets, collection, query response, aggregation and publication
of marks currently results in a lot of manual labour. This is not only very
inefficient, but may also result in integrity issues with lost marks and in er-
rors being introduced during the collection and importing of marks as well
as privacy issues with marks being, at times, visible to fellow students. The
above inefficiencies and other problems have led Jan Kroeze to propose a
marks management system which can be accessed from mobile devices and
web browsers.

### **Vision and Scope**

The proposed system is a mark collection, aggregation and publication system which will allow lecturers to:

* maintain course information,
* manage assessments,
* manage marks,
* reporting, and
* deal with queries.

In particular, the system will allow 

*administrators to download and update information around courses from the CS systems, including the lecturers, teaching assistants and students for a course

* lecturers to specify atomic leaf assessments (assessments which are given a single,atomic mark, like a question for a test or a practical which is assigned a single atomic mark in the assessment system) and how these assessments are to be aggregated into higher level assessments (e.g. how the questions are aggregated into a test mark and how the test and practical marks are aggregated into a semester mark); create assessment sessions with students and markers assigned to these sessions; publish leaf and aggregated marks and generate assessment reports at any level of aggregation as well
as audit reports and have these rendered either onto the screen, onto a PDF document or onto a CSV file for subsequent importing into a spreadsheet or a database.

* markers who have been assigned to mark leaf assessments of certain students to submit, modify or remove marks

* students retrieve their marks for an assessment at any level of aggregation and have these rendered either onto the screen, onto a PDF document or onto a CSV file for subsequent importing into a spreadsheet or a database. 

### **Nice-To-Have's**

Provided the outlined requirements are fulfilled early and there is time on our hands, we will try to add some of the following features to the system:

* The system will be pluggable into other departments in the University of Pretoria through changing the LDAP server used and the Course database.
* The web interface will be implemented with a dynamic loading web page
