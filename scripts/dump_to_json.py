import json

def dump_to_json(dic, filename):
	json_file = open(f"database/{filename}.json", 'w')
	json.dump(dic, json_file, ensure_ascii=False, indent=2)
	json_file.close()
