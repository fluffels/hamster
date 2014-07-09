#Architectural Requirements

###Preface
This document discusses the software architecture requirements that is the requirements around the software infrastructure within which the application functionality is to be developed. The purpose of this infrastructure is to address the non-functional requirements. In particular, the architecture requirements specify:

* the architectural responsibilities which need to be addressed,
* the access and integration requirements for the system,
* the quality requirements, and
* the architecture constraints specified by the client.

###1 Access and integration requirements
####1.1 Access channels
The system will be accessible by human users through the following channels:

1. From a web browser through a rich web interface. The system must
be accessible from any of the widely used web browsers including all
recent versions of Mozilla Firefox, Google Chrome, Apple Safari and
Microsoft Internet Explorer.

Other systems should be able to access the services offered by the system through RESTful web services.

####1.2 Integration channels
This system will be able to access:

1. the CS LDAP server in order to retrieve personal details and class lists,
and
2. the CS MySQL database to access course/module information.

In addition, the system will allow manual integration through importing and exporting of CSV files. In particular, the system will support:

* Importing of assessment entries from CSV files.
* Exporting of mark sheets to CSV files, PDF files and web services.

####1.3 Quality requirements for access and integration channels

* All communication of sensitive data must be done securely using HTTPS.
* Web services should respond within 1 second.
* Exports of documents should be within 5 seconds.
* Personal data such as marks are encrypted.

###2 Architectural responsibilities

The architectural responsibilities include the responsibilities of the architectural requirements the system must support, which are:

|System Requirements|Architectural Responsibility|
|--------------------|--------------------------|
|User can access content through web access channel.|Web interface is separated from logic side, but will allow user full access to information based on user security level through the use of data I/O API and RESTful web services.|
|System will have a host and execution environment.|System will be integrated and hosted on the UP CS department server, with the use of the CS relational courses database and LDAP database.|
|System allows persistence and accessibility of domain objects.| Persistence will be accomplished through the use of an object relational mapper that comes bundled with Django. Domain objects will be accessible through the API in the business logic tier.|
|The system will have an infrastructure for specifying and executing reports.|This will be accomplished through the Django bundled libraries, specifically the CSV library for generating CSV's and the ReportLab library for generating PDF's.|
|System must integrate with LDAP|Integration and authentication will be done using the Django python-ldap library.|
|Audit log needed by the system to keep record of the changes made.|Changes in mark allocations are captured in the CS department database, the log information can only be viewed, and not modified.|

###3 Quality requirements
####3.1 Security
General security considerations:

|Use Case|Pre Condition|Post Condition|
|---------|------------|--------------|
|Access system functionality.|User must be in the CS department LDAP system.|The system should log a user out after a specific amount of time of no interaction with the system.|
|Operations on data (add, edit, and remove).|User must have the correct authorization credentials| The system must make changes to the database,record changes to audit log then notify user that changes have been made, or alternatively raise an exception.|
|Data exchange between entities.|Secure connection via HTTPS| |

####3.2 Auditability
One should be able to query for any entity, any changes made to that entity or any of its components. The information provided must include

* by whom the change was made,
* when the change was made, and
* the new and old value of the field(s) which were changed.

The system will provide only services to extract information from the audit log and will not allow the audit log to be modified.

####3.3 Testability
All services offered by the system must be testable through unit tests which test:

* that the service is provided if all pre-conditions are met (i.e. that no exception is raised except if one of the pre-conditions for the service is not met), and
* that all post-conditions hold true once the service has been provided.

The system should be tested using the Mock library, that comes bundled with Python-Django. The mock objects will test That all modules work as expected The system will go through the following tests.

* acceptance testing,
* integration testing,
* unit testing, and
* regression testing.

Testing of the system should run in less than 2 and a half minutes.

####3.4 Usability
1. Majority of the Computer Science department students, and lecturers should be able to use the system without any prior training, this is due to knowledge of computers. In the case where the system is scaled to other departments, 98% of the students from the other departments must be able to use the system without any prior training.
2. The system must be developed using internationalization in order to support multiple languages. Initially only English needs to be supported, but it must allow for translations to the other oficial languages of the University to be added at a later stage.
3. The system will be developed with the aim of minimizing operations the user needs to do in order to complete a specific task i.e giving the user the ability to add short-cuts to get to a specific task they occasionally make use of.
4. System employs an invalid data capturing feature to prevent users from storing incorrect information.

####3.5 Scalability
1. The deployed system must be able to scale to handle all assessments of all modules of the department of Computer Science.
2. The deployed system must be able to operate effectively under the load of 500 concurrent users.
3. The software architecture should be such that it can, in future, be easily modified to scale to Massive Open Online Courses (MOOC) by porting the system onto clustered and cloud-computing based architectures.

####3.6 Performance requirements
The system does not have particularly stringent performance requirements.

1. All non-reporting operations should respond within less than 1 second.
2. Report queries should be processed in no more than 10 seconds.

###4 Architecture constraints
The following architecture constraints have been introduced largely for maintainability reasons.

####4.1 Technological constraints
  1. The system must be developed using the following technologies
* The system will be developed using the Django web framework.
* Persistence to a relational database must be done using the Object- Relational Mapper bundled with Django.
* The unit tests should be developed using the Django unittest module.
* Web services will use the Django REST framework.
* Android implemented using Twitter bootstraps reactive design framework.

  2. The system must ultimately be deployed onto a Django application server running within the cs.up.ac.za Apache web server.
  3. The system must be decoupled from the choice of database.
  4. The system will use the MySQL database.
  5. The system must expose all system functionality as RESTful web services and hence may not have any application   functionality within the presentation layer.
  6. Web services will be published as RESTful web services.

####4.2 Time constraints
1. The system must be completed, and fully functional before the 20th October 2014
2. The majority of the coding has to be completed between the 22nd of June and 20th of July 2014, this will be a school holiday period.

####4.3 Environmental constraints
1. We do not have access to the labs.

####4.4 Trade-offs
The time we have to develop the system may not be sufficient for implementing additional services.










