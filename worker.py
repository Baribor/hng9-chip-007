#pylint:disable=W0603
# pylint:disable=W0621
import csv
import json
import hashlib
import os


team_data = {
    "Team Bevel": (1, 20),
    "Team Clutch": (21, 40),
    "Team Engine": (41, 60),
    "Team Grit": (61, 80),
    "Team Prybar": (81, 100),
    "Team Chisel": (101, 120),
    "Team Brainbox": (121, 140),
    "Team Plug": (141, 160),
    "Team Headlight": (161, 180),
    "Team Crankshaft": (181, 200),
    "Team Gear": (201, 220),
    "Team Tape": (221, 240),
    "Team Axle": (241, 260),
    "Team PowerDrill": (261, 280),
    "Team Hydraulics": (281, 300),
    "Team Scale": (301, 320),
    "Team Sandpaper": (321, 340),
    "Team Ruler": (341, 360),
    "Team Vbelt": (361, 380),
    "Team Axe": (381, 400),
    "Team Boot ": (401, 420),
}

data = []
hashes = {}
sn, file_name, desc, gender, uuid, _ = [None] * 6
column2index = {}


def get_team_name(index):
    """
    Given an a serial number, returns the name of the team that is assigned the serial number.
    """
    for key, value in team_data.items():
        if index in range(value[0], value[1] + 1):
            return key


def create_json():
    global column2index, file_name

    if not os.path.exists("output files"):
        os.mkdir("output files")

    for file in os.listdir("input files"):

        with open(f"input files/{file}") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            line_count = 0

            for row in csv_reader:
                if line_count == 0:
                    sn, file_name, desc, gender, uuid, _ = row
                    column2index = {n: i for i, n in enumerate(row)}
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:

                    item = {
                        "format": "CHIP-0007",
                        "name": row[column2index[file_name]],
                        "description": row[column2index[desc]],
                        "minting_tool": get_team_name(int(row[column2index[sn]])),
                        "sensitive_content": False,
                        "series_number": row[column2index[sn]],
                        "series_total": 526,
                        "attributes": [
                            {
                                "trait_type": "gender",
                                "value": row[column2index[gender]],
                            },
                            {"trait_type": "uuid", "value": row[column2index[uuid]]},
                        ],
                        "collection": {
                            "name": "Zuri NFT Tickets for Free Lunch",
                            "id": "b774f676-c1d5-422e-beed-00ef5510c64d",
                            "attributes": [
                                {
                                    "type": "description",
                                    "value": "Rewards for accomplishments during HNGi9.",
                                }
                            ],
                        },
                    }
                    file = f"{row[column2index[file_name]]}.json"
                    with open(f"output files/{file}", "w") as output:
                        output.write(json.dumps(item, indent=4))
                    data.append(file)


def generate_hashes():
    """
    Generates the sha256 hash for each created json file.
    """
    for f in data:
        with open(f"output files/{f}", "rb") as file:
            h = hashlib.sha256(file.read()).hexdigest()
            hashes[f.split(".")[0]] = h


def create_output():
    """
    Creates an output file with the name format file_name.output.csv with the hash of each row appended.
    """

    if not os.path.exists("outputs"):
        os.mkdir("outputs")

    for file in os.listdir("input files"):
        with open(f"input files/{file}", "r") as read_file, open(
            f'outputs/{file.split(".")[0]}.output.csv', "w"
        ) as write_file:
            cr = csv.reader(read_file)
            cw = csv.writer(write_file)
            line_count = 0
            for row in cr:
                if line_count == 0:
                    row.append("CHIP Hash-sha256")
                    line_count += 1

                else:

                    row.append(hashes[row[column2index[file_name]]])
                cw.writerow(row)


if __name__ == "__main__":

    create_json()
    generate_hashes()
    create_output()
