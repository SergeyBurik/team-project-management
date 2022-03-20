# TPMS - team project management system

TPMS is a software development tool used by agile teams. Designed to ease things up for more convenient task tracking and team communication.

## ⚙️ Installation

Make sure you have Python installed ([download](https://www.python.org/downloads/)). Version `3.7` or higher is required.  
Messenger service requires Node.js installed ([download](https://nodejs.org/en/download/)).

```bash
$ pip install -r lamp/requirements.txt
$ (cd webchat && npm install)
```

## ⚡️ Getting started

```bash
# start server
$ python lamp/manage.py runserver

# start messenger server
$ npm start --prefix webchat
```
Application will be available on `localhost:8000`.

## 🎯 Features
* Plan - plan sprints, and distribute tasks across your software team  
* Track - track and observe the progress of completing tasks ???
* Communicate - discuss your team’s work using built-in messenger
* Workflow - Create your own process of shipping projects

## How it works
Application consists of two services: `web app and messenger service`.  
`Web platform` represents a core service with user service and project management. Built on `Python/Django using MySQL`.  
`Messenger service` is a module for web platform. Group chat is being created automatically for each project board. Module uses `Node.js, WebSockets and MongoDB`.  


## License
[MIT](https://choosealicense.com/licenses/mit/)
