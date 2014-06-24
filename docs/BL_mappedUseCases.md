#Mapped business logic models to implemented use cases

Below is a list all the use cases that are implemented in the business logic models and the associated
classes used to accomplish them. 

####1. Login Use Case:
Below is a list all the use cases that are implemented in the business logic models and the associated
classes used to accomplish them. 

####1. Login Use Case:
* The Login function is used to capture user’s information and authenticate them against LDAP.

####2. Assessment Management Use Case:
* The module class is used to identify for which module is the assessment for and the assessment class used to manage all assessment available.

####3. Open/Lock Assessment Session Use Case:
* The SessionStatus class is used to open,close and get status of a session.

####4. Create/Modify Assessment Session Use Case:
* The Session class is used for creating, modifying and deleting sessions, assigning Markers and student to the session and uses the assessment class to identify for which assessment the session belongs to.

####5. Create/Modify/Remove Leaf Assessment:
* The LeafAssessment class is used to create, modify and delete a leaf assessment of an assessment.

####6. Create/Modify/Remove Aggregate Assessment Use Case:
* The AggregateAssessment class is used to create, modify and delete an aggregate assessment and the aggregator, SimpleSumAggregator, WeightedSumAggregator, BestOfAggregator are used to set how the aggregate assessment mark should be aggregated.

####7. Marks Management Use Case:
* The MarkAllocation class is use to create , modify and delete marks for an assessment.
