# Challenge Data Analytics - Python

### Initiate a Conda Enviroment

For this project, I've used the Anaconda distribution of Python. So follow this steps to create an enviroment:

1. To create an environment:

```
conda create -n yourenv pip
```

- Replace "yourenv" with the name of the new environment. The command pip should make you able to work with pip to install the packages needed with pip.

2. To activate an environment:

```
conda activate myenv
```

- This should activate the environment and load some packages.

3. To download all the packages, run:

```
pip install -r requirements.txt
```

#### Take in count:

The urls of the databases could be changed in the `app/links.py` if necessary.

- To connect with PostgreSQL, you need to add your PostgreSQL data in `.env`

4. Once you have the package we can execute the code with:

```
python app/main.py
```
