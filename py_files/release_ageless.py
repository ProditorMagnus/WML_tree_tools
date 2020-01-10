#!/usr/bin/python3
from os.path import join
import re
import preprocess_addon

# Not needed, agreed with Soliton that wmlunits timeout will be large enough

preprocess_addon.preprocess_addon("Ageless_Era")

main_path = join("..", "preprocessed_addon", "Ageless_Era", "_main.cfg")
out_path = join("..", "preprocessed_addon", "ageless_4_25.preprocessed.cfg")

with open(main_path, encoding="utf8") as f:
    with open(out_path, "w", encoding="utf8") as g:
        file = f.read()
        print("len before", len(file))
        output = file
        output = re.sub('"(.*?)"', '<<\\1>>', output, flags=re.DOTALL)
        output = re.sub('>><<', '"', output, flags=re.DOTALL)
        print("len after", len(output))
        g.write(output)
