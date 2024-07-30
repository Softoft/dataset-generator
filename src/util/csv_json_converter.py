import csv
import json
import random

import pandas as pd


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


def json_to_csv_splitting_tags(json_file_path, columns, output_file):
    with open(json_file_path, encoding='utf-8') as json_file:
        data = json.load(json_file)

    df = pd.json_normalize(data)
    number_tags = 5
    tags_df = df['tags'].apply(
        lambda x: x + [None] * (number_tags - len(x)) if len(x) < number_tags else x[:number_tags]).apply(pd.Series)
    tags_df.columns = [f'tag_{i + 1}' for i in range(number_tags)]
    result_df = pd.concat([df.drop(columns=['tags']), tags_df], axis=1)
    result_df = result_df[columns + [f'tag_{i + 1}' for i in range(number_tags)]]
    result_df.to_csv(output_file, index=False)


def csv_to_json(csv_file_path, json_file_path):
    with open(csv_file_path, encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = list(csv_reader)
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


""""
    body: str
    answer: str
    type: TicketType
    queue: TicketQueue
    priority: Priority
    language: Language
    business_type: str
    product_category: str
    product_sub_category: str
    product: str]
    """
if __name__ == '__main__':
    json_to_csv_splitting_tags("../../data/training/dataset-v3_8_0-1k.json",
                               ["subject", "body", "answer", "type", "queue", "priority", "language", "business_type"],
                               "../../data/clean_production_data/ticket-helpdesk-multi-lang_3_8.csv")
