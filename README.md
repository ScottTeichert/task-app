Task Management Application | Applied AI Program Project
Overview

This project is a web-based task management application designed to demonstrate how modern software practices can support structured workflows, user accountability, and secure data management.

The application allows individual users to register, authenticate, and manage their own task portfolios within a controlled environment. It reflects a progression from a simple prototype to a production-ready system, emphasizing sound architecture, data integrity, and operational readiness.

Purpose and Practical Value

At its core, this project explores how lightweight web applications can support operational efficiency in environments that require coordination, tracking, and follow-through. In a higher education context, this type of system could be adapted to support admissions workflows, student outreach tracking, or internal project management.

The design prioritizes:

Clear ownership of work
Controlled access to data
Consistent, structured task tracking
Expandability for future integration with other systems
Key Capabilities
User Authentication and Security
Secure registration and login with hashed passwords and session-based access control.
User-Specific Data Ownership
Each user can only view and manage their own data, reinforcing accountability and privacy.
Full Task Lifecycle Management
Create, view, update, and delete tasks through a clean interface.
API Access for Integration
RESTful endpoints allow task data to be accessed programmatically, enabling future integration with dashboards, reporting tools, or external systems.
Production-Ready Configuration
Environment-based configuration, dependency management, and deployment readiness using a WSGI server.
Technology Approach

The application is built using a pragmatic, widely adopted stack:

Flask for application structure
SQLAlchemy for database management
SQLite for development and PostgreSQL for production
Jinja2 for templating
Gunicorn for deployment

The emphasis is not on novelty, but on applying established tools correctly and cohesively.

Architecture and Design Decisions

Several intentional design decisions guided the development:

Separation of concerns between data, logic, and presentation
Incremental development, evolving from file-based storage to a relational database
Security-first mindset, avoiding plain-text credentials, and restricting data access
Environment-based configuration, enabling portability across local and cloud environments
API layer inclusion, recognizing that modern systems rarely operate in isolation
Deployment and Operational Readiness

The application is structured for deployment on a cloud platform, with:

Externalized configuration via environment variables
Dependency tracking through requirements.txt
Compatibility with WSGI servers for scalable hosting
A production database supporting persistent data storage

All core functionality, including authentication and CRUD operations, is fully operational in a live environment.

Reflection
This project demonstrates the transition from a functional prototype to a system that reflects real-world expectations. The most significant shift was moving beyond “making it work” toward making it secure, maintainable, and deployable.

The result is not just a working application, but a foundation that could be extended into a more robust operational tool with relatively modest additional investment.

Author

Scott Teichert
Senior Director of Admissions
Utah Valley University
Master’s Program in Applied Artificial Intelligence
