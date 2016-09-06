# http://stackoverflow.com/questions/39262556/preserve-quotes-and-also-add-data-with-quotes-in-ruamel

from ruamel.yaml.scalarstring import SingleQuotedScalarString

if 'foo' in hiera and 'bar' in hiera['foo']:
    try:
        if 'el' not in hiera['foo']['bar']['myarray']:
            hiera['foo']['bar']['myarray'].append(SingleQuotedScalarString('el'))

    except:
        e = sys.exc_info()[0]
        print "Got %s when executing %s for %s" % (e, code_file, f)
