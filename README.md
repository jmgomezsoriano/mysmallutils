# MySmallUtils
Small Python utils to do life easier.

This includes tools to execute external commands, compress files,
manage configuration files, open different types of files (JSON, YAML and Pickle) compressed or not,
configure logging, obtain metrics, download files, etc.

This module is divided into the following categories:

* [Collections](#collections)
  * [Head of a set or dict](#head-of-a-set-or-dict)
  * [List union](#list-union)
* [Text](#text)
  * [Remove urls](#remove-urls)
  * [Clean text](#clean-text)
* [File access, load and save files](#file-access-load-and-save-files)
  * [Open files](#open-files)
  * [Read the first line of a file](#read-the-first-line-of-a-file)
  * [Load and save json files](#load-and-save-json-files)
  * [Load and save pickle files](#load-and-save-pickle-files)
  * [Load and save Yaml files](#load-and-save-yaml-files)
  * [Copy files](#copy-files)
  * [Remove files](#remove-files)
  * [Check if exists several files](#check-if-exists-several-files)
  * [Count lines](#count-lines)
  * [Touch](#touch)
* [Compressing files](#compressing-files)
  * [Gzip](#gzip)
  * [Tar](#tar)
* [External commands](#external-commands)
* [Configuration files](#configuration-files)
* [Logging](#logging)
* [Method synchronization](#method-synchronization)
* Obtaining metrics
* [Services and Web](#services-and-web)
  * [Download a file](#download-a-file)
  * [Flask services](#flask-services)
  
## Collections<a id="collections"></a>
Some util functions for list, set or dict collections.

### Head of a set or dict<a id="head-of-a-set-or-dict"></a>
Get the first n elements of a dictionary or a set.

```python
from mysutils.collections import head

# A set of latin characters
set1 = {chr(97 + i) for i in range(26)}
# Select the first 5 elements of the set
head(set1, 5)  # returns {'d', 'a', 'b', 'e', 'c'}
# By default select 10 elements
head(set1)  # returns {'f', 'd', 'j', 'a', 'b', 'e', 'h', 'i', 'c', 'g'}

# A dictionary of latin characters
dict1 = {i: chr(97 + i) for i in range(26)}
# Select the first 5 items of the dictionary
head(dict1, 5)  # Returns {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e'}
# By default select 10 items
head(dict1)  # Returns {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j'}
```

Also, you can use the specific functions for set and dictionaries: **sh()** for set head and **dh()** for dictionaries.

```python
from mysutils.collections import sh

# A set of latin characters
set1 = {chr(97 + i) for i in range(26)}
# Select the first 5 elements of the set
sh(set1, 5)
# By default select 10 elements
sh(set1)
```

```python
from mysutils.collections import dh

# A dictionary of latin characters
dict1 = {i: chr(97 + i) for i in range(26)}
# Select the first 5 items of the dictionary
dh(dict1, 5)
# By default select 10 items
dh(dict1)
```

### List union<a id="list-union"></a>
Create the union of two or more lists maintaining the order of elements.

```python
from mysutils.collections import list_union

l1 = [1, 2, 3]
l2 = [4, 5, 6, 1]
l3 = [2, 6, 24]
# This will return  [1, 2, 3, 4, 5, 6, 24]
list_union(l1, l2, l3)
# This will return [1, 2, 3, 6, 24, 4, 5]
list_union(l1, l3, l2)
```

## Text<a id="text"></a>
Simple functions related to text.

### Remove urls<a id="remove-urls"></a>
Remove urls from a text.

```python
from mysutils.text import remove_urls

text = 'This is a test!\n     Clean punctuation symbols and urls like this: '
       'https://example.com/my_space/user?a=b&c=3#first '
       'https://example.com/my_space/user#first'
remove_urls(text)
# Result: 
# 'This is a test!\n     Clean punctuation symbols and urls like this:  '
```

### Clean text<a id="clean-text"></a>
Remove punctuation symbols, urls and convert to lower.

```python
from mysutils.text import clean_text

text = 'This is a test!\n     Clean punctuation symbols and urls like this: ' \
       'https://example.com/my_space/user?a=b&c=3#first ' \
       'https://example.com/my_space/user#first'

# Remove punctuation, urls and convert to lower
clean_text(text)

# Remove punctuation and urls but do not convert to lower
clean_text(text, lower=False)

# Only remove punctuation
clean_text(text, lower=False, url=False)
```

## File access, load and save files<a id="file-access-load-and-save-files"></a>
With these functions you can open files, create json and pickle files, and execute external commands very easily.
Moreover, only changing the file extension you can store the information in a compressed file with gzip.

### Open files<a id="open-files"></a>
```python
from mysutils.file import open_file, force_open

# Open a text file to read
with open_file('file.txt') as file:
    pass

# Open a compressed text file to write
with open_file('file.txt.gz', 'w') as file:
    pass

# Open a file in a directory, if the directory does not exist, 
# then create the parent directories.
with force_open('file.txt') as file:
    pass

# The same as previously, but with a compressed file.
with force_open('file.txt.gz', 'w') as file:
    pass
```

### Read the first line of a file<a id="read-the-first-line-of-a-file"></a>
This function only reads the first line of a text file (gzip compressed or not) and returns it without the \n if 
it exists.

```python
from mysutils.file import first_line

# Read the first line of the file token.txt ignoring the character \n at the end of the line.
token = first_line('token.txt')
```

### Load and save json files<a id="load-and-save-json-files"></a>
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

# Save the json into a text file in a given directory, 
# if the directory does not exist, then create it
save_json(d, 'data/file.json', force=True)

# The same but wit a compressed file
save_json(d, 'data/file.json.gz', force=True)

# Load from a tar file
from mysutils.tar import load_tar_json

# Load a json (data.json) from a compressed tar file (file.tar.bz2)
d = load_tar_json('data/file.tar.bz2', 'data.json')
```

### Load and save pickle files<a id="load-and-save-pickle-files"></a>
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

# Save the object into a pickle file in a given directory, 
# if the directory does not exist, then create it
save_pickle(d, 'data/test1.pkl', force=True)

# The same but wit a compressed pickle file
save_pickle(d, 'data/test1.pkl.gz', force=True)

# Load from a tar file
from mysutils.tar import load_tar_pickle

# Load a compressed pickle (data.pkl.gz) from a compressed tar file (file.tar.bz2)
d = load_tar_pickle('data/file.tar.bz2', 'data.pkl.gz')
```

### Load and save Yaml files<a id="load-and-save-yaml-files"></a>
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

# Save the object into a yaml file in a given directory, 
# if the directory does not exist, then create it
save_yaml(d, 'data/file.yml', force=True)

# The same but wit a compressed yaml file
save_yaml(d, 'data/file.yml.gz', force=True)

# Load from a tar file
from mysutils.yaml import load_tar_yaml

# Load a yaml (data.yaml) from a compressed tar file (file.tar.xz)
d = load_tar_yaml('data/file.tar.xz', 'data.yaml')
```

### Copy files<a id="copy-files"></a>

A very simple way to copy several files into a directory. For example:

```python
from mysutils.file import copy_files

# Copy the files 'file1.txt' and 'file2.txt' to the folder 'data/'. 
# If the directory does not exist, then create it.
copy_files('data/', 'file1.txt', 'file2.txt')

# To avoid create the folder if it does not exist.
copy_files('data/', 'file1.txt', 'file2.txt', force=False)
```

### Remove files<a id="remove-files"></a>

You can also remove several files and empty folders with just one sentence, using the remove_files() function:

```python
from mysutils.file import remove_files

remove_files('test2.json', 'data/test1.json', 'data/')
```

If the file to remove is a directory, it has to be empty. If you want to remove directories with subdirectories or 
files, use shutil.rmtree().

### Check if exists several files<a id="check-if-exists-several-files"></a>
With the function exist_files() you can check if several files exist or not.
Its usage is very simple, for example:

```python
from mysutils.file import exist_files

# Returns True if all the files exist, otherwise False.
exist_files('mysutils/collections.py', 'test/filetests.py', 'mysutils/file.py')
```

### Count lines<a id="count-lines"></a> 
Count the number of lines of a file. If the file is gzip compressed, then decompress it first.

```python
from mysutils.file import open_file, count_lines
# Create a file with two lines
with open_file('text.txt.gz', 'wt') as file:
    print('First line', file=file)
    print('Second line', file=file)
# Return 2
count_lines('text.txt.gz')
```

### Touch<a id="touch"></a>
Create an empty file.

```python
from mysutils.file import touch

# Create the text.txt file without content
touch('text.txt')
```

## Compressing files<a id="compressing-files"></a>
With this library there are two ways to compress files: single gzip files and tar files.

### Gzip<a id="gzip"></a>

```python
from mysutils.file import gzip_compress, gzip_decompress, save_json

# Create a file
d = {
    'version': 1.0,
    'file_list': ['1.txt', '2.txt']
}
save_json(d, 'file.json')

# Compress the file
gzip_compress('file.json', 'file.json.gz')
# Decompress the file
gzip_decompress('file.json.gz', 'file2.json')
```

### Tar<a id="tar"></a>
Some utils to create, extract and use tar files.

All the examples of this section assume you have the files 'test.json' and 'test.json.gz', for instance, with
this code:

```python
from mysutils.file import save_json

d = {
    'version': 1.0,
    'file_list': ['1.txt', '2.txt']
}
save_json(d, 'test.json')
save_json(d, 'test.json.gz')
```

#### Create a tar file<a id="create-a-tar-file"></a>
With create_tar() you can create a tar file (compressed or not) and include a list of files.

```python
from mysutils.tar import create_tar

# Create a normal tar file
create_tar('test.tar', 'test.json', 'test.json.gz')

# Create a gzip compressed tar file
create_tar('test.tar.gz', 'test.json', 'test.json.gz')

# Create a bzip2 compressed tar file
create_tar('test.tar.bz2', 'test.json', 'test.json.gz')

# create a xz compressed tar file
create_tar('test.tar.xz', 'test.json', 'test.json.gz')
```

#### List the content of a tar file<a id="list-the-content-of-a-tar-file"></a>

```python
from mysutils.tar import list_tar

lst = list_tar('test.tar.gz')
print(lst[0].path)
```

#### Extract a specific file<a id="extract-a-specific-file"></a>
```python
from mysutils.tar import extract_tar_file

# Extract the file 'test.json' to 'test2.json' from 'test.tar.gz'. 
extract_tar_file('test.tar.gz', 'test2.json', 'test.json')

# Extract the file 'test.json' and save it into 'data/' folder from 'test.tar.gz'.
extract_tar_file('test.tar.gz', 'data/', 'test.json')
```

#### Extract several files into a folder<a id="extract-several-files-into-a-folder"></a>
```python
from mysutils.tar import extract_tar_files, extract_tar

# Extract 'test.json' and 'test.json.gz' from 'test.tar.gz2' and store them into 'data/' if it exists.
extract_tar_files('test.tar.bz2', 'data/', 'test.json', 'test.json.gz')

# The same as before but creates the folder 'data/' if it does not exist.
extract_tar_files('test.tar.bz2', 'data/', 'test.json', 'test.json.gz', force=True)

# Extract files showing a progress bar
extract_tar_files('test.tar.bz2', 'data/', 'test.json', 'test.json.gz', verbose=True)

# Extract all the files into the folder 'data/' if it exists
extract_tar('test.tar', 'data/', False)

# Extract all the files forcing the folder creation
extract_tar('test.tar', 'data/', True)

# Show a progress bar
extract_tar('test.tar', 'data/', verbose=True)
```

## External commands<a id="external-commands"></a>
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

## Configuration files<a id="configuration-files"></a>

Too many times, when you deal with config files or some kind of configuration cluster server, you become crazy
because there are a small spelling mistake in the name of a configuration parameter, and you code does not work 
properly.
With the function parse_config() you can easily define an array with the configuration parameter that you need and
this function throws an exception if there are any error or the parameters in the configuration file does not match
with the defined ones. For example:

```python
from mysutils.config import parse_config

PARAM_DEFINITION = [('server_host', False, 'http://0.0.0.0'), ('server_port', False, 8080),
                    ('database_name', True, None)]
# Check if all the required parameters are in the configuration file and there are anymore (double check)
config = {
  'database_name': 'Test'
}
values = parse_config(config, PARAM_DEFINITION, True)  # Returns the default values of the parameters

# With double_check to False instead of True, the configuration file can have other no defined parameters
config = {
  'database_name': 'Test',
  'new_parameter': 1
}
values = parse_config(config, PARAM_DEFINITION, False)

# This will raise an error because double_check is activated and the configuration file has a non-defined value.
config = {
  'database_name': 'Test',
  'new_parameter': 1
}
parse_config(config, PARAM_DEFINITION, True)
```

## Logging<a id="logging"></a>
Some functions to configure and to get information about logging. 

```python
from mysutils.logging import get_log_level_names, get_log_levels, get_log_level, config_log

# Configure the logging to show only error messages
config_log('ERROR')

# Configure the logging to show INFO or higher message level and store it in a file
config_log('ERROR', 'file.log')

# Get the log level names
get_log_level_names()

# Get the log level names and its number
get_log_levels()

# Get the log level number from its name
get_log_level('DEBUG')
```

## Method synchronization<a id="method-synchronization"></a>
Sometimes it is necessary to create a synchronized method.
With @synchronized you can create a synchronized method easily:

```python
from mysutils.method import synchronized
from time import sleep
from threading import Thread

num = 0

# Create a class with a synchronized method
class MyClass(object):
    @synchronized
    def calculate(self):
        global num
        print(f'Starting calculation {num}.')
        sleep(5)
        num += 1
        print(f'Ending calculation {num}.')

# Create two instances of the same class
obj1, obj2 = MyClass(), MyClass()
# Execute the method of the first object as a thread 
thread = Thread(target=obj1.calculate)
thread.start()
sleep(1)
# This method will wait 4 seconds more to finish the first calculate() method.
obj1.calculate()
```

## Obtaining metrics<a id="obtaining-metrics"></a>

## Services and Web<a id="services-and-web"></a>

### Download a file<a id="download-a-file"></a>
This function requires to install the Requests module with the following command:

```bash
pip install requests~=2.25.1
```

After module requests is installed, you can download a file with this simple command:

```python
from mysutils.web import download

# Download the file from the url to 'dest/file.txt'.
download('<url-to-download>', 'dest/file.txt')
```

### Flask services<a id="flask-services"></a>
In the contexts of a Flask service, you can need the base url to a service, that means, 
the protocol, IP or hostname and path to the service. 
You can obtain this with endpoint() function. 
However, you first need to install the Flask module:

```bash
pip install Flask~=2.0.1
```

An example of how to use:

```python
from flask import Flask, request
from mysutils.flaskservice import endpoint

app = Flask(__name__)


@app.route('/api/fantastic')
def my_service():
  url = endpoint(request, '/api/fantastic')
  print(f'Executing service at {url}...')
```
