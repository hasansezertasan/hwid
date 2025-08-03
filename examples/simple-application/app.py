import json
import os
import pathlib

from hwid import get_hwid

if __name__ == "__main__":
    hwid = get_hwid()
    information = {
        "hwid": hwid,
    }

    file_path = Path(__file__).parent / "information.json"
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(information, f, ensure_ascii=False, indent=4)
    input()
