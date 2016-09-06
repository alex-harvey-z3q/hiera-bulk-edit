# Delete all keys that start with 'foo'.

for k in hiera.keys():
    if k.startswith('foo'):
        hiera.pop(k)
