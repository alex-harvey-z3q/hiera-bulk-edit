# http://stackoverflow.com/questions/39307956/insert-a-key-using-ruamel/39308307#39308307

if hasattr(hiera, '_yaml_comment'):
    yaml_comment = hiera._yaml_comment

hiera = ruamel.yaml.comments.CommentedMap(sorted(hiera.items(), key=lambda t: t[0]))

if hasattr(hiera, '_yaml_comment'):
    hiera._yaml_comment = yaml_comment
