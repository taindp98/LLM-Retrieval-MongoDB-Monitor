<h1>
  <img alt="lograg_bg" src="./docs/images/lograg_bg.png" style="width: 100%;">
  <p align="center">
	Empower RAG Request with MongoDB Monitoring
  </p>
</h1>

<p align="center">
    <img alt="OpenAI" src="https://img.shields.io/badge/OpenAI-000000?logo=openai&logoColor=white&style=flat" />
<img alt="MongoDB" src="https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white&style=flat" />
<a href="./notebooks/request_example.ipynb">
        <img alt="Jupyter Notebook" src="https://img.shields.io/badge/Jupyter_Notebook-F37626?logo=jupyter&logoColor=white&style=flat" />
    </a>
</p>

## Table of Contents

- [Update](#update)
- [Quickstart](#quickstart)
- [Contributing](#contributing)

## Update
- [08/2024]: We released the first version of the codebase

## Quickstart

To re-product the project, please refer to the repository

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for simple_rag
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── simple_rag                <- Source code for use in this project.
    │
    ├── __init__.py    <- Makes simple_rag a Python module
```

The structure of source code:


Let’s install the library

```bash
pip install -r requirements.txt
```

Create the `.env` file containing `OPENAI_API_KEY` the connection to the `MongoDB` Atlas

```
## OPENAI
OPENAI_API_KEY=sk-***

## MONGODB
COLLECTION_NAME=<your-collection-name>
DB_NAME=<your-database-name>
CLUSTER_ADDRESS=<your-cluster-ip-address>
USRNAME=<provided-user-name>
PASSWD=<provided-password>
```

## Contributing

All contributions are welcome.




