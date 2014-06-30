#Mapped business logic models to use cases implementations

Below is a list all the use cases that are implemented in the business logic models and the associated
classes used to accomplish them. 

####1. Login Use Case:
* The Login function (in models) is used to the capture user’s information and authenticate them against LDAP.

####2. Assessment Management Use Case:
* The 'Module' class is used to identify for which module the assessment is for and the 'Assessment' class used to manage all the available 'Assessments'.

####3. Assessment Session Use Case:
* The 'Session' class is used for creating, modifying and deleting sessions, it uses the 'AllocatePerson' class to identify and keep track of the markers and students assigned to the session and also uses the 'Assessment' class to identify for which assessment the session belongs to and it also specifies if an assessment is open or closed.

####5. Create/Modify/Remove Leaf Assessment:
* The 'LeafAssessment' class is used to create, modify and delete leaf assessments of an aggregate assessment.

####6. Create/Modify/Remove Aggregate Assessment Use Case:
* The 'AggregateAssessment' class is used to create, modify and delete aggregate assessments,  and the aggregators 'SimpleSumAggregator', 'WeightedSumAggregator' and 'BestOfAggregator' classes are used to set how marks should be aggregated and keeps track of all its leaf assessments.

####7. Marks Management Use Case:
* The 'LeafAssessment' class manages the marks entered and uses the 'MarkAllocation' class to associate a person to a certain mark and keep track of which marker set the student mark.

####8. AuditLog use case:
* The 'AuditAction' class is used to keep track of the action taken by a user, 'AuditTable' class is used to keep track of which table has been modified, 'AuditTableColumn' class is used to keep track of the table record being modified and the 'AuditLog' class uses all of these tables to keep track of changes that have been made in the database.
