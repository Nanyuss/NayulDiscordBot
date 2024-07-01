import yaml

def Permissions():
	with open("./core/resources/locale/permissions.yml", "r", encoding="utf-8") as file:
		return yaml.safe_load(file)