import json

def dump_to_json(database_name, dic):
	json_file = open(f"database/{database_name}.json", 'w')
	json.dump(dic, json_file, ensure_ascii=False, indent=2)
	json_file.close()
	print("json updated!")
