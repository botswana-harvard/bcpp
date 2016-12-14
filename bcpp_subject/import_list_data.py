import json

data = {}
filename = '/Users/erikvw/source/bcpp/bcpp_subject/lists.txt'

with open(filename, 'r') as f:
    json_text = f.read()
    json_object = json.loads(json_text)
for obj in json_object:
    d = []
    if obj.get('model').startswith('bcpp_list'):
        model = obj.get('model')
        fields = obj.get('fields')
        try:
            data[model]
        except KeyError:
            data[model] = []
        name, shortname = None, None
        for fname, value in obj.get('fields').items():
            if fname == 'name':
                name = value
            if fname == 'short_name':
                shortname = value
            if name and shortname:
                data[model].append((name, shortname))
                name, shortname = None, None
