import sys, json 

json_ = sys.argv[1]
dict_ = json.loads(json_)

print(json.dumps(dict_))