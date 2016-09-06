# http://stackoverflow.com/questions/39262556/preserve-quotes-and-also-add-data-with-quotes-in-ruamel

from ruamel.yaml.scalarstring import SingleQuotedScalarString, DoubleQuotedScalarString

hiera['foo'] = SingleQuotedScalarString('bar')
hiera['bar'] = DoubleQuotedScalarString('baz')

# This will add the following at the end of every YAML file:
# foo: 'bar'
# bar: "baz"
