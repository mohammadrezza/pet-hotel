**Pet Hotel**

A simple best practice for modern flask application with mongodb.
In this project you can learn how to:
1. work http requests and responses
2. make simple mongodb queries
3. use Jwt for authorization
4. use decorators in python
5. document API's using postman
6. build and deploy service using docker
7. write tests with decent coverage
8. work with external services api like send-in-blue for sending e-mail's
9. write scalable project layout

_Note_: feel free to submit pull requests to.

**1. Requirements**

- Python 3.6 or higher
- Mongodb 3.6 or higher

**2. Setup**

Run commands bellow to set up the project with `virtualenv`

-`git clone https://github.com/mohammadrezza/pet-hotel.git`

-`cd pet-hotel/`

-`sudo apt-get install python3-venv -y`

-`python3 -m venv venv`

-`source venv/bin/activate`

-`(venv) python -m pip install -r requirements.txt`

**3. Run**

_Note_: if the server is running for the first time,
run the `cereate_manager.py` in `scripts` directory.
This will create a manager user and prints out the credentials.
You can change credentials in the script if you want.

- `python scripts/create_manager.py`
```angular2html
Successfully created manager user, credentials:
Email:  manager@gmail.com
Password:  1qaz!QAZ
```

run project :

-`(venv) python wsgi.py`

Sample output:
```angular2html
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 202-050-804
```

_Note:_ if you need to run project in specific environment,
set `FLASK_ENV` before running to one of `dev`, `test` or `prod`.
Default is `dev`.

**4. Test**

Run command below to run all tests in `tests` directory.
- `python -m unittest discover -s tests/ -vvv`

Sample tests output:
```angular2html
test_create_pet (test_pets.TestPets) ... ok
test_delete_pet_by_manager (test_pets.TestPets) ... ok
test_delete_pet_checked_in_by_customer (test_pets.TestPets) ... ok
test_edit_pet (test_pets.TestPets) ... ok
test_get_pets_by_customer (test_pets.TestPets) ... ok
test_get_pets_by_staff (test_pets.TestPets) ... ok
test_pet_check_in_forbidden (test_pets.TestPets) ... ok
test_pet_check_in_full_room (test_pets.TestPets) ... ok
test_pet_check_in_successful (test_pets.TestPets) ... ok
test_pet_check_out (test_pets.TestPets) ... ok
test_create_new_staff_forbidden (test_users.TestUsers) ... ok
test_create_new_staff_successful (test_users.TestUsers) ... ok
test_create_new_staff_unauthorized (test_users.TestUsers) ... ok
test_get_customer_info (test_users.TestUsers) ... ok
test_update_status_successful (test_users.TestUsers) ... ok
test_user_login_block_after_failed_attempts (test_users.TestUsers) ... ok
test_user_login_email_not_exist (test_users.TestUsers) ... ok
test_user_login_invalid_password (test_users.TestUsers) ... ok
test_user_register_successful (test_users.TestUsers) ... ok

----------------------------------------------------------------------
Ran 19 tests in 27.930s

OK

```

**5. Postman**

There is a postman collection exported in json format under `docs` directory
with its environment. Import them in postman and there will be multiple
examples for each request with their responses.

**6. Docker**

-`docker build -t pet-hotel .`

-`docker run -d -p 5000:5000 pet-hotel`