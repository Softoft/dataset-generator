import csv
import json
import random

import pandas as pd


def json_to_csv(json_file_path, csv_file_path, shuffle=True, max_size=10 ** 6):
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


def delete_duplicate_values(tickets: list[dict], columns: list[str]) -> list[dict]:
    columns_used_values: dict[str, set] = { column: set() for column in columns }
    unique_tickets = []
    for ticket in tickets:
        ticket_values = { column: ticket[column] for column in columns }
        if all(ticket_values[column] not in columns_used_values[column] for column in columns):
            unique_tickets.append(ticket)
            for column in columns:
                columns_used_values[column].add(ticket_values[column])
    return unique_tickets


def json_to_csv_splitting_tags(json_file_path, columns, output_file, order_by=None, shuffle=True, number_tags=5,
                               max_size=10 ** 100):
    with open(json_file_path, encoding='utf-8') as json_file:
        data = json.load(json_file)
    if order_by:
        data = sorted(data, key=lambda x: x[order_by])
    elif shuffle:
        random.shuffle(data)
    data = delete_duplicate_values(data, ["subject", "body", "answer"])
    df = pd.json_normalize(data)[:max_size]
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
    json_to_csv_splitting_tags("../../data/training/dataset-v3_27_3-big-release.json",
                               ["id", "subject", "body", "answer", "type", "queue", "priority", "language",
                                "business_type"],
                               "../../data/clean_production_data/helpdesk_customer_tickets.csv", order_by="id",
                               number_tags=9)
