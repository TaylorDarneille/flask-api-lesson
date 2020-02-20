remember you have to manually write the requirements.txt file (this is like package.json)

pip3 wont do it for you

you do this after you install a module by running

```bash
$pip3 freeze > requirements.txt
```

later when you clone a flask app from somewhere else, to get all the modules listed in the requirements.txt file, run

```bash
$pip3 install -r requirements.txt
```
