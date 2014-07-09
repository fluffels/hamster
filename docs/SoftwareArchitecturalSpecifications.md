# Architectural Specifications

### Architectural Patterns and Styles
The system will be making use of the multilayered architecture. This is to allow for the separation of concerns of the system through different layers that will be representing different conceptual elements  that make up the entire system.

The benefits of this would be the grouping of elements in layers in order to provide high cohesion and low coupling.

The system will further use the 3-tier architectural pattern in order to group the elements based on the client tier, business tier and database tier. This separation of concern allows for a more robust system that is more manageable and it results in information hiding of lower layers.

The system will also employ the Persistence Framework Architectural Style. This is specifically for persistence in the system, and it will ensure the ability to save objects to a database and retrieve them afterwards, while providing separation of concerns, data hiding, and design for change. This style allows for the use of different database types from different vendors.

We also using the model view controller Architectural pattern through the django framework which will be used to implement the business layer.

### Architectural Tactics and Strategies
We are using the Agile Methodology, specifically, the Scrum method.

We have identified requirements of the system and in the process of prioritizing them with the client in order to add them to the backlog as the issue tracker. We have Sprint planning meetings atleast twice a week based on  our schedules, and prioritize on what to do next. We meet 4 times a week for coding sessions in which we try and accomplish the tasks we have set for ourselves.

### Reference Architectures and Frameworks
The system will use the Multilayered architecture with the Django framework.

The Client layer will make use of the Django REST Framework used for web services

The Database layer will make use of the Django Object Relational Mapper

### Technologies Used
Technologies we will use include, but are not limited to:
* Various Linux distros, Windows 7 and 8,
* Python
* MySQL
* HTML5
* CSS3
* JavaScript
* LDAP
* Django framework
* JQuery
* VirtualBox
* Github
* Microsoft Visio
* Miktex, texmaker
* Twitter's Bootstrap

### Access and Integration Channels
 1. Access to the system will be through:
* mobile devices, and
* web browsers
 2. Integration channel :
* HTTPS for a secure connection,
* SMTP and POP3 for the query system.

Database manager within the persistence pattern will form part of the integration channel that will integrate the database provided in the database tier with the rest of the system.

Integration between the client tier and the business tier is through the web service module.

### Constraints
#### Technological constraints
1. Lack of availability of some technologies on campus computers.
2. University Infrastructure

#### Time constraints
1. Limited amount of time for learning new technologies and using them effectively.

#### Trade-offs
1. Increased amount of technologies and frameworks used results in a more complex and harder to maintain system
