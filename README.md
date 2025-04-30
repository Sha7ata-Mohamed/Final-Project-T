# final-project-404-not-found
final-project-404-not-found created by GitHub Classroom
# Overview
 - The project is a Website designed to be a quiz for many topic like Python, HTML and Django framework. Users will be able to test their knowledge through various quizzes and track their scores. This is how it will work.
 - Three **DIFFICULTY LEVEL** Easy, Medium and Hard. The user can choose any difficulty level then they will have to choose which topic they want to test their knowledge in. There will be scores for each correct answer
# Requirements 
 - [ ] Setup new project named **Final_Project**
 ### Note do not forget to cd 
 - [ ] Setup new app named **Code_Mix** use this code
 - [ ] Create the models based on ER diagram 
 - [ ] Perform migrations and prepare the database (makemigrations & migrate)
 - [ ] Create the admin based on these models
 - [ ] Create a superuser name **test** email(optional) test@test.com **password** 1234
 - [ ] Create the the questions and the options in the **admin**
 - [ ] Create the views functions
 - [ ] Create a template folder **templates** inside it create a HTML file name it as you like
 - [ ] Create a new URL inside the project & connect the local URL to the new URL
 - [ ] Set up the URLs 
 - [ ] Make sure the data show in the webpage
 - [ ] Create a CSS folder name it **static/css** inside the folder create a file name **style.css**
 - [ ] Search for **How to link a CSS file to HTML file in Django framework**
### Team Roles
 - Project manager: 
    - Abdulrahman-Mohamed
 - Team members: 
    - 1- Abdullah bokubr
    - 2- Mohammad AlBudayeh
### Documentation
 - Name of the project (website): CodeMix
 - There will be two quizzes about Python & HTML programming languages 5 questions for each languages with 4 options for the 1 question
 - There will be 2 level Bronze Master 
 ### Interface
  - Include a welcome phrase
  - Show two options for the Quiz (Which language you want to test your knowledge)
 ### Relationship  
  - It will be one to many meaning 1Q has many options / many options has 1Q 

  ![Image](https://github.com/user-attachments/assets/eb7f647d-3a0b-483e-92f9-1b750c05ab16)
### Bounces
  - I used **Count,Q,ExpressionWrapper and FloatField** to calculate the scores and for calculating the percentage of scores
  - I used **Cast** to from Django ORM to change (convert) the data type of a database field inside a Django query(Display data in a new format without changing it in the database itself.)
  - I used **reverse** Because if I changed The URL patterns later, I don't need to update all the code manually. I only need to update the urls.py, and reverse will still work automatically. 
  **Example**:  instead of typing the URL like this /blog/5/ // I do this (url = reverse('post_detail', args=[5]))
  - I used def **save(self, *args, *kwargs)** 
  args stands for Any **positional arguments** Django sends to .save().
  kwargs stands for Any **keyword arguments** Django sends to .save().
  This helped me with Customizing what happens before/after saving.Also, if I forget to save the Customizations