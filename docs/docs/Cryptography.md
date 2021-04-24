# Cryptography

As originally intended, Ilo enables the sending of plaintext and Cryptographic messages. Assuming a valid user exists, is sending the request, Potion will forward the message without verifying keys.

Potion will only enable requests from users that are logged in. A user can log in by sending a put request to `/user` to FastAPI. More information can be found at [Swagger](/ilo/Swagger). Due to the general-purpose design used within development, Ilo can support any Cryptographic algorithm. The expectation for clients is to use RSA with OAEP ([Optimal Asymmetric Encryption Padding](https://en.wikipedia.org/wiki/Optimal_asymmetric_encryption_padding)).

