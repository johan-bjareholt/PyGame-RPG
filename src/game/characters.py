import datetime
import os
import ConfigParser
import globals as globs


basechar = {
	'General':
		{
			'Name',
			'Created'
		},
	'Appearance':
		{
			'hairstyle',
			'haircolor',
			'eyecolor'
		},
	'Attributes':
		{
			'Strength',
			'Agility',
			'Inteligence',
			'Vitality',
			'Magicka'
		},
	'Skills':
		{
			'Onehanded',
			'Marksmanship',
			'Destruction'
		},
	'Equipment':
		{
			'Head',
			'Chest',
			'Legs',
			'Feet',
			'Mainhand',
			'Offhand'
		},
	'Inventory':
		{
			'0',
			'1',
			'2',
			'3',
			'4',
			'5',
			'6',
			'7',
			'8',
			'9',
			'10',
			'11',
			'12',
			'13',
			'14',
			'15',
			'16',
			'17',
			'18',
			'19',
		}
}


def create(name, appearance={"hairstyle": "hair1", "haircolor": (200,120,110),"eyecolor": (0,0,255)}):
	config = ConfigParser.RawConfigParser()

	for section in basechar:
		config.add_section(section)
		print(section)
		for setting in basechar[section]:
			print(setting)
			global value
			if section == 'General':
				if setting == 'Name':
					value = name
				elif setting == 'Created':
					value = datetime.datetime.now()
			elif section == 'Attributes' or section == 'Skills':
				value = 1
			if section == 'Appearance':
				if type(appearance[setting]) == tuple:
					value = ""
					for part in appearance[setting]:
						value += str(part) + ","
					#value = appearance[setting]
				if type(appearance[setting]) == str:
					value = appearance[setting]
			else:
				print("Unknown setting {}.{}".format(section, setting))

			config.set(section, setting, value)
			print("Created setting {}.{} as {}".format(section, setting, value))
			value = 0

	# Writing our configuration file to 'example.cfg'
	with open(globs.cwd+'/game/characters/{}'.format(name), 'w+') as configfile:
	    config.write(configfile)

def listCharacters():
	characters = os.listdir(globs.cwd+'/game/characters/')
	for char in characters:
		if char[0] == '.':
			characters.remove(char)
	return characters

def remove(name):
	try:
		location = globs.cwd+'/game/characters/{}'.format(name)
		os.remove()
		return True
	except Exception as e:
		return False

def load(name):
	location = globs.cwd+'/game/characters/{}'.format(name)
	config = ConfigParser.RawConfigParser()
	config.read([location])

	character = {}

	for section in config.sections():
		character[section] = {}
		for option in config.options(section):
			character[section][option] = config.get(section, option)

	return character
	#print(config.read(location))
	#return config.read(location)

	#try:
	#	with open(location, 'r') as configfile:
	#	    return config.read(configfile)
	#except IOError:
	#	print("Could not find character!")
	#	globs.location = "main.characters"