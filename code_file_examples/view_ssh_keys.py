# You may need to run pip install clint first to run this example.

from clint.textui import puts, colored, indent

if 'profile::base::users' in hiera and 'ec2-user' in hiera['profile::base::users'] and 'ssh_keys' in hiera['profile::base::users']['ec2-user']:
    try:
        print "In %s:" % f
        puts(colored.green("hiera['profile::base::users']['ec2-user']:"))
        with indent(4):
            puts(colored.green(ruamel.yaml.round_trip_dump(hiera['']['ec2-user'])))

    except:
        e = sys.exc_info()[0]
        print "Got %s when executing %s for %s" % (e, code_file, f)
