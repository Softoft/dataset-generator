# Open JSON File and count the number of items

import json
import uuid
from dataclasses import dataclass
from pathlib import Path
import random


@dataclass
class FileInformation:
    file_path: Path
    version: int


def merge_json_and_assign_uuid(files: list[FileInformation], output: str):
    merged = []
    for file_information in files:
        with open(file_information.file_path) as file:
            data = json.load(file)
            for item in data:
                item["id"] = str(uuid.uuid4())
                item["version"] = file_information.version
                merged.append(item)

    random.shuffle(merged)
    print(f"Total number of items: {len(merged)}")
    with open(output, "w") as out:
        json_string = json.dumps(merged, indent=4)
        out.write(json_string)


if __name__ == '__main__':
    files = [
        FileInformation(Path('../../data/training/dataset-v3_27_0-big-release.json'), 2),
        FileInformation(Path('../../data/training/dataset-v3_27_1-big-release.json'), 2),
        FileInformation(Path('../../data/training/dataset-v3_27_2-big-release.json'), 2),
        FileInformation(Path('../../data/training/dataset-v3_27_3-big-release.json'), 2),
        FileInformation(Path('../../data/extras/gpt-4-multi-lang-big-8k-15-07.json'), 1),
    ]
    output = "../../data/pre-release/dataset-tickets-multi-lang-uncleaned-release-candidate.json"
    merge_json_and_assign_uuid(files, output)
