import csv
import json
import random


def json_to_csv(json_file_path, csv_file_path, shuffle=False, max_size=10 ** 6):
    with open(json_file_path, encoding='utf-8') as json_file:
        data = json.load(json_file)
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        header = data[0].keys()
        csv_writer.writerow(header)
        if shuffle:
            random.shuffle(data)
        for row in data[:max_size]:
            csv_writer.writerow(row._values())


def csv_to_json(csv_file_path, json_file_path):
    with open(csv_file_path, encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = list(csv_reader)
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    json_to_csv("../../data/extras/gpt-4-multi-lang-big-1k-randomized.json",
                "../data/clean_production_data/ticket-helpdesk-multi-lang.csv",
                True, 400)
