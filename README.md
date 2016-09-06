# Hiera Bulk Edit

This tool facilitates the programmatic bulk editing of Hiera YAML files.

By allowing the execution of arbitrary python code on the YAML data in memory, a powerful and flexible interface for programmatically updating human-edited Hiera data is provided.  The heavy lifting is done by Anthon van der Neut's [Ruamel](https://bitbucket.org/ruamel/yaml) Python library, and we respect most of the human-edited formatting and also preserve the commenting in the input file.

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

Note that Bash Globbing and Brace Expansion are supported in <paths>.

## Example command line

```
$ hiera-bulk-edit.py '*/control_repo/hieradata' do_stuff_to_hiera.py
```

## Example code files

### Adding a key with formatting

```python
# add_a_key_with_quotes.py
# http://stackoverflow.com/questions/39262556/preserve-quotes-and-also-add-data-with-quotes-in-ruamel

from ruamel.yaml.scalarstring import SingleQuotedScalarString, DoubleQuotedScalarString

hiera['foo'] = SingleQuotedScalarString('bar')
hiera['bar'] = DoubleQuotedScalarString('baz')
```

```
$ hiera-bulk-edit.py '*/puppet-control/hieradata' add_a_key_with_quotes.py
```

This will add two new keys to the bottom of each YAML file found under '*/puppet-control/hieradata'.

### Deleting all keys starting with a pattern

```python
# delete_all_fluentd_keys.py
for k in hiera.keys():
    if k.startswith('fluentd'):
        hiera.pop(k)
```

```
$ hiera-bulk-edit.py '*/puppet-control/hieradata' delete_all_fluentd_keys.py
```

### More examples

Look in the `code_file_examples` directory.

## Known issues

The Ruamel library does not preserve all indentation styles but normalises the input file.  Inconsistencies in the human-edited indentation would be reset by the Bulk Edit script.  Likewise, whitespaces are not always preserved.

The Ruamel project is still in beta and other bugs may come to light.  Proceed cautiously and check all diffs before merging changes.

