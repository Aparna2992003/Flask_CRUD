To set up virtual environment in flask

python3 -m venv venv
source ./venv/bin/activate

To install python3 flask
pip3 install flask

To run server
python3 app.py

For all GET requests type the api endpoint in browser along with the local host details

for PUT requests 
curl -X PUT http://127.0.0.1:5000/put_employee/1 \
     -H "Content-Type: application/json" \
     -d '{"first_name": "Lia",                                  
        "last_name": "Dill",    
        "company_name": "Press",           
        "city": "San Franisco",
        "state": "LA",
        "zip": 95222,
        "email": "lia@hotmail.com",
        "web": "http://www.press.com", 
        "age": 45
    }'

    Exceute the above code in terminal

  for PATCH requests

  curl -X PATCH http://127.0.0.1:5000/patch_employee/1 \
     -H "Content-Type: application/json" \
     -d '{"email" : "dhanush@gmail.com"}'

    Exceute the above code in terminal

    For DELETE requets
    curl -X DELETE http://127.0.0.1:5000/delete_employee/<id> 

  Pagination and limit
curl "http://127.0.0.1:5000/api/users?page=1&limit=2"   


- How long did it take you?
		Two days



- What was most challenging?
	task 1 mostly the pagination task
- What was unclear?
- Task 1 had a lot of parameters to take into consideration so took time to understand

- Any unexpected challenges?
- 

- Is the difficulty appropriate?
- Yes

- Why the chosen tools?
- Since flask is a lightweight framework

- Any assumptions or decisions made?
-
