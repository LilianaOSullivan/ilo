# Architecture

Ilo is powered predominantly by two of the below technologies

* **Python** - FastAPI
* **Elixir** - CowBoy

The Ilo system combines all three above technologies in an encapsulated manner, much as showcased below.
<img src="/img/system_arc.png" style="width:40%;display:block;margin-left: auto;margin-right:auto;">


## Python
Python handles all the 'business' end of the platform. Such as the creation of users or the validation of API keys.

The Python backend is created using <a href="https://fastapi.tiangolo.com/">FastAPI</a>. FastAPI is a high-performance web framework built on Starlette and Pydantic.


## Elixir
Elixir is used as a WebServer for the sending of messages. Elixir is a functional programming language that specialises in concurrency and fault tolerant systems. The WebSocket server is created using CowBoy. Elixir is referenced as *Potion* within the system.


