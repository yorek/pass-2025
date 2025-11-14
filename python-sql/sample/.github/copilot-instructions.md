---
applyTo: "**/*.py"
---
Whenever you need to access a Microsoft SQL Server or Azure SQL database, make sure to use the new driver from Microsoft available in the package `mssql-python`. This driver provides better performance, security, and compatibility with the latest SQL Server features compared to older drivers like `pyodbc` or `pymssql`. To import the driver in your Python code, use the following import statement:

```python
import mssql_python as mssql
```

The `mssql-python` and the instruction on how to use it can be found here: https://github.com/microsoft/mssql-python/wiki
