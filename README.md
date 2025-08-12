## About

Code to run on the remote server (PC). Designed to work with the [robot code](https://github.com/tplaysted/integrated-robot).

## Usage
After cloning the repository to your PC, create a [virtual environment](https://docs.python.org/3/library/venv.html) in the installation folder. After activating the environment, get dependencies with `pip install -r requirements.txt`.

### Command listener
Run `python key_sub.py` to start the command listener. You may use `-i` to specify the interface and `-p` for the port, but it's not recommended to change the defaults.
