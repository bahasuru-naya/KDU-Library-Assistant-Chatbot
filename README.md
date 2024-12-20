# KDU-Library-Assistant-Chatbot
KDU Library Assistant Chatbot using Rasa, MongoDB, HTML/CSS/JS

# Setup chatbot
### 1. Create new project and virtual environment in your IDE
### 2. Then copy 'requirements.txt' file to your project directory
### 3. Go to the project directory in terminal then run following command to install dependencies in project
```
pip install -r requirements.txt
 ```
### 4. Next create new rasa chatbot using following coomand
```
rasa init
 ```
### 5. Copy and replace files in 'bot' folder to new chatbot
### 6. Train  chatbot using following command
```
rasa train
 ```


# To run  chatbot in terminal
### Run follwing command in terminal 
```
rasa shell
 ```
```
rasa run actions 
 ```

# To run  chatbot in GUI application(socketio)

### Run follwing command in terminal 
```
rasa run -m models --enable-api --cors "*"
 ```
```
rasa run actions 
 ```

### After loading server open index.html in forntend folder

