# Hiera Bulk Edit

This tool facilitates the programmatic bulk editing of Hiera YAML files (or any YAML files really).

By allowing the execution of arbitrary python code on the YAML data in memory, a powerful and flexible interface for programmatically updating human-edited Hiera data is provided.  The heavy lifting is done by Anthon van der Neut's [Ruamel](https://bitbucket.org/ruamel/yaml) Python library, and we respect most of the human-edited formatting and commenting of the input file.

# Why Python

Because [there is only one](https://www.ruby-forum.com/topic/6877080) YAML parser that preserves formatting and comments and it's a Python library!

# Install dependencies

Install the Ruamel YAML library:

```
$ pip install -r requirements.txt 
```

You should end up with ruamel.yaml version 0.12.7 or higher:

```
$ pip list ruamel.yaml |grep ruamel
ruamel.ordereddict (0.4.9)
ruamel.yaml (0.12.7)
```

# Usage

```
$ hiera-bulk-edit.py <paths> <code_file>.py
```

Note that Bash Globbing and Brace Expansion are supported in `<paths>`.

## Example usage

```
$ hiera-bulk-edit.py '*/control_repo/hieradata' do_stuff_to_hiera.py
```

## Example code files

The following example replaces all `hiera['foo']['bar']` keys
with the values specified:

```python
try:
    # 'hiera' is the Ruamel Dictionary structure that represents the
    # Hiera file's YAML data. The purpose of the block of code is always
    # to edit this dictionary in some way before the calling script
    # writes it back to disk.

    hiera['foo']['bar'] = {
        'key1': 'val1',
        'key2': 'val2',
    }

except:
    # We would get to here if, for example, the Hiera file does not contain the
    # key hiera['foo'].
    e = sys.exc_info()[0]

    # The following variables are also available from the calling script's scope:
    #   'f' is the filename of the file being edited.
    print "Got %s when updating %s" % (e, f)
```

### Adding a key with formatting

```python
# add_a_key_with_quotes.py
# http://stackoverflow.com/questions/39262556/preserve-quotes-and-also-add-data-with-quotes-in-ruamel

from ruamel.yaml.scalarstring import SingleQuotedScalarString, DoubleQuotedScalarString

hiera['foo'] = SingleQuotedScalarString('bar')
hiera['bar'] = DoubleQuotedScalarString('baz')
```

This will add two new keys to the bottom of each YAML file.

### Deleting all keys starting with a pattern

```python
# delete_all_fluentd_keys.py
for k in hiera.keys():
    if k.startswith('fluentd'):
        hiera.pop(k)
```

### More examples

Look in the `code_file_examples` directory.

## Variables in the code file

### hiera

The Hiera YAML data is stored in a Python Dictionary called `hiera`.

### f

The file name of the YAML file being edited is stored in `f`.

## Known issues

The Ruamel library does not preserve all indentation styles but normalises the input file.  Inconsistencies in the human-edited indentation would be reset by the Bulk Edit script.  Likewise, whitespaces are not always preserved.

The Ruamel project is still in beta and other bugs may come to light.  Proceed cautiously and check all diffs before merging changes.

## Acknowledgements

All credit to Anthon van der Neut for Ruamel.yaml, and in particular for his help on Stack Overflow and his quick response to bug reports.
