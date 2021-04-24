# Deployment

Ilo requires FastAPI and Potion running concurrency to function correctly.

FastAPI can be deployed with multiple different WSGI/ASGI web servers. For an ASGI environment, <a href="https://www.uvicorn.org/">Uvicorn</a> is suggested. <br><br>
For a WSGI environment, <a href="https://docs.pylonsproject.org/projects/waitress/en/latest/">Waitress</a> is recommended.
If you are unsure of which to use, ASGI (<a href="https://www.uvicorn.org/">Uvicorn</a>) is recommended. Additional deployment information can be found <a href="https://fastapi.tiangolo.com/deployment/">here</a>.

FastAPI requires an instance of Cassandra. The Cassandra address and additional information can be configured within the [general config](/ilo/Configurability/#general)

*[WSGI]: Web Server Gateway Interface
*[ASGI]: Asynchronous Server Gateway Interface
