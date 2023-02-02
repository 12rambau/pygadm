## 0.2.0 (2023-02-02)

### Feat

- add the support for continents
- use lists in the requests

### Fix

- udate database generation script
- add last continents
- ignore ruff cache
- add north america
- add europe and asia
- increase coverage
- build documentation in the appropriate folder Fix #1

### Refactor

- styling
- edit database to avoid duplication now the database is a stair with first all the countries then all admin 1 etc. This ensure that when there is a duplication (e.g. Italy) it catches the country first
- reduce size of continent list

## 0.1.1 (2023-01-10)

### Refactor

- use ruff replace isort and flake8
- remove .DS_Store legacy mac file
- use brotli compression for database

## 0.1.0 (2023-01-08)

### Feat

- aline the get_name behavior on get_items
- automatic publishing
- output a pandas dataframe
- first version of the methods

### Fix

- search case insensitive
- use json instead of geopackage format
- remove execution of gee cells
- make it work with gee
- remove colorama dependency
- unit.yml typo
- remove jupyter_execute related to #1
- remove vscode
- add parquet file to distrib
- use parquet pickle files have an incompatibility issue between pandas 1.2 - 1.3
- use protocol 4 for the pickle compatibility issue with Python 3.7
- don't assess dead-fixture because I don't use fixtures

### Refactor

- remove useless variable in the docs
- use get_name in get_items
- typo
- only use shield.io badges
- typo
