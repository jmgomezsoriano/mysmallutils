# MySmallUtils
Small Python utils to do life easier.

This includes tools to execute external commands, compress files,
manage configuration files, open different types of files (JSON, YAML and Pickle) compressed or not,
configure logging, obtain metrics, download files, etc.

This module is divided into the following categories:

* [Install](#install)
* [Collections](#collections)
  * [Head of a set or dict](#head-of-a-set-or-dict)
  * [List union](#list-union)
  * [Concat lists](#concat-lists)
  * [Dictionary operations](#dictionary-operations)
  * [Filter lists](#filter-lists)
  * [Tuples](#tuples)
* [Text](#text)
  * [Remove urls](#remove-urls)
  * [Replace urls](#replace-urls)
  * [Clean text](#clean-text)
  * [Text markup](#text-markup)
* [File access, load and save files](#file-access-load-and-save-files)
  * [Open files](#open-files)
  * [Read file](#read-file)
  * [Load and save json files](#load-and-save-json-files)
  * [Load and save pickle files](#load-and-save-pickle-files)
  * [Load and save Yaml files](#load-and-save-yaml-files)
  * [Copy files](#copy-files)
  * [Remove files](#remove-files)
  * [Check if exists several files](#check-if-exists-several-files)
  * [Count lines](#count-lines)
  * [Touch](#touch)
  * [Cat](#cat)
  * [Make directories](#make-directories)
  * [Move files](#move-files)
  * [List files](#list-files)
  * [Generate output file paths](#generate-output-file-paths)
  * [Check file encoding](#check-file-encoding)
* [Removable files](#remove-files)
* [Compressing files](#compressing-files)
  * [Gzip](#gzip)
  * [Tar](#tar)
* [External commands](#external-commands)
* [Configuration files](#configuration-files)
* [Logging](#logging)
* [Method synchronization](#method-synchronization)
* [Services and Web](#services-and-web)
  * [Download a file](#download-a-file)
  * [Endpoint](#endpoint)
  * [Generate service help](#generate-service-help)
  * [JSON post](#json-post)
* [Git monitor](#git-monitor)
* [File unit tests](#unit-tests)
* [Miscellany](#miscellany)

# Install

It is very easy to install:

```bash
# With pip
pip install mysmallutils

# With conda
conda install mysmallutils
```
  
# Collections<a id="collections"></a>
Some util functions for list, set or dict collections.

## Head of a set or dict<a id="head-of-a-set-or-dict"></a>
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

## List union<a id="list-union" name="list-union"></a>
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

## Concat lists<a id="concat-lists" name="concat-lists"></a>
Concatenate a list of lists and return other list with the results.
This is different from the list_union() function because the final list can contain repeated elements.

```python
from mysutils.collections import concat_lists

l1 = [1, 2, 3]
l2 = [4, 5, 6, 1]
l3 = [2, 6, 24]
# This will return  [1, 2, 3, 4, 5, 6, 1, 2, 6, 24]
concat_lists(l1, l2, l3)
# This will return  [4, 5, 6, 1, 2, 6, 24, 1, 2, 3]
concat_lists(l2, l3, l1)
```

## Dictionary operations<a id="dictionary-operations" name="dictionary-operations"></a>

With these functions you can do several operation over dictionaries in just one code line. 
For example, if you want to add a dictionary item, remove other, and modify the keys and values of the dictionary,
you can do the following:

```python
from mysutils.collections import add_keys, del_keys, mod_key, mod_value

d = {'name': 'Pablo', 'lastname': 'Escobar', 'email': 'pabloescobar@example.com'}
# Add the key 'country', remove 'email', change 'name' by 'firstname' and change the 'lastname' value:
mod_value(mod_key(del_keys(add_keys(d, country='Colombia'), 'email'), 'name', 'firstname'), 'lastname', 'Smith')
```

More information about these and other functions in the following subsections.

### Add keys
You can add several dictionary items in just one sentence and return the results.

```python
from mysutils.collections import add_keys

d = {'b': 2}
# Print {'a': 1, 'b': 2, 'c': 3}
print(add_keys(d, a=1, c=3))
# You can modify an existing item
print(add_keys(d, a=1, b=4, c=3))
# Or you can raise an error if the key already exists.
print(add_keys(d, modify=False, a=1, b=4, c=3))
```

### Delete keys

You can remove one or more dictionary items by their keys and return the result with only one line.

```python
from mysutils.collections import del_keys

d = {'a': 1, 'b': 2, 'c': 3}

# Remove the element c from the dictionary and print the results
print(del_keys(d.copy(), 'c'))
# Remove the elements a and c from the dictionary and print the results
print(del_keys(d.copy(), 'a', 'c'))
# If an element does not exist, ignore the key error
print(del_keys(d.copy(), 'a', 'd'))
# If an element does not exist, raise the KeyError exception
print(del_keys(d.copy(), 'a', 'd', ignore_errors=False))
```

### Modify keys

With just one sentence you can modify one or more keys without changing their values.

```python
from mysutils.collections import mod_key, mod_keys 

# Modify just one key: name by firstname
d = {'name': 'Pablo', 'lastname': 'Escobar', 'email': 'pabloescobar@example.com'}
mod_key(d, 'name', 'firstname')
# Modify several keys: name by firstname and lastname by familyname
d = {'name': 'Pablo', 'lastname': 'Escobar', 'email': 'pabloescobar@example.com'}
mod_keys(d, name='firstname', lastname='familyname')
```

### Modify values

With just one sentence you can modify one or more values.

```python
from mysutils.collections import mod_value, mod_values 

# Modify two values concatenating commands
d = {'name': 'Pablo', 'lastname': 'Escobar', 'email': 'pabloescobar@example.com'}
mod_value(mod_value(d, 'name', 'Jhon'), 'lastname', 'Smith')
# Modify two values with just one sentence
d = {'name': 'Pablo', 'lastname': 'Escobar', 'email': 'pabloescobar@example.com'}
mod_values(d, name='Jhon', lastname='Smith')
```

### Merge a list of dictionaries<a id="merge-a-list-of-directories" name="merge-a-list-of-dictionaries"></a>

Convert a list of dictionaries with the same keys in a dictionary which each key contain the list of values of each 
dictionary. For example:

```python
from mysutils.collections import merge_dicts

lst = [{'a': 1, 'b': 10}, {'a': 2, 'b': 11}, {'a': 3, 'b': 12}]
d = merge_dicts(lst)  # The value of d is {'a': [1, 2, 3], 'b': [10, 11, 12]}
```

### Get dictionary items

Several function to get different items of a dictionary apart from its key.

```python
from mysutils.collections import first_item, last_item, first_key, last_key, first_value, last_value, item, key, value

d = {'a': 1, 'b': 2, 'c': 3}

# Get the first dictionary item
first_item(d)  # Returns ('a', 1)
# Get the last dictionary item
last_item(d)  # Returns ('c', 3)
# Get the first key of the dictionary
first_key(d)  # Returns 'a'
# Get the last key of the dictionary
last_key(d)  # Returns 'c'
# Get the first value of the dictionary
first_value(d)  # Returns 1
# Get the last value of the dictionary
last_value(d)  # Returns 3
# Get the item in the position 1 of the dictionary
item(d, 1)  # Returns ('b', 2)
# Get the key in the position 1 of the dictionary
key(d, 1)  # Returns 'b'
# Get the value in the position 1 of the dictionary
value(d, 1)  # Returns 2
```

### Search the first key in a list of dictionaries.

In an iterable of dicts (like a list) this function return the value of the first dictionary that contains the key.

```python
from mysutils.collections import first_key_value

lst = [{'a': 1, 'b': 2}, {'a': 10, 'c': 3}, {'a': 100, 'c': 30}]
first_key_value(lst, 'a')  # Returns 1
first_key_value(lst, 'b')  # Returns 2
first_key_value(lst, 'c')  # Returns 3
first_key_value(lst, 'd')  # Raises a KeyError exception
```

## Filter lists<a id="filter-lists" name="filter-lists"></a>
Filter a list by a condition.

```python
from mysutils.collections import filter_lst

lst = [i for i in range(1, 20)]

# Returns [1, 2, 3, 4]
filter_lst(lst, 4)
# Returns [2, 3, 4]
filter_lst(lst, 3, 1)
# Returns [3, 5]
filter_lst(lst, 5, 1, lambda x: x % 2 == 1)
```

## Tuples<a id="tuples" name="tuples"></a>

Convert a list of tuples into a tuple of lists. For example:

```python
from mysutils.collections import merge_tuples

lst = [(1, 10), (2, 11), (3, 12)]
t = merge_tuples(lst)  # The value of t is ([1, 2, 3], [10, 11, 12])
```

# Text<a id="text" name="text"></a>
Simple functions related to text.

## Remove URLs<a id="remove-urls" name="remove-urls"></a>
Remove URLs from a text.

```python
from mysutils.text import remove_urls

text = """This is a test!
Clean urls like this:
https://example.com/my_space/user?a=b&c=3#first
https://example.com/your_space/user#first"""
remove_urls(text)
# Result: 
# 'This is a test!\nClean urls like this:'

# You can filter by path:
remove_urls(text, r'my_space/user\?a=b&c=3#first')
# Result:
# 'This is a test!\n
#     Clean punctuation symbols and urls like this:  https://example.com/your_space/user#first')
```

# Replace URLs<a id='remove-urls" name="remove-urls"></a>

Replace all the URLs which have a given path.

```python
from mysutils.text import replace_urls

text = """This is a test!
Clean some urls like this:
https://example.com/my_space/user?a=b&c=3#first
https://example.com/your_space/user#first"""

# Replace only the url with the path /my_space/user
replace_urls(text, 'https://hello.com')
# Result:
# 'This is a test!\n
#      Clean punctuation symbols and urls like this: https://hello.com https://hello.com'

# Replace only the url with the path /my_space/user
replace_urls(text, 'https://hello.com', r'my_space/user')
# Result:
# 'This is a test!\n
#      Clean punctuation symbols and urls like this: https://hello.com https://example.com/your_space')
```

## Clean text<a id="clean-text" name="clean-text"></a>
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
## Text markup<a id='text-markup' name='text-markup'></a>

Create text effects in the console.

```python
from mysutils.text import AnsiCodes, markup

# Print a yellow, italic and blinked text.
print(markup('This is a text with effects', 
             AnsiCodes.YELLOW, AnsiCodes.ITALIC, 
             AnsiCodes.SLOW_BLINK))
# This is the same but using string names
print(markup('This is a text with effects', 
             'yellow', 'italic', 
             'SLOW_BLINK'))
```

You can see the list of effects in the mysutils.text.AnsiCode enumeration.

Furthermore, you can set your own font, background and underline colors based on R, G, B scale.

```python
from mysutils.text import AnsiCodes, markup, color, bg_color, un_color

# Print 'text' in yellow with gray background and blue underline color.
print('This is a ' + \ 
      markup('text', AnsiCodes.UNDERLINE, 
             color(255, 255, 20), 
             bg_color(60, 60, 60),
             un_color(80, 80, 255)) + 'with effects.')
```
**Important note:** All these font variants, styles and color do not work in all the consoles/terminals.

# File access, load and save files<a id="file-access-load-and-save-files" name="file-access-load-and-save-files"></a>
With these functions you can open files, create json and pickle files, and execute external commands very easily.
Moreover, only changing the file extension you can store the information in a compressed file with gzip.

## Open files<a id="open-files" name="open-files"></a>
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

## Load and save json files<a id="load-and-save-json-files" name="load-and-save-json-files"></a>
This save and load json files, even if they are compressed, with just one line.
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

# Load a json file and if it doesn't exists, 
# then it returns a default value
d = load_json('file.json', default={})

# Load from a tar file
from mysutils.tar import load_tar_json

# Load a json (data.json) from a compressed tar file (file.tar.bz2)
d = load_tar_json('data/file.tar.bz2', 'data.json')
```

You can also load a JSON file from a [compressed tar file](#open-and-load-files-inside-a-tar-archive).

## Load and save pickle files<a id="load-and-save-pickle-files" name="load-and-save-pickle-files"></a>
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

# Load the object but if the file does not exist, 
# then return the default vaule.
d = load_pickle('test1.pkl', default={})

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
You can also load a pickle file from a [compressed tar file](#open-and-load-files-inside-a-tar-archive).

## Load and save Yaml files<a id="load-and-save-yaml-files" name="load-and-save-yaml-files"></a>
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

# Load the object from the yaml file if it exists,
# otherwise it returns the default object
d = load_yaml('file.yml.gz', {})

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
You can also load a YAML file from a [compressed tar file](#open-and-load-files-inside-a-tar-archive).

## Copy files<a id="copy-files" name="copy-files"></a>

A very simple way to copy several files into a directory. For example:

```python
from mysutils.file import copy_files

# Copy the files 'file1.txt' and 'file2.txt' to the folder 'data/'. 
# If the directory does not exist, then create it.
copy_files('data/', 'file1.txt', 'file2.txt')

# To avoid create the folder if it does not exist.
copy_files('data/', 'file1.txt', 'file2.txt', force=False)
```

## Remove files<a id="remove-files" name="remove-files"></a>
You can also remove several files and empty folders with just one sentence, using the remove_files() function:

```python
from mysutils.file import remove_files

# Remove three files at once.
remove_files('test2.json', 'data/test1.json', 'data/')

# Remove three files at once ignoring if any does not exist.
remove_files('test2.json', 'data/test1.json', 'data/', ignore_errors=True)

# Remove three files or folders at once, if the folder contains more files, also will be removed.
remove_files('test2.json', 'data/test1.json', 'data/', recursive=True)
```

If the file to remove is a directory, it has to be empty. If you want to remove directories with subdirectories or 
files, use shutil.rmtree().

Also,you can use removable_files() to remove files after their use:

```python
from mysutils.tmp import removable_files

# These files will be removed when the with ends
with removable_files('test2.json', 'data/test1.json', 'data/'):
    pass

# These files will be removed when the with ends, ignoring possible errors
with removable_files('test2.json', 'data/test1.json', 'data/', ignore_errors=True):
    pass

# These files will be removed when the with ends, if any folder contains more files, also will be removed
with removable_files('test2.json', 'data/test1.json', 'data/', recursive=True):
    pass

# Get the variables for each removable file
with removable_files('test2.json') as (f1,):
    pass

# Even for several files
with removable_files('test2.json', 'data/test1.json', 'data/') as (f1, f2, f3):
    pass
```

## Check if exists several files<a id="check-if-exists-several-files" name="check-if-exists-several-files"></a>
With the function exist_files() you can check if several files exist or not.
Its usage is very simple, for example:

```python
from mysutils.file import exist_files, not_exist_files, are_dir, not_are_dir

# Returns True if all of the files exist, otherwise False.
exist_files('mysutils/collections.py', 'test/filetests.py', 'mysutils/file.py')

# Return True if any of the files exist, if it exists at least one, then return False
not_exist_files('mysutils/collections.py', 'test/filetests.py', 'mysutils/file.py')

# Returns True if all of the files are directories, otherwise False.
are_dir('mysutils/collections.py', 'test/filetests.py', 'mysutils/file.py')

# Return True if any of the files are directories, otherwise False.
not_are_dir('mysutils/collections.py', 'test/filetests.py', 'mysutils/file.py')
```

## Count lines<a id="count-lines" name="count-lines"></a> 
Count the number of lines of one or several files. If the file is gzip compressed, then decompress it first.

```python
from mysutils.file import open_file, count_lines
# Create a file with two lines
with open_file('text.txt.gz', 'wt') as file:
    print('First line', file=file)
    print('Second line', file=file)
# Return 2
count_lines('text.txt.gz')

# Count lines of several files
count_lines('file.txt.gz', 'file.txt')
```

## Touch<a id="touch" name="touch"></a>
Create several empty files.

```python
from mysutils.file import touch

# Create the text.txt file without content
touch('text.txt')

# Create several empty files
touch('1.txt', '2.txt', '3.txt')
```

## Cat<a id="cat" name="cat"></a>
Print the content of a file.

```python
from mysutils.file import cat, open_file

# Print the content of text.txt in the standard output
cat('text.txt')
# Print the content of the compressed file text.txt.gz in the standard output
cat('text.txt.gz')
# Print the content of text.txt into the file text_cat.txt
with open_file('text_cat.txt', 'wt') as file:
    cat('text.txt', output=file)
# Print the content of the compressed file text.txt.gz in the other compressed file text_cat.txt.gz.
with open_file('text_cat.txt.gz', 'wt') as file:
    cat('text.txt.gz', file)
```

## Read file<a id="read-file" name="read-file"></a>
Here is included functions to read a file of several forms.

```python
from mysutils.file import read_file, first_line, last_line, head, tail, body, \
  read_files, read_from, read_until

# Read the file 'text.txt'
lines = read_file('text.txt')
# Read the compressed file 'text.txt.gz'
lines = read_file('text.txt.gz')
# Read the compressed file 'text.txt.gz' removing the newline character if it exists
lines = read_file('text.txt.gz', False)

# Read the first line of the file token.txt ignoring the character \n at the end of the line.
token = first_line('token.txt')
# Read the last line of the file
line = last_line('credits.txt')
# Read the top 20 lines of the file
top_lines = head('README.md', 20)
# Read the last 20 lines of the file
last_lines = tail('README.md', 20)
# Read the lines between the 5 to 20
body_lines = body('README.md', 5, 20)
# Read lines from the line that starts with "# Text" appears to the end of file
read_from('README.md', r'^# Text')
# Read lines until the line that starts with "# Text" is found
read_until('README.md', r'^# Text')

# Read several files at once and return a unique list with the content of all the files
lines = read_files('README.md', 'requirements.txt')
```

## Make directories<a id="make-directories" name="make-directories"></a>
Create one or more directories but if them already exist, then do nothing.

```python
from mysutils.file import mkdirs

# Create the folder if not exists
mkdirs('new_folder')

# Do nothing because the folder was already created
mkdirs('new_folder')

# Create several folders at once
mkdirs('folder1', 'folder2', 'folder3')
```

## Move files<a id="move-files" name="move-files"></a>
Move several files at once.

```python
from mysutils.file import move_files

# Move several files to test/
move_files('test/', '1.txt', '2.txt', '3.txt')

# Create the folder test/ if it does not exist
move_files('test/', '1.txt', '2.txt', '3.txt', force=True)

# Replace the files if already exists in test/
move_files('test/', '1.txt', '2.txt', '3.txt', replace=True)
```

## List files<a id="list-files" name="list-files"></a>
Functions to list a folder and obtain the first or last file of a folder.

```python
from mysutils.file import first_file, last_file, list_dir

# Return a sorted list of files of the current directory.
list_dir()

# Return a sorted list of files of the 'test' directory.
list_dir('test')

# # Return the list of files thant end with '.txt' of the 'test' directory.



# Return the same list but with the inverted order
list_dir('test', '.*\.txt$', reverse=True)

# Return the path of the first file in the current folder
first_file()

# Return the path of the last file in the current folder
last_file()

# Return the path of the first file in the 'test' folder
first_file('test/')

# Return the path of the last file in the 'test' folder
last_file('test/')

# Return the path of the first file in the 'test' folder that ends with .txt
first_file('test/', r'.*\.txt$')

# Return the path of the last file in the 'test' folder that ends with .txt
last_file('test/', r'.*\.txt$')
```

## Generate output file paths<a id="generate-output-file-paths" name="generate-output-file-paths"></a>
Sometimes it is useful to generate a file name taken into account some parameters and the current timestamp.
This function generates this file paths.

```python
from mysutils.file import output_file_path

# Generate a file name in the current folder with the timestamp
file_path = output_file_path()

# Generate a file name in the 'model' folder with the timestamp
file_path = output_file_path('model')

# Generate a file name in the 'model' folder with the timestamp and .tar.gz as suffix.
file_path = output_file_path('model', '.tar.gz')

# Generate a file name in the 'model' folder with the timestamp, followed by the string "-svm-0.7-300-lemma",
# and .tar.gz as suffix.
filepath = output_file_path('model', '.tar.gz', True, method='svm', k=0.7, passes=300, lemma=True, stopw=False)

# Generate the same as previous but without timestamp
output_file_path('model', '.tar.gz', False, method='svm', k=0.7, passes=300, lemma=True, stopw=False)
```

## Check file encoding<a id="check-file-encoding" name="check-file-encoding"></a>
Check if a file content is compatible with a text encoding.

```python
from mysutils.file import has_encoding

# Return True if the file 1.txt is compatible with utf-8
has_encoding('1.txt', 'utf-8')
```

# Removable files<a id="removable-files"></a>
Many times it is necessary to remove temporal files after their use, even if there are any problem with the process.
These classes and functions allow you to self-removable files, temporally or not.

For example, with removable_tmp() function you can do:
```python
from mysutils.tmp import removable_tmp

# Create removable temporal file
with removable_tmp() as tmp:
    # Do something with the file tmp, for example:
    with open(tmp, 'wt') as file:
        print('Hello world', file=file)
# The tmp file is removed

# Create removable temporal folder
with removable_tmp(folder=True) as tmp:
    # Do something with the folder tmp
    ...
# The temporal folder is removed

# Create a file with suffix:
with removable_tmp(suffix='tar.gz') as tmp:
    # Do something with the file tmp
    ...
# The temporal folder is removed

# Create a file with suffix and prefix
with removable_tmp(suffix='tar.gz', prefix='prefix_') as tmp:
    # Do something with the file tmp
    ...
# The temporal folder is removed
```

Also, you can do the same with custom created files:
```python
from mysutils.tmp import removable_files
from mysutils.file import mkdirs

# Several files to remove
with removable_files('1.txt', '2.txt', '3.txt', 'x.out', 'y.out', 'z.out'):
    # Do something with the defined files, for example:
    with open('1.txt', 'wt') as file:
        print('Hello world', file=file)
# All the files are removed

# Create a removable file and assign it to a variable
with removable_files('1.txt') as (filename,):
  with open(filename, 'wt') as file:
        print('Hello world', file=file)
# The file is removed
      
# Several files to remove and assign them to variables
with removable_files('1.txt', '2.txt', '3.txt', 'x.out', 'y.out', 'z.out') as (f1, f2, f3, f4, f6):
    # Do something with the defined files, for example:
    with open(f1, 'wt') as file:
        print('Hello world', file=file)
    with open(f2, 'wt') as file:
        print('Goodbye world', file=file)
# All the files are removed

# A removable folders
with removable_files('data1', 'data2', recursive=True) as (d1, d2):
    mkdirs(d1, d2)
    # Do something with the folders
    ...
# Remove automatically the folders and their files
```

# Compressing files<a id="compressing-files" name="compressing-files"></a>
With this library there are two ways to compress files: single gzip files and tar files.

## Gzip<a id="gzip" name="gzip"></a>

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

## Tar<a id="tar" name="tar"></a>
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

### Create a tar file<a id="create-a-tar-file"></a>
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

# The compress method is selected automatically, but you can force it by the parameter compress_method
create_tar('test.tar', 'test.json', 'test.json.gz', compress_method='gz')
```

### List the content of a tar file<a id="list-the-content-of-a-tar-file"></a>

```python
from mysutils.tar import list_tar

lst = list_tar('test.tar.gz')
print(lst[0].path)
```

### Extract a specific file<a id="extract-a-specific-file"></a>
```python
from mysutils.tar import extract_tar_file

# Extract the file 'test.json' to 'test2.json' from 'test.tar.gz'. 
extract_tar_file('test.tar.gz', 'test2.json', 'test.json')

# Extract the file 'test.json' and save it into 'data/' folder from 'test.tar.gz'.
extract_tar_file('test.tar.gz', 'data/', 'test.json')

# The decompress method is selected automatically, but you can force it by the parameter compress_method
extract_tar_file('test.tar', 'data/', 'test.json', compress_method='gz')
```

### Extract several files into a folder<a id="extract-several-files-into-a-folder"></a>
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

In all the previous functions you can use __compress_method__ parameter to select manually which compression or 
decompression method you want to use.

### Add files to a TAR archive

```python
from mysutils.tar import create_tar, add_tar_files

# Create a tar file with a compressed json file
create_tar('test.tar', 'test.json.gz')
# Add the files to the tar file
add_tar_files('test.tar', 'test.json', 'test1.txt')

# This function also works with compressed tar files
create_tar('test.tar.gz', 'test.json.gz')
add_tar_files('test.tar.gz', 'test.json', 'test1.txt')

# The decompress method is selected automatically, but you can force it by the parameter compress_method
add_tar_files('test.tar', 'test.json', 'test1.txt', compress_method='gz')
```

### Open and load files inside a tar archive<a id="open-and-load-files-inside-a-tar-archive" name="open-and-load-files-inside-a-tar-archive"></a>
With these functions it is possible to open a stream to or load a yaml, json or pickle of a specific file inside a tar 
archive.

```python
from mysutils.tar import open_tar_file, load_tar_json, load_tar_pickle
from mysutils.yaml import load_tar_yaml
import json

# Open the file test.txt from test.tar.gz and print its content 
with open_tar_file('test.tar.gz', 'test.txt') as file:
    for line in file:
      print(line, end='')

# Load a json file inside a tar archive, even if it is also compressed
d = load_tar_json('test.tar.gz', 'test.json.gz')

# Load a pickle file inside a tar archive, even if it is also compressed
o = load_tar_pickle('test.tar.gz', 'test.pkl')

# Load a yaml file inside a tar archive, even if it is also compressed
d = load_tar_yaml('test.tar.gz', 'test.yaml.gz')
```

### Check if some files are inside a TAR file

```python
from mysutils.tar import create_tar, exist_tar_files

# Create a TAR file
create_tar('test.tar.gz', 'test.json', 'test.json.gz')
# This will return True
exist_tar_files('test.tar.gz', 'test.json', 'test.json.gz')
# This will return False
exist_tar_files('test.tar.gz', 'other.json', 'test.json.gz')
```

# External commands<a id="external-commands" name="external-commands"></a>
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

# Also you can introduce an unique string
std, err = execute_command('echo -n "This is a test"')
```

# Configuration files<a id="configuration-files" name="configuration-files"></a>

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

# Logging<a id="logging" name="logging"></a>
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

You have also the log_curl_request() function to 

```python
from logging import getLogger
from mysutils.logging import log_curl_request
from mysutils.text import AnsiCodes

logger = getLogger(__name__)

log_curl_request(logger.error,
                 'http://localhost:5000/world_domination',
                 'POST',
                 {'Content-Type': 'application/json'},
                 {'quantity_of_people': 'everybody'},
                 AnsiCodes.RED)
```

The previous code will print the following output but with the command in red color:

```bash
curl -X POST -H "Content-Type: application/json" "http://localhost:5000/world_domination" --data '{"quantity_of_people": "everybody"}'
```

# Method synchronization<a id="method-synchronization" name="method-synchronization"></a>
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

# Services and Web<a id="services-and-web" name="services-and-web"></a>

## Download a file<a id="download-a-file" name="download-a-file"></a>
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

## Endpoint<a id="endpoint" name="endpoint"></a>
In the contexts of a web service, you can need the base real final url to a service, that means, 
the protocol, IP or hostname and path to the service. 
You can obtain this with endpoint() function. This function is based on javascript, 
then it is necessary to use inside an HTML document.

An example, in all my services I create a start point (usually home page) to describe briefly how to use.
Depending on if I deploy this service locally or in the job server, the path to the service changes.
However, I would not like to remember to modify each time the service or any parameter. 
To avoid this, I use the endpoint() function in the HTML instructions like this:

```python
from fastapi import FastAPI, HTTPException
from mysutils.service import endpoint

app = FastAPI()

@app.get('/', response_class=HTMLResponse)
def home() -> str:
    """ Show the help.
    :return: The HTML code to show the help.
    """
    return f'<h1>My service</h1>\n' \
           '<p>With these services, you can do wonderful things. ' \
           'For example, with this one you can dominate the world:</p>\n' \
           '<code>' + \
           f'curl -X GET -L -i \'{endpoint("dominate")}?num_countries=&lt;NUM&gt;\'' \
           '</code>\n' \

```

If your service is in the URL https://www.example.com/services/dominate, this will generate a page like this:

> # My service
> With this service, you can do wonderful things. For example, with this one you can dominate the world:
> ```bash
> curl -X GET -L -i 'https://www.example.com/services/dominate?num_countries=&lt;NUM&gt;'
> ```

However, if you execute this command locally in port 8080,
the last URL will be: http://localhost:8080/dominate?num_countries=<NUM>.

This method works in both, FastAPI or Flask, and it maybe can work also in other server environments.

## Generate service help<a id="generate-service-help" name="generate-service-help"></a>

You can create a page with documentation about your service from a README.md or another Markdown file with the function
generate_service_help(). For example:

```python
from mysutils.fastapi import gen_service_help
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get('/help', response_class=HTMLResponse)
def home() -> str:
  """ Show the help.
  :return: The HTML code to show the help.
  """
  return gen_service_help('Page title', 'README.md', '# Web API',
                          '/service1', '/service2', '/service3')
```

This way, it will generate a Web page with the title 'Page title', using the information in the README.md file
from the section '# Web API' for the service endpoints 'service1', 'service2' and 'service3'.

If the endpoints are used, then, if in the readme threre are any url like 'https?://.*/serviceX', 
then it will return the real URL of the service.

*Note:* To use this function, you need to install markdown package, and, optionally, if you want colorful embedded code, you also need to install pygments:

```bash
pip install markdown~=3.3.6 Pygments>=2.10.0,~=2.11.2
```

## JSON post<a id="json-post" name="json-post"></a>
A very easy way to send a dictionary by means to http post, ot a json service.

```python
from mysutils.request import json_post

# Send the dictionary '{"msg": "Hello world!"}' to the service with that url 
json_post('https://postman-echo.com/post', {"msg": "Hello world!"})
```

# Git monitor<a id="git-monitor" name="git-monitor"></a>
Monitor a Git repository to check if there is any change in the remote repository with respect the local one.

```python
from mysutils.git import GitMonitor

# Function to execute when the is a change
def func(*files: str) -> None:
  # Print the changed files
  print(files)

# Create a monitor instance to execute one only time  
monitor = GitMonitor(func, 'local_dir', 'remote_url', 'branch_name')
# Execute the monitor
monitor.monitor()
# Execute the monitor as a thread
monitor.start()

# If you want to check the git repository several times you need add an interval to
monitor = GitMonitor(func, 'local_dir', 'remote_url', 'branch_name', interval=30)  # 30 seconds
# If you want to execute func() the first time although the repository has not changed, use force
monitor = GitMonitor(func, 'local_dir', 'remote_url', 'branch_name', force=True, interval=30)
```

# File unit tests<a id="unit-tests" name="unit-tests"></a>
A small class that inherits from TestCase and have methods to assert the typical file options like exists or isdir.

```python
from mysutils import unittest
from mysutils.file import touch, move_files

class MyTestCase(unittest.FileTestCase):
  # Check if some files exists and they have been moved successfully
  def test_move_files(self) -> None:
    touch('1.txt', '2.txt', '3.txt')
    move_files('test/', '1.txt', '2.txt', '3.txt')
    self.assertExists('test/1.txt', 'test/2.txt', 'test/3.txt')
    self.assertNotExists('1.txt', '2.txt', '3.txt')

  def test_encoding(self) -> None:
    # Check if the content of 1.txt, 2.txt and 3.txt are compatible
    # with iso8859-1 encoding.
    self.assertEncoding('1.txt', '2.txt', '3.txt', encoding='iso8859-1')
    # Check if the content of 1.txt, 2.txt and 3.txt are not compatible
    # with iso8859-1 encoding.
    self.assertEncoding('1.txt', '2.txt', '3.txt', encoding='iso8859-1')
```

# Miscellany<a id="miscellany" name="miscellany"></a>

Other no classifiable functions, like conditional() function that executes a function if a condition is True.
For example, if you need to do the following:

```python
from mysutils.misc import conditional

# The function to execute
def my_func(a: int, b: str, **kwargs) -> str:
    return f'Intent {a} of {b} for {kwargs["c"]}'

# Instead of doing this:
if a > b:
  my_func(1, 'apple', c='Lucas')

# You can do
conditional(my_func, a > b, 1, 'apple', c='Lucas')
```

# How to collaborate

I you want to collaborate with this project, please, <a href="mailto:jmgomez.soriano@gmail.com">contact with me</a>.