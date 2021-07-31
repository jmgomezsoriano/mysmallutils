# MySmallUtils
Small Python utils to do life easier.

This includes tools to execute external commands, compress files,
manage configuration files, open different types of files (JSON, YAML and Pickle) compressed or not,
configure logging, obtain metrics, download files, etc.

This module is divided into the following categories:

* [External commands](#external-commands)
* Compressing files
* Configuration files
* [File access, load and save files](#file-access-load-and-save-files)
  * [Open files](#open-files)
  * [Load and save json files](#load-and-save-json-files)
  * [Load and save pickle files](#load-and-save-pickle-files)
  * [Load and save Yaml files](#load-and-save-yaml-files)
  * [Copy files](#copy-files)
* Logging
* Process synchronization
* Obtaining metrics
* Services and Web

## External commands

This module only contains a function that execute an external command and return the standard and error outputs.
Its execution is very simple:

```python
from mysutils.command import execute_command
# Execute the Unix shell command 'ls data/'
std, err = execute_command(['ls', 'data/'])
# Print the standard output
print(std)
# Print the error output
print(err)
```

## Compressing files

## Configuration files

## File access, load and save files

With these functions you can open files, create json and pickle files, and execute external commands very easily.
Moreover, only changing the file extension you can store the information in a compressed file with gzip.

### Open files
```python
from mysutils.file import open_file, force_open
# Open a text file to read
with open_file('file.txt') as file:
    pass
# Open a compressed text file to write
with open_file('file.txt.gz', 'w') as file:
    pass
# Open a file in a directory, if the directory does not exist, then create the parent directories.
with force_open('file.txt') as file:
    pass
# The same as previously, but with a compressed file.
with force_open('file.txt.gz', 'w') as file:
    pass
```

### Load and save json files
```python
from mysutils.file import load_json, save_json
d = {
    'version': 1.0,
    'file_list': ['1.txt', '2.txt']
}
# Save the json in a text file
save_json(d, 'file.json')
# Load the json file from a text file
d = load_json('file.json')
# Save the json in a compressed file
save_json(d, 'file.json.gz')
# Load the json file from a compressed file
d = load_json('file.json.gz')
# Save the json into a text file in a given directory, if the directory does not exist, then create it
save_json(d, 'data/file.json', force=True)
# The same but wit a compressed file
save_json(d, 'data/file.json.gz', force=True)
```

### Load and save pickle files
```python
from mysutils.file import load_pickle, save_pickle
d = {
    'version': 1.0,
    'file_list': ['1.txt', '2.txt']
}
# Save a object in a pickle file
save_pickle(d, 'test1.pkl')
# Load the object from a pickle file
d = load_pickle('test1.pkl')
# Save the object into a compressed pickle file
save_pickle(d, 'test1.pkl.gz')
# Load the object from a compressed pickle file
d = load_pickle('test1.pkl.gz')
# Save the object into a pickle file in a given directory, if the directory does not exist, then create it
save_pickle(d, 'data/test1.pkl', force=True)
# The same but wit a compressed pickle file
save_pickle(d, 'data/test1.pkl.gz', force=True)
```

### Load and save Yaml files

These functions require to install the PyYaml module with the following command:
```bash
pip install PyYAML~=5.4.1
```
Examples of usage:
```python
from mysutils.yaml import load_yaml, save_yaml
d = {
    'version': 1.0,
    'file_list': ['1.txt', '2.txt']
}
# Save a object in a yaml file
save_yaml(d, 'file.yml')
# Load the object from a yaml file
d = load_yaml('file.yml')
# Save the object into a compressed yaml file
save_yaml(d, 'file.yml.gz')
# Load the object from a compressed yaml file
d = load_yaml('file.yml.gz')
# Save the object into a yaml file in a given directory, if the directory does not exist, then create it
save_yaml(d, 'data/file.yml', force=True)
# The same but wit a compressed yaml file
save_yaml(d, 'data/file.yml.gz', force=True)
```
### Copy files

A very simple way to copy several files into a directory. For example:

```python
from mysutils.file import copy_files
# Copy the files 'file1.txt' and 'file2.txt' to the folder 'data/'. If the directory does not exist, then create it.
copy_files('data/', 'file1.txt', 'file2.txt')
# To avoid create the folder if it does not exist.
copy_files('data/', 'file1.txt', 'file2.txt', force=False)
```


## Logging

## Process synchronization

## Obtaining metrics

## Services and Web
