import csv
import json
import io
# Counting

stem = True if input('stemmed?') == 'y' else False

FILE_IN = 'training-data-stemmed.tsv' if stem else 'training-data.tsv'
FILE_OUT = 'training-data-2-stemmed.json' if stem else 'training-data-2.json'
data = {
    "tags": {
        '<S>': {
            "count": 1
        }
    },
    "transitions": {}
}

with open(FILE_IN) as training_data:
    reader = csv.reader(training_data, delimiter='\t')
    last_tag = '<S>'

    for row in reader:
        if len(row) == 0:
            last_tag = '<S>'
            data['tags'][last_tag]['count'] += 1
            continue

        token = row[0].lower()
        tag = row[1].upper()
        transition = f'{last_tag}-{tag}'
        last_tag = tag

        if tag in data["tags"]:
            data["tags"][tag]["count"] += 1
        else:
            elem = {
                "count": 1,
                "type": {}
            }
            data["tags"][tag] = elem

        if token in data["tags"][tag]["type"]:
            data["tags"][tag]["type"][token] += 1
        else:
            data["tags"][tag]["type"][token] = 1

        if transition in data["transitions"]:
            data["transitions"][transition] += 1
        else:
            data["transitions"][transition] = 1


with io.open(FILE_OUT, 'w', encoding="utf8") as training_data_json:
    json.dump(data, training_data_json, ensure_ascii=False)
