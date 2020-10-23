curl -i -H "Content-Type: application/json" -X POST -d {"field1":"value"} resource_curl

curl -i -H "Content-Type: application/json" -X POST resource_url?field1=val1&field2=val2

curl -i -H "Content-Type: application/json" -X POST -d '{"username":"mahesh4@rocks", "email": "mahesh994@gmail.com","password": "mahesh12345", "name":"Mahesh4" }' http://10.1.1.15:5000/api/v1/users

curl -i -H "Content-Type: application/json" -X delete -d '{"username":"manish12345" }' http://localhost:5000/api/v1/users

curl -i -H "Content-Type: application/json" -X PUT -d '{ "password": "ABCDE" }' http://10.1.1.15:5000/api/v1/users/3

curl -i -H "Content-Type: application/json" -X POST -d '{"username":"mahesh4@rocks", "body": "tweets"}' http://10.1.1.15:5000/api/v2/tweets
