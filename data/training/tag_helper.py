from pathlib import Path


def remove_duplicate_tags():
    tags = Path("./list_of_tags").read_text().splitlines()
    tags = sorted(list(set(tags)))
    Path("./list_of_tags").write_text("\n".join(tags))


if __name__ == '__main__':
    remove_duplicate_tags()
