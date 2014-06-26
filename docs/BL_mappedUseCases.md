#Mapped business logic models to implemented use cases

Below is a list all the use cases that are implemented in the business logic models and the associated
classes used to accomplish them. 

####1. Login Use Case:
* The Login function is used to capture user’s information and authenticate them against LDAP.

####2. Assessment Management Use Case:
* The module class is used to identify for which module is the assessment for and the assessment class used to manage all assessment available.

####3. Assessment Session Use Case:
* The Session class is used for creating, modifying and deleting sessions, used the allocate person class to identify and keep track of the Markers and student assigned to the session and also uses the assessment class to identify for which assessment the session belongs to and it also specify if an assessment is open or closed.

####5. Create/Modify/Remove Leaf Assessment:
* The LeafAssessment class is used to create, modify and delete a leaf assessment of an assessment and it users the MarkAllocation class to associate a person to a certain mark and keep track of which marker set the ,student mark.

####6. Create/Modify/Remove Aggregate Assessment Use Case:
* The AggregateAssessment class is used to create, modify and delete an aggregate assessment and the aggregator, SimpleSumAggregator, WeightedSumAggregator, BestOfAggregator classes are used to set how the aggregate assessment mark should be aggregated and keeps track of all its leaf assessment.

####7. Marks Management Use Case:
* The leafAssessment class is use to create , modify and delete marks for an assessment.
