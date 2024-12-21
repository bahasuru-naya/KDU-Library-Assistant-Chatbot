# KDU-Library-Assistant-Chatbot
### - KDU Library Assistant Chatbot using Rasa, MongoDB, HTML/CSS/JS.
### - Data which use to craete database are found at 'Book.book_data.csv' in 'data' folder. 

# Setup chatbot
### 1. Download or clone repository into your PC
### 2. Create new project and virtual environment in your IDE
### 3. Then copy 'requirements.txt' file to your project directory
### 4. Go to the project directory in terminal then run following command to install dependencies in project
```
pip install -r requirements.txt
 ```
### 5. Next create new rasa chatbot using following command in terminal
```
rasa init
 ```
### 6. Copy and replace files in 'bot' folder into new chatbot
### 7. Train  chatbot using following command
```
rasa train
 ```


# To run  chatbot in terminal
### Run following commands in terminal 
```
rasa shell
 ```
```
rasa run actions 
 ```

# To run  chatbot in GUI application (socketio)

### 1. Run following commands in terminal 
```
rasa run -m models --enable-api --cors "*"
 ```
```
rasa run actions 
 ```

### 2. After loading server open 'chatbot.html' in 'forntend' folder

