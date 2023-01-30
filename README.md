# ComplaintSystem
## Description
### What the application does?
This is a complaints system API that ensures users, that if there's a problem with something, we can give them a refund. First, to do anything, the 
user have to register or login first. 
Once the user is in, they can create and sent a complaint giving the required details. When the complaint is sent, it is stored, and a pending transaction is 
created with it. Once a complaint is released, it 
must be checked by approver who can either accept or reject it. If he accepts it, then the transaction is activated and the money is fund to the 
user, unless the complaint is rejected. The logged in user can also apply for approver with certificate and if the request is accepted, he will be granted rights to approve other complaints. Besides complainers and reviewers, we also have administrators who also have some functions. They deal specifically 
with the approval of people who want to become approvers. They also have the rights to remove approvers. The admin position is achieved through the ORM 
and there is no backdoor login.

### Used Technologies

#### Flask Framework

I chose `Flask` because of its elasticity and freedom. I wanted to go deeper and I needed to control the architecture completely by myself. 
I mainly used flask-oriented external libraries. For the implementation of the REST concept is used the `Flask-RESTful` library.
#### Database
 For Database I chose `PostgreSQL`, for Migrations I chose `Flask-Migrate` and for ORM I chose
`Flask-SQLAlchemy`. There is a separate table for all types of users. Also have a table for all complaints, for all transfers created, 
and have a table for all users who registered for approvers. About the ralationships, there is `one-to-many` ralationship between complainer table 
and complaint table. Also there is `one-to-one` relationship between transaction table and complaint table and between complainer table and approver 
request table. There is also two Enums, one for user roles (admin, approver, complainer) and one for the complaint's status (pending, approved, rejected).
#### Authorization and Authentication
The REST API also has fully developed authorization and authentication. I used the `PyJWT` and `Flask-HTTPAuth` librarys to create web tokens that have a duration of two days 
and an `HS256 algorithm`. Also, the verify token function has been rewritten, which gives us the possibility in many places to be able to get the given 
user directly by their token. The registration and login endpoints are the only ones that are not secured in any way. All others require a token and a 
specific role. It should be mentioned that each user's password is stored, in the form of a hash, 
and on login the two hashes are compared using `generate_password_hash, check_password_hash` methods from `werkzeug` library.
#### Data Validation- Schemas
For the data validation, I used the `marshmallow` library. Everything that is passed, is checked to the last detail and according to the 
requirements of the models of course. The schemes are divided into request and response, and as here, as everywhere, anything that can be made more 
abstract is added to base classes.
#### Integrations
There are also 3rd party integrations with `Wise` and `AWS S3`. Wise is our payment provider, through which we make a transaction that is put on hold whenever a 
complaint is raised. And with each approved complaint, the transaction is activated and, accordingly, the money is fund to the user. The AWS S3 
is used to store all the images that will be submitted (approver's certificates and complainants' photos). As with the integrations, as in other
places, we have made sure that if something goes wrong, the program will not make records in the database, will not make a transactions, and will 
not upload the photos to the AWS server.
#### Tests
The tests are written using `pytest` library. From `unittest` library, I used `@patch`, for mocking the integrations and other external libraries like `uuid`, 
also for the tokens. For the tests, I have also used `factory-boy` to create objects in the database that come with different data and attributes 
each time they are created. Of course, the tests have their own environment, which also requires its own database. It is important to mention that 
a new database is created for each individual test, and after the completion of the particular test, the database is dropped. And so for every single 
test. I've tried to cover most of the edge cases and in general the tests will pretty much ensure that the things done now will not break 
the moment we write something new.

## REST API

### Register

#### Example Request
```
curl -X POST /complainer_register
     -H "Content-Type: application/json" \
     -d'{
        "first_name": "Example",
        "last_name": "Example",
        "email": "example@mail.com",
        "phone": "+00000000000000",
        "password": "SomePass5",
        "sort_code":231470,
        "account_number":28821822,
       }'
```

#### Example Response
```
HTTP/1.1 201 CREATED
{
  "token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```

#### Data description and validation

| Field            | Requirements                                                                            | Format   |
| ---------------- | --------------------------------------------------------------------------------------  | -------- |
| first_name       | At least 2 letters and containing only letters. Maximum length is 20 letters.           | String   |
| last_name        | At least 2 letters and containing only letters. Maximum length is 20 letters.           | String   |
| email            | Valid Email format and domain.                                                          | String   |
| phone            | Must starts with a "+" symbol and must be 14 characters long without the "+" symbol.    | String   |
| password         | Must contain at least 8 characters, with at least one uppercase letter and one number.  | String   |
| sort_code        | Length must be 6 digits.                                                                | String   |
| account_number   | Length must be 8 digits.                                                                | String   |

### Login
#### Example Request
```
curl -X POST /login
     -H "Content-Type: application/json" \
     -d'{
        "email": "example@mail.com",
        "password": "SomePass5",
       }'
```
#### Example Response
```
HTTP/1.1 200 OK
{
  "token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```

| Field     | Requirements                                                                             | Format   |
| --------- | ---------------------------------------------------------------------------------------- | -------- |
| email     | Valid Email format and domain.                                                           | String   |
| password  | Must contain at least 8 characters, with at least one uppercase letter and one number.   | String   |

