# API Usage

This section documents the usage of Ilo as a backend; It is highly recommended to have glanced at the [architecture](/ilo/Architecture) section; this section assumes some technical insights of Ilo.

A client must, at minimum, support

* **WebSockets**: This is a requirement for the sending of messages between Potion and the client.
* **JSON Parsing**: The information exchanged within the WebSocket connection is in a JSON format, and as such is essential to the understanding of the information exchanged.

To access public-facing methods, all information is exchanged using an appropriate HTTP method, and a [JSON schema](/ilo/Swagger#json-schema). These are documented within the [Swagger](/ilo/Swagger#json-schema) section.

## Message Sending

To send a message, the following pre-conditions must exist.

* An API Key must be obtained [1](/Development/API Usage/#obtaining-an-api-key)
* A user must be created [2](/Development/API Usage/#user-creation)
* A user must be logged-in [3](/Development/API Usage/#log-a-user-in)

### Obtaining an API Key

An API Key can be obtained by sending a *POST* request to `/key`. The API will reply with a JSON as follows.

```json
{
  "detail": "824a47ae-d0b9-5350-bffb-cc2ee48424a3"
}
```

### User Creation

A user can be created by sending a *POST* request to `/user`, with a JSON attached contained the required information. A sample has been provided below. Information on password requirements can be seen [here](/ilo/Swagger#user-creation)

```json
{
  "username": "cookielover57🍪",
  "password": "MySuperSecurePassword57!",
  "public_key": "XzKSzgiX2qoPySbe5T4TSK2018V...",
  "api_key": "824a47ae-d0b9-5350-bffb-cc2ee48424a3"
}
```

### Log a user in

To log a user in, we send a PUT request to `/user`. The JSON we send along with this request will look as follows.

```json
{
  "username": "cookielover57🍪",
  "password": "MySuperSecurePassword57!",
  "api_key": "824a47ae-d0b9-5350-bffb-cc2ee48424a3"
}
```

## Reference Client

A reference client implemented in Python's Tkinter GUI toolkit has been created to provide a sample implementation of a client. This can be found within the Python folder, under `py_client` or the project path of `ilo/python/py_client`.

![](/img/py_client.png)

This client is aimed to showcase the use of the Ilo API. It provided the following functionality.

* Registering a user
* Connecting to a Potion room
* Changing rooms