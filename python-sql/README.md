# Be a SQL Python Hero with VS Code, GitHub Copilot & MSSQL-Python Driver

Make sure you have Python and VS Code on your machine, and then install the recommended extensions.

Install `UV` for managing Python packages and virtual environments:

https://docs.astral.sh/uv/

so that you can run the python samples via

```sh
uv run <filename>.py
```

before running any sample make sure the needed Python packages are installed via

```sh
uv sync
```

The demos are the following:

## sample-0

Basic connection to a SQL Server database using the `mssql-python` driver. Use the `sql-test.py` file.

## sample-1

List all the tables in a database

## sample-2

Export data from a SQL Server table to a Parquet file

## sample-3

A website to display table usage

## sample-4

Display index usage using [streamlit](https://streamlit.io/)