# Reduce number of classes for detection:
# - 'player': Don't distinguish between teams and player/keeper
# - 'ball'
# - 'field_center'

import os

IN_DIR = "../images/"
OUT_DIR = "../reduced_labels/"

MAPPING = {
    "1": "0",
    "2": "1",
    "3": "1",
    "4": "1",
    "5": "1",
    "6": "2"

}
for file in os.listdir(IN_DIR):
    if file.endswith(".txt"):
        with open(IN_DIR + file) as f:
            lines = f.readlines()

            with open(OUT_DIR + file, 'w') as out_f:
                for line in lines:
                    cls = line[0]
                    if cls in MAPPING:
                        out_f.write(MAPPING[cls] + line[1:])

