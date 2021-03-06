Bakery Promotion Effectiveness Dashboard
==============================

Getting Started
------------

Clone project from git repository
`git clone `

Setup virtual environment using the provided requirements.txt file

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Run project using
`main.py`

Alternatively, to produce an interactive dashboard, run
`streamlit run app.py`
Note: after installing dependencies, deactivate and reactivate the virtual environment for streamlit to work.

Project Organization
------------

    ├── README.md               <- The top-level README for developers using this project.
    │
    ├── main.py                 <- The main app module
    │
    ├── app.py                  <- An associated streamlit app
    │
    ├── requirements.txt        <- The requirements file for reproducing the analysis environment.
    │
    ├── dbinfo.yaml             <- The database information (stored as a yaml file)
    │
    ├── output.log              <- Output log for main.py
    |
    ├── images                  <- Directory where images are stored.
    │
    └── src                     <- Source files for use in this project
        │
        ├── read_dbinfo_yaml.py <- Read database information from yaml file
        │
        ├── DBInteractor.py     <- Database interaction class (connects to database, runs sql queries)
        │
        └── visualizations.py   <- Visualizations module

------------
