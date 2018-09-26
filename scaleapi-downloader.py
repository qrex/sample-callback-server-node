#!/usr/bin/env python3
import json
import argparse
import urllib

from pymongo import MongoClient


def collect_task_results(label, url):
    with MongoClient(url) as client:
        db = client.get_database()
        with db.tasks.find({'metadata.label': label}) as mongo_cursor:
            data_list = []
            for data_row in mongo_cursor:
                result = False
                if data_row["response"]["category"] == "is_bug":
                    result = True
                reviews_dict = data_row["metadata"]["review"]
                reviews_dict["is_bug"] = result

                data_list.append(reviews_dict)
    return data_list


def main():
    parser = argparse.ArgumentParser(description='Send review to be classified to scaleapi')
    parser.add_argument('-l', '--label', required=True, help='Label for the reviews')
    parser.add_argument('url', help='URL of mongodb, e.g. mongodb://localhost:27017/test')
    parser.add_argument('file', help='Json file with reviews to label')
    args = parser.parse_args()

    data = collect_task_results(args.label, args.url)
    with open(args.file, "w", encoding='utf-8') as write_file:
        json.dump(data, write_file, ensure_ascii=False)


if __name__ == '__main__':
    main()
