# What The *Github* Did I Do?
Did you ever work on a project and felt like...
- Man, what did I do?
- Did I forget to close some issues?
- What did I do during my drunken black-out on github?

For all those questions, we can utilize the GitHub API to solve those issues.

---

# Disclaimer
##### This is just an personal development project for creating applications in Python
*Please only use this as a template for your projects, do not attempt to simply use this project without modifications.*

---

### INSTALL instructions:

##### You need to create a ```config.py``` and fill in the TOKEN directly on GitHub! 
See the official how-to here at GitHub: 
- https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/

Put that new personal token into ```config.py``` (see ```config.py.example```):
```python
TOKEN="put-your-token-in-here"
```

Ensure you install the required packages either in a virtual python install...
```bash
virtualenv venv
source venv/bin/activate
```
or directly on your system by using the provided pip package list:
```bash
pip install -r requirements.txt
```

***Note:*** This was created by utilizing `pip freeze`:
```bash
pip freeze > requirements.txt
```

Upon finish you can now start the application.
```bash
python3 main.py
```
