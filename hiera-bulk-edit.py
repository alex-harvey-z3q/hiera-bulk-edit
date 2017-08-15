#!/usr/bin/env python

import ruamel.yaml
import sys, os, re, glob2
import braceexpand
from braceexpand import braceexpand
from compiler.ast import flatten

def usage():
    print 'Hiera Bulk Edit.  Programmatically update human-edited Hiera YAML files.'
    print ''
    print 'Usage: %s <paths> <code_file>' % __file__
    print ''
    print "Example invocation: %s '*/puppet-control/hieradata' do_stuff_to_hiera.py" % __file__
    print '''
Bash-style globbing and brace expansion is valid in the specification of <paths>.

The <code_file> must contain Python code that will be exec'ed by the calling script.

Example code file:

The following example replaces all hiera['foo']['bar'] keys
with the values specified:

try:
    # 'hiera' is the Ruamel Dictionary structure that represents the
    # Hiera file's YAML data. The purpose of this code is always to edit
    # the 'hiera' dictionary in some way before it is written back to
    # disk.

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
    print 'Got %s when executing %s for %s' % (e, f)
'''
    exit(1)

def check_paths(paths):
    for p in paths:
        for _p in list(braceexpand(p)):
            if glob2.glob(_p) == []:
                if not os.path.exists(_p):
                    print '%s not found' % _p
                    usage()

def yaml_files(paths):
    expanded = flatten([glob2.glob(p + '/**/*.yaml') for p in list(braceexpand(paths))])
    return expanded

def code_file_data(f):
    with open(f, 'r') as _f:
        code_file_data = _f.read()
    return code_file_data

def read_file(f):
    if ruamel.yaml.version_info >= (0, 15, 30):
        yaml = ruamel.yaml.YAML()
        yaml.preserver_quotes = True
        with open(f, 'r') as _f:
            return yaml.load(_f)
    with open(f, 'r') as _f:
        return ruamel.yaml.round_trip_load(
            _f,  # for large files it is somewhat better not to read everything in memory
            preserve_quotes=True)

def write_file(f, data):
    if ruamel.yaml.version_info >= (0, 15, 30):
        yaml = ruamel.yaml.YAML()
        yaml.explicit_start = True
        yaml.width = 1024
        yaml.indent(mapping=2, sequence=4, offset=2)
        with open(f, 'w') as _f:
            yaml.dump(data, stream=_f)
        return
    with open(f, 'w') as _f:
        ruamel.yaml.dump(
            data,
            stream=_f,
            Dumper=ruamel.yaml.RoundTripDumper,
            explicit_start=True,
            width=1024)

# main

try:
    script_name, yaml_path, code_file = sys.argv
except:
    usage()

check_paths([code_file, yaml_path])
code_file_data = code_file_data(code_file)

for f in yaml_files(yaml_path):
    hiera  = read_file(f)
    _hiera = read_file(f)

    # execute the arbitrary python code in code_file.
    try:
        exec(code_file_data)
        if hiera == _hiera:
            print 'No changes to make in %s' % f
        else:
            print 'Updated for %s' % f
            write_file(f, hiera)

    except:
        print 'Got %s when executing %s for %s' % (sys.exc_info(), code_file, f)
