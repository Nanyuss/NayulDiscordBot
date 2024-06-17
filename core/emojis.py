import yaml
from dataclasses import dataclass

def get_emojis():
	with open("./core/resources/emojis.yml", encoding="utf-8") as file:
		return yaml.safe_load(file)
		
@dataclass
class Emoji:
	emojis = get_emojis()
	
	# Emojis de Insígnias
	active_developer = emojis["active_developer"]
	verified_bot_developer = emojis["verified_bot_developer"]
	hypesquad = emojis["hypesquad"]
	hypesquad_balance = emojis["hypesquad_balance"]
	hypesquad_bravery = emojis["hypesquad_bravery"]
	hypesquad_brilliance = emojis["hypesquad_brilliance"]
	partner = emojis["partner"]
	bug_hunter = emojis["bug_hunter"]
	bug_hunter_level_2 = emojis["bug_hunter_level_2"]
	early_supporter = emojis["early_supporter"]
	staff = emojis["staff"]
	discord_certified_moderator = emojis["discord_certified_moderator"]
	spammer = emojis["spammer"]
	verified_bot = emojis["verified_bot"]
	unverified_bot = emojis["unverified_bot"]
	
	# Emojis de Checagem
	check = emojis["check"]
	error = emojis["error"]
	
	# Emojis de Carregamento
	loading_v1 = emojis["loading_v1"]
	loading_v2 = emojis["loading_v2"]
	
	# Emojis de Navegação
	left = emojis["left"]
	right = emojis["right"]
	back = emojis["back"]
	
	# Emojis de Membros
	new_member = emojis["new_member"]
	booster_lv1 = emojis["booster_lv1"]
	crown = emojis["crown"]
	
	# Emojis de Ícones Gerais
	icon_user = emojis["icon_user"]
	icon_settings = emojis["icon_settings"]
	icon_role = emojis["icon_role"]
	icon_emoji = emojis["icon_emoji"]
	icon_edit = emojis["icon_edit"]
	info = emojis["info"]
	image = emojis["image"]
	splash = emojis["splash"]
	banner = emojis["banner"]
	settings_animated = emojis["settings_animated"]
	discord_icon = emojis["discord_icon"]
	
	# Emojis de Ações
	add = emojis["add"]
	paper = emojis["paper"]
	annotation = emojis["annotation"]
	paleta = emojis["paleta"]
	list = emojis["list"]
	footer = emojis["footer"]
	delete = emojis["delete"]
	exportar = emojis["exportar"]
	importar = emojis["importar"]
	send = emojis["send"]
	webhook = emojis["webhook"]
	accept = emojis["accept"]
	reject = emojis["reject"]
	
	# Emojis de Identificação
	id_icon = emojis["id_icon"]
	members = emojis["members"]
	
	# Emojis de Categorias
	icon_calendar = emojis["icon_calendar"]
	icon_category = emojis["icon_category"]
	icon_badge = emojis["icon_badge"]