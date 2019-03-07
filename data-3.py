import csv
import json
import io
# Counting

FILE_IN = 'training-data.tsv'
FILE_OUT = 'training-data-3.json'
data = {
    "tags": {
        '<S>': {
            "count": 1,
            "type": {
                "": 1
            }
        }
    },
    "transitions": {}
}

with open(FILE_IN) as training_data:
    reader = csv.reader(training_data, delimiter='\t')
    first_tag, second_tag = '<S>', '<S>'

    for row in reader:
        if len(row) == 0:
            first_tag, second_tag = '<S>', '<S>'
            data['tags']['<S>']['count'] += 1
            continue

        token = row[0].lower()
        tag = row[1].upper()
        transition = f'{first_tag}-{second_tag}-{tag}'
        bi_transition = f'{second_tag}-{tag}'
        first_tag, second_tag = second_tag, tag

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
        
        if bi_transition in data["transitions"]:
            data["transitions"][bi_transition] += 1
        else:
            data["transitions"][bi_transition] = 1


with io.open(FILE_OUT, 'w', encoding="utf8") as training_data_json:
    json.dump(data, training_data_json, ensure_ascii=False)
