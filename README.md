# Blogly

A blogging website exercise for practice

---

## Setup Steps

1. Clone the repo

    ```sh
    git clone https://github.com/MrCookiefries/Blogly.git
    ```

1. Make a virtual enviroment in Python at root of repo & install packages

    ```sh
    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt
    ```

1. Seed the database with starter data

    ```sh
    python seed.py
    ```

1. Start the Flask server & open the page

    ```sh
    flask run
    ```

---

## Tools Used

- HTML
    - Jinja
- CSS
- Python
- Flask
    - FSQLA

### Testing

There are tests for the two python files `app.py` & `models.py`
In order to test them, run the test files
```sh
python -m unittest test_app.py
python -m unittest test_models.py
```
