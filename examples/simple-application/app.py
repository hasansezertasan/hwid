"""Simple application example that saves HWID to a file."""

# Copyright (c) 2023 Hasan Sezer Taşan
# Licensed under the MIT License

import json
from pathlib import Path

from hwid import get_hwid


def main() -> None:
    """Extract and save the hardware ID of this machine."""
    hwid = get_hwid()
    information = {"hwid": hwid}

    file_path = Path(__file__).parent / "information.json"
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(information, f, ensure_ascii=False, indent=4)

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
