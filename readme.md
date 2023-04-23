# Stock Price Notifier
A simple project which can send notification to the user on the basis of preferences given by them. It makes use of yahoo finance api to get current price of stock then compares it with user preference and sends notification to the user. The components can be broken down as folows:
### 1. Simple Flask app to record users information and preferences
### 2. Airflow DAGs to schedule the task of comparing and sending notification


# Flask App
It performs following task:

### 1. Provide a form to fill user info and preferences

![](screenshots/form.png?raw=true)

Sores the users preferences in a csv file instead of database. Which seems practical due to nature of application and simplicity of csv 

# Airflow Orchestration

4 different scheduling mechanish is allowed for now namely hourly, daily, weekly and 10mins. A user can selecct one from above in the form.
![](screenshots/home.png?raw=true)

Every DAGs listed above have identical Tasks and their execution procedure. The process of reading content stored in csv processing it to determine need of notification and nitifying the user.

![](screenshots/dag.png?raw=true)


# Problems
### A problem faced was, inability to import or call flask app controller functions from dags directory. Various solutions were tried by adding paths and what not so as a solution ovaral flask project directory was added inside the dags folder which is not a good practice and is to be enhanced further