### Create Complaint
#### Example Request
`Complainer role required`
```
curl -X POST /make_complaint
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <token>" \
     -d'{
        "title": "ExampleTitle",
        "description": "Example description",
        "photo": "<photo in base64 format>",
        "amount": 10.30,
        "photo_extension": "png"
       }'
```

#### Example Response
```
HTTP/1.1 201 CREATED
{
  "title": "ExampleTitle",
  "photo_url": "<url to s3>",
  "status": "pending",
  "complainer_id": 1,
  "id": 1,
  "amount": 10.30,
  "description": "Example description",
}
```

#### Data description and validation

| Field            | Requirements                                             | Format   |
| ---------------- | -------------------------------------------------------- | -------- |
| title            | Required field with maximum length of 20 letters.        | String   |
| description      | Required field.                                          | Text     |
| photo            | Valid photo in base64 format.                            | Text     |
| amount           | Must be number, bigger than zero.                        | Float    |
| photo_extension  | Valid photo extension.                                   | String   |


### Approve Complaint
#### Example Request
`Approver role required`
```
curl -X PUT /complaint/{complaint_id}/approve
     -H "Authorization: Bearer <token>" \
```

#### Example Response
```
HTTP/1.1 200 OK
{
  204
}
```

### Reject Complaint
#### Example Request
`Approver role required`
```
curl -X PUT /complaint/{complaint_id}/reject
     -H "Authorization: Bearer <token>" \
```

#### Example Response
```
HTTP/1.1 200 OK
{
  204
}
```

### Approver Register
#### Example Request
`Complainer role required`
```
curl -X POST /approver_register
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <token>" \
     -d'{
        "certificate": <photo in base64 format>,
        "certificate_extension": "png"
       }'
```

#### Example Response
```
HTTP/1.1 201 CREATED
{
  "id": 1,
  "certificate": "<url to s3>",
  "complainer_id": 1,
  "status": "pending"
}
```

| Field                  | Requirements                           | Format   |
| ---------------------- | -------------------------------------- | -------- |
| certificate            | Valid photo in base64 format.          | Text     |
| certificate_extension  | Valid photo extension.                 | String   |


### Approve Approver Request
#### Example Request
`Admin role required`
```
curl -X PUT /approver_request/{request_id}/approve
     -H "Authorization: Bearer <token>" \
```

#### Example Response
```
HTTP/1.1 200 OK
{
  204
}
```

### Reject Approver Request
#### Example Request
`Admin role required`
```
curl -X PUT /approver_request/{request_id}/reject
     -H "Authorization: Bearer <token>" \
```

#### Example Response
```
HTTP/1.1 200 OK
{
  204
}
```

### Remove Approver
#### Example Request
`Admin role required`
```
curl -X PUT /remove_approver/{approver_id}
     -H "Authorization: Bearer <token>" \
```

#### Example Response
```
HTTP/1.1 200 OK
{
  204
}
```

### Accessing endpoint without a token

`Valid for all endpoints that require a token`
#### Example Request
```
curl -X PUT /complaint/{complaint_id}/reject
```

#### Example Response
```
HTTP/1.1 401 UNAUTHORIZED
{
  "message": "Token Required"
}
```

### Accessing endpoint with invalid a token
`Valid for all endpoints that require a token`
#### Example Request
```
curl -X PUT /complaint/{complaint_id}/reject
     -H "Authorization: Bearer <invalid token>" \
```

#### Example Response
```
HTTP/1.1 401 UNAUTHORIZED
{
  "message": "Invalid Token"
}
```
### Accessing endpoint with expired a token
`Valid for all endpoints that require a token`
#### Example Request
```
curl -X PUT /complaint/{complaint_id}/reject
     -H "Authorization: Bearer <expired token>" \
```

#### Example Response
```
HTTP/1.1 401 UNAUTHORIZED
{
  "message": "Expired Token"
}
```
### Accessing endpoint without expected role
`Valid for all endpoints that require a role`
#### Example Request
```
curl -X PUT /complaint/{complaint_id}/reject
     -H "Authorization: Bearer <token>" \
```

#### Example Response
```
HTTP/1.1 403 FORBIDEN
{
  "message": "Permission denied"
}
```
### Passed wrong data
`Valid for all endpoints that require data`

#### Example Request
```
curl -X POST /complainer_register
     -H "Content-Type: application/json" \
     -d'{
        "first_name": "",
        "email": "examplemail.com",
        "phone": "+000000000",
        "password": "somePass",
        "sort_code":231,
        "account_number":28821,
       }'
```

#### Example Response
```
HTTP/1.1 400 BAD REQUEST
{
  "message": {
        "email": [
            "Not a valid email address."
        ],
        "last_name": [
            "Missing data for required field."
        ],
        "unknown": [
            "Unknown field."
        ],
        "first_name": [
            "Min length is 2 letters"
        ],
        "password": [
            "Invalid Password"
        ],
        "phone": [
            "The phone number should to be 14 symbols"
        ],
        "sort_code": [
            "The sort code should be 6 digits long"
        ]
    }
}
```

