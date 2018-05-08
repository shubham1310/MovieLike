## Initial Setup

When setting up the project initially, run

```bash
pip install --upgrade pip
virtualenv meta-pyenv
source meta-pyenv/bin/activate
pip install -r requirements.txt
```
Run this to install punkt
```bash
source meta-pyenv/bin/activate
python
```
and then inside python do this:
```bash
import nltk
nltk.download('punkt')
```

Make sure you run the `source` command before working with this project.
Alternatively, you can add it to your `~/.bashrc`.

To leave the virtual environment, simply close your terminal or type
`deactivate`.

## Running the servers

To run the search engine server,

```bash
python search_server.py config.toml
```


