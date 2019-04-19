To run the project:
1. Download the project
2. make a virtual environment and install from requirements.txt
3. run python crud.py
4. send the requests using postman

User has following attributes:-
ID
First Name
Last Name
Company Name
Age
City
State
Zip
Email
Web

Application should has following endpoints:-
/api/users - GET - To list the users 
Response with HTTP status code 200 on success


Also, supports some query parameters:-
page - a number for pagination
limit - no. of items to be return, default limit is 5
name - search user by name as substring in First Name or Last Name (Note, use substring matching algorithm/pattern to match the name)
Sort - name of attribute, the items to be sort. By default it returns items in ascending order if  this parameter exist, and if value of parameter is prefix with ‘-’ character, then it should return item in descending order
Sample query endpoint:- /api/users?page=1&limit=10&name=James&sort=-age
This endpoint should return list of 10 users whose first name or last name contains substring given name and sort the users by age in descending order of page 1.



/api/users - POST - To create a new user
Request Payload should be like in json format :-
Response with HTTP status code 201 on success
This endpoint will create a new user inside the database



/api/users/{id} - GET - To get the details of a user
Here {id} will be the id of the user in path parameter 
Response with HTTP status code 200 on success
	


/api/users/{id} - PUT - To update the details of a user
Here {id} will be the id of the user in path parameter 
Request Payload should be like in json format for updating first name, last name and age:-

{
    "first_name": "Josephine",
    "last_name": "Darakjy",
    "age": 48
}
Response with HTTP status code 200 on success



/api/users/{id} - DELETE - To delete the user
Here {id} will be the id of the user in path parameter 
Response with HTTP status code 200 on success
