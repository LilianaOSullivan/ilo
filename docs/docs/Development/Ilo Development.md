# Ilo Development

Ilo requires Python and Elixir to function, with both FastAPI and Potion running concurrency to function correctly.

Python can be downloaded from the official <a href="https://www.python.org/downloads/">Python.org download</a> website.
Once downloaded and installed, the required Python libraries can be installed from PyPi using pip requirements

<div id="termynal" data-termynal>
    <span data-ty="input" data-ty-prompt="ilo/python $">pip install -r requirements.txt</span>
</div>

<br>

Within the Python folder there is a bash to run FastAPI with `localhost` certificates. A localhost SSL certificate needs to be created within the python directory. To do this enter the following command at the terminal. Additional information on localhost certificate generation can be found <a href="https://letsencrypt.org/docs/certificates-for-localhost/#making-and-trusting-your-own-certificates">here</a>

```bash
openssl req -x509 -out localhost.crt -keyout localhost.key \
  -newkey rsa:2048 -nodes -sha256 \
  -subj '/CN=localhost' -extensions EXT -config <( \
   printf "[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")
```

The FastAPI server will additionally need a MongoDB backend to function. Specifically it requires the creation of the following

* Database
* User collection
* Api key collection

The names of the database and collections can be set within the `general_config.yaml` file within the python folder. Along with providing it the IP Address of the database.


<div id="termynal" data-termynal>
    <span data-ty="input" data-ty-prompt="ilo/python $">bash run.sh</span>
</div>

<br>

Potion dependencies can be installed using `mix deps.get` from the potion folder
<div id="termynal" data-termynal>
    <span data-ty="input" data-ty-prompt="ilo/elixir $">mix deps.get</span>
</div>

<br>

Potion can be launched in interactive mode with `iex`
<div id="termynal" data-termynal>
    <span data-ty="input" data-ty-prompt="ilo/elixir $">iex -S mix</span>
</div>

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
