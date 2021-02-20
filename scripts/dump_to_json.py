import json

def dump_to_json(dic):
	json_file = open("database/coalition_users.json", 'w')
	json.dump(dic, json_file, ensure_ascii=False, indent=2)
	json_file.close()
	print("json updated!")
