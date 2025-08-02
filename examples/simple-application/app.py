import json
import os
import pathlib

from hwid import get_hwid

if __name__ == "__main__":
    hwid = get_hwid()
    information = {
        "hwid": hwid,
    }

    basedir = pathlib.Path(pathlib.Path(__file__).parent).resolve()
    file = os.path.join(basedir, "information.json")
    with open(file, "w", encoding="utf-8") as f:
        json.dump(information, f, ensure_ascii=False, indent=4)
    input()
