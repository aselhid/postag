import csv
import json
# Counting

data = {
    "corpus": {},
    "tags": {},
    "transition": {}
}

with open('training-data.tsv') as training_data:
    reader = csv.reader(training_data, delimiter='\t')
    last_tag = '<S>'

    for row in reader:
        if len(row) == 0:
            last_tag = '<S>'
            continue

        token = row[0].lower()
        tag = row[1].upper()
        transition = f'{last_tag}-{tag}'
        last_tag = tag

        if token in data["corpus"]:
            data["corpus"][token]["count"] += 1
        else:
            token_data = {
                "count": 1,
                "tags": {}
            }

            data["corpus"][token] = token_data

        if tag in data["corpus"][token]["tags"]:
            data["corpus"][token]["tags"][tag] += 1
        else:
            data["corpus"][token]["tags"][tag] = 1

        if tag in data["tags"]:
            data["tags"][tag] += 1
        else:
            data["tags"][tag] = 1

        if transition in data["transition"]:
            data["transition"][transition] += 1
        else:
            data["transition"][transition] = 1


with open('training-data.json', 'w') as training_data_json:
    json.dump(data, training_data_json)
