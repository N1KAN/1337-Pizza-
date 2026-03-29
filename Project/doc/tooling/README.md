# Tools used in the project
The following lists the tools and frameworks, that are used in the project. 
- [Docker](https://docs.docker.com/get-started/overview/)    
   Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly. With Docker, you can manage your infrastructure in the same ways you manage your applications. By taking advantage of Docker's methodologies for shipping, testing, and deploying code, you can significantly reduce the delay between writing code and running it in production.
- [Kubernetes](https://kubernetes.io/docs/concepts/overview/)
Kubernetes is a portable, extensible, open source platform for managing containerized workloads and services, that facilitates both declarative configuration and automation.

In a production environment, you need to manage the containers that run the applications and ensure that there is no downtime.

It takes care of scaling and failover for your application, provides deployment patterns, and more.

You can move workloads without having to redesign your applications or completely rework your operational tools.

- [FastAPI](https://fastapi.tiangolo.com/tutorial/)
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints.


- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

It provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.

SQLAlchemy considers the database to be a relational algebra engine, not just a collection of tables.

instead of hiding away SQL and object relational details behind a wall of automation, all processes are fully exposed within a series of composable, transparent tools.
- [FastAPI with SQLAlchemy](https://fastapi.tiangolo.com/tutorial/sql-databases/)
SQLModel is built on top of SQLAlchemy and Pydantic. It was made by the same author of FastAPI to be the perfect match for FastAPI applications that need to use SQL databases.

It combines SQLAlchemy and Pydantic and tries to simplify the code you write as much as possible, allowing you to reduce the code duplication to a minimum, but while getting the best developer experience possible.

- [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
Alembic provides for the creation, management, and invocation of change management scripts for a relational database, using SQLAlchemy as the underlying engine.

It allows developers to manage and apply changes to a database schema over time in a controlled and versioned manner.

- [Swagger UI](https://swagger.io/tools/swagger-ui/)
Swagger UI allows anyone to visualize and interact with the API’s resources without having any of the implementation logic in place.

Swagger UI is an interactive web-based interface that renders OpenAPI (formerly Swagger) specifications, making it easy to visualize and interact with REST APIs

- [Ruff](https://github.com/astral-sh/ruff)

# GitLab CI/CD

The following is a collection of short hints on how to do the most essential things in a GitLab CI/CD pipeline:

- How to delay a job until another job is done: 

  By using the `needs` keyword. Example:
  ```yaml
  job2:
    needs: [job1]
  ```
- How to change the image used in a task: 
    
    Use the `image` keyword in the job:
  ```yaml
  job:
    image: python:3.12
  ```

- How do you start a task manually:

  Use `when: manual`:
  
  ```yaml
  job:
    script: ...
    when: manual
  ```
- The Script part of the config file - what is it good for?
  
  It's where you define the shell commands the job should run.
  ```yaml
  script:
  - echo "Build starts"
  - make build
  ```
- If I want a task to run for every branch I put it into the stage ??
  Commit stage
- If I want a task to run for every merge request I put it into the stage ??
  Acceptance stage
- If I want a task to run for every commit to the main branch I put it into the stage ??
  
  Release stage

# Ruff

- What is the purpose of ruff?  
  ruff is a Python tool that checks code for compliance with Python style conventions (like PEP 8) and detects potential errors.

- What types of problems does it detect ?  
  Python style related problems (e.g. syntax errors).

- Why should you use a tool like ruff in a serious project?  
  ruff should be used in serious projects to avoid committing/merging code with (e.g. syntax) errors to the Production code.

## Run ruff on your local Computer

  It is very annoying (and takes a lot of time) to wait for the pipeline to check the syntax 
  of your code. To speed it up, you may run it locally like this:

### Configure PyCharm (only once)
- find out the name of your docker container containing ruff. Open the tab *services* in PyCharm and look at the container in the service called *web*. The the name should contain the string *1337_pizza_web_dev*.  
- select _Settings->Tools->External Tools_ 
- select the +-sign (new Tool)
- enter Name: *ruff-docker*
- enter Program: *docker*
- enter Arguments (replace the first parameter with the name of your container): 
    *exec -i NAMEOFYOURCONTAINER ruff check --exclude /opt/project/app/api/database/migrations/ /opt/project/app/api/ /opt/project/tests/*
- enter Working Directory: *\$ProjectFileDir\$*

If you like it convenient: Add a button for ruff to your toolbar!
- right click into the taskbar (e.g. on one of the git icons) and select *Customize ToolBar*
- select the +-sign and Add Action
- select External Tools->ruff-docker

### Run ruff on your project
  - Remember! You will always need to run the docker container called *1337_pizza_web_dev* of your project, to do this! 
    So start the docker container(s) locally by running your project
  - Now you may run ruff 
      - by clicking on the new icon in your toolbar or 
      - by selecting from the menu: Tools->External Tools->ruff-docker 

# GrayLog

- What is the purpose of GrayLog?
  - System for collecting and managing logs
  - Real-time analysis of log data
  - Search and filter functions for troubleshooting
  - Alerting -> notifications for specific events


- What logging levels are available?
  - INFO – General runtime information
  - WARNING – Indication of potential issues
  - ERROR – Error that caused part of the program to fail

- What is the default logging level?
  - WARNING

- Give 3-4 examples for logging commands in Python:
  - logging.info('User created with username {}'.format(entity.username))
    - user was successfully created

  - logging.error('User {} not found'.format(user_id))
    - the user with this ID was not found

  - logging.warning('Unusual HTTP response detected for endpoint: {}'.format(endpoint_url))
    - an unusual HTTP response was detected

# SonarQube

- What is the purpose of SonarQube?
  -tool that analyzes your code to detect bugs, code smells, and security vulnerabilities
  -main goal: improve code quality and maintainability throughout the development process

- What is the purpose of the quality rules of SonarQube?
  -quality rules define what SonarQube checks in your code
  -identify bugs, code smells, security vulnerabilities, style violations
  -help maintain clean, safe, and readable code

- What is the purpose of the quality gates of SonarQube?
  -set pass and fail criteria for your code
  -automatically block bad code from being merged or deployed
  -used in CI/CD to ensure only clean code


## Run SonarLint on your local Computer

It is very annoying (and takes a lot of time) to wait for the pipeline to run SonarQube. 
To speed it up, you may first run the linting part of SonarQube (SonarLint) locally like this:

### Configure PyCharm for SonarLint (only once)

- Open *Settings->Plugins*
- Choose *MarketPlace*
- Search for *SonarLint* and install the PlugIn

### Run SonarLint

- In the project view (usually to the left) you can run the SonarLint analysis by a right click on a file or a folder. 
  You will find the entry at the very bottom of the menu.
- To run it on all source code of your project select the folder called *app*

# VPN

The servers providing Graylog, SonarQube and your APIs are hidden behind the firewall of Hochschule Darmstadt.
From outside the university it can only be accessed when using a VPN.
https://its.h-da.io/stvpn-docs/de/ 