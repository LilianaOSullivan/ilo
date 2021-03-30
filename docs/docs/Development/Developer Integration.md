# Developer Integration

Ilo requires Python and Elixir to function, with both FastAPI and Potion running concurrency to function correctly.

Python can be downloaded from the official <a href="https://www.python.org/downloads/">Python.org download</a> website.
Once downloaded and installed, the required Python libraries can be installed from PyPi using pip requirements

<div id="termynal" data-termynal>
    <span data-ty="input" data-ty-prompt="ilo/python $">pip install -r requirements.txt</span>
</div>

<br>

Within the Python folder there is a bash to run FastAPI with `localhost` certificates
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
