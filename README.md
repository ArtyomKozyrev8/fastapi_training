# fastapi_training
This is a pet-project just to learn FastApi and SQL Alchemy

Create db:

`docker run --name fastapi_training_db -p 9798:5432 -e ENCODING=UTF8  -e POSTGRES_PASSWORD=some_pswd -e POSTGRES_USER=some_user -e POSTGRES_DB=fastapi_training_db -d postgres
`
