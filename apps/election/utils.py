import json
import os


def get_json_data(file_path):
    with open(file_path, "r") as file:
        json_data = json.loads(file.read())
        return json_data


if __name__ == "__main__":
    print(__file__)
    print(os.path.abspath(__file__))
    d = get_json_data(
        r"C:\Users\USER\Desktop\voteX\apps\election\data\default_setting.json"
    )
    print(d)
    print(list(d.values()))
    print(list(d.values())[0])
