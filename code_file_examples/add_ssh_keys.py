# http://stackoverflow.com/questions/39262556/preserve-quotes-and-also-add-data-with-quotes-in-ruamel

#    ssh_keys:
#      joe_smith@example.com:
#        type: 'ssh-rsa'
#        key: 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDSWvVUwYDFbFEoYPSQAJBLwuWUVnfQG0tVSKWNK7Q+Pt4BWoK4qW9oaZs6vKQLSEwHhXsygu6JsggT+pzbTQ4PCbcEZqNyBo3X5D+tvc1mVqYB+oL0aTyFB+gt6/RZxsPF4J3ihDHNQXG6gIZ5SI21u5gkRnWWz3E9XRkhHOPDnjwkpTqo6lnNVVsGUhVRTEy2G9rvwHA6K8ZxSEwhPzFS2Wv9HgEng22ojJ3MSDrrBDa/FBxSsZhieajdEPev73qUB9od3YNbzyMbiXdHmk7GFlckxEi9twT+vOrZdOxJVZylSPFqIDr1V5buk9mPyav9wN3ntqGAqj42pXdmNaNd joe@joe.local'

from ruamel.yaml.scalarstring import SingleQuotedScalarString

team_keys = {
    'joe_smith@example.com':  'AAAAB3NzaC1yc2EAAAADAQABAAABAQDSWvVUwYDFbFEoYPSQAJBLwuWUVnfQG0tVSKWNK7Q+Pt4BWoK4qW9oaZs6vKQLSEwHhXsygu6JsggT+pzbTQ4PCbcEZqNyBo3X5D+tvc1mVqYB+oL0aTyFB+gt6/RZxsPF4J3ihDHNQXG6gIZ5SI21u5gkRnWWz3E9XRkhHOPDnjwkpTqo6lnNVVsGUhVRTEy2G9rvwHA6K8ZxSEwhPzFS2Wv9HgEng22ojJ3MSDrrBDa/FBxSsZhieajdEPev73qUB9od3YNbzyMbiXdHmk7GFlckxEi9twT+vOrZdOxJVZylSPFqIDr1V5buk9mPyav9wN3ntqGAqj42pXdmNaNd',
    'joe_bloggs@example.com': 'AAAAB3NzaC1yc2EAAAADAQABAAABAQDqNKFOy4kYtMEPLEqAPR5crpLNiIkxxtdA4+MGMJbocQZNmBulWfbgeWbYnqE/IsjTUY8TWDjc34vHVxEuOb1vKP4Qn56vTWGmxyQXRDZbscO/UwQ8NHquFggDKK+xWg9v/VVCp1gPrz95DO7qjihZK3uqOZCfssdrMFI8dE/swZeaXBTmsPf2mj9FaI2SOuahdNd1wCMs64Fqhs7rwsk5O8I4L83Or8ttFXjmTELhjn3bs6odZYmtb0jiOlohJrQ/+IsOcJ4qwHtC96fQhDkH+YIC6FoaThn5ZFBlOkRoIpe49DFv/kbGQNufLrIZSGwq9dnnphfclWbXmy0G1IbF',
}

if 'profile::base::users' in hiera and 'ec2-user' in hiera['profile::base::users'] and 'ssh_keys' in hiera['profile::base::users']['ec2-user']:
    try:
        for email, key in team_keys.items():
            if email not in hiera['profile::base::users']['ec2-user']['ssh_keys']:
                hiera['profile::base::users']['ec2-user']['ssh_keys'][email] = {
                    'type': SingleQuotedScalarString('ssh-rsa'),
                    'key': SingleQuotedScalarString(key),
                }

    except:
        e = sys.exc_info()[0]
        print "Got %s when executing %s for %s" % (e, code_file, f)
