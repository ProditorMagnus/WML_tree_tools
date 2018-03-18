from subprocess import call
from os.path import join
import re

wesnoth_dir = r"C:\Users\Ravana\Desktop\general\wesnoth-related\mydev1.12.6"
wesnoth_path = join(wesnoth_dir,"wesnoth-mydev.exe")
core_path = join(wesnoth_dir,"data")

main_path = join("..","preprocessed_addon","_main.cfg")
out_path = join("..","preprocessed_addon","ageless_4_19.preprocessed.cfg")

with open(main_path, encoding="utf8") as f:
	with open(out_path, "w", encoding="utf8") as g:
		file = f.read()
		print("len before",len(file))
		output = file
		output = re.sub('"(.*?)"', '<<\\1>>', output, flags=re.DOTALL)
		output = re.sub('>><<', '"', output, flags=re.DOTALL)
		print("len after",len(output))
		g.write(output)
