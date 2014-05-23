# Reporting
=========================================

Reporting is concerned with providing reports for assessments at different levels of granularity. The type of reports that can be requested are:
* Audit reports
* Assessment reports
* Student reports

Reports are in the format of either a csv file or a pdf document. The way in which the classes arestructured suggests that the Factory Method design pattern was used to generate the different types of reports.

## Descriptions of back-end functions/classes
--------------------------------------------------

### class `AssessmentReport()`
Assessment Reports contain variables such as heading, name, data (in the form of an array), averages and standard deviation. The instantiated assessment report object will have getters that can access these variables for the report.

### class `AuditReport()`
Audit reports contain variables such as report name, heading and data. The instantiated object has getters that will access these variables.

### class `StudentMarksReport()`
Student Marks reports contain variables such as name, heading, total  and data. The instantiated object has getters that will access these variables.

### class `Report()`
This class is the abstract class which holds the functions that can be called by the concrete classes AssessmentReport, AuditReport and StudentMarksReport. 
The functions in question are createReport(), average() and stdDeviation(). Like they suggest, these functions create a report, obtain the average mark of a list of marks, and find the standard deviation of those marks respectively.

### class `ReportGenerator()`
This is the abstract Generator that contains functions such as generateAuditReport(), generateStudentReport(), generateAssessmentReport() to generate the relevant reports. The functions themselves have not been implemented and thus return empty strings.

### class `PDFReportGenerator()`
This class provides functions to create a pdf report for the 3 types of reports that are available namely 
generateAssessmentReport(), generateStudentMarksReport(), generateAuditReport. an additional function create_report() exists that is called in either one of the mentioned functions to actually create the report.

### class `CSVReportGenerator()`
This class provides functions to create a csv report for the 3 types of reports that are available namely 
generateAssessmentReport(), generateStudentMarksReport(), generateAuditReport(). an additional function merge() exists that is called in either one of the mentioned functions to append the data within the csv document.

### class `WebReportGenerator()`
This class provides the functions to create a report that will be displayed onto web app. These functions are generateAssessmentReport(), generateStudentMarksReport(), generateAuditReport().

### class `AndroidReportGenerator()`
This class provides the functions to create a report that will be displayed onto the android app. These functions are generateAssessmentReport(), generateStudentMarksReport(), generateAuditReport().

