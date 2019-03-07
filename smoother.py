import json
import io

stem = True if input('stemmed?').lower() == 'y' else False
FILE_IN = 'training-data-2-stemmed.json' if stem else 'training-data-2.json'
FILE_OUT = 'training-data-2-stemmed_smoothed.json' if stem else 'training-data-2_smoothed.json'
with io.open('training-data.json', 'r', encoding='utf-8-sig') as raw_training_data:
    json_training = json.load(raw_training_data)
    types = json_training['corpus']

with io.open(FILE_IN, 'r', encoding='utf-8-sig') as raw_training_data:
    training_data = json.load(raw_training_data)

unknowns = ['berekor', 'setibanya', 'multibudaya', 'humanis', 'wings', 'album', 'terlaris', 'gaon', 'album', 'chart', 'google', 'larry', 'page', 'sergey', 'brin', 'ph.d.', 'stanford', 'kemarau', 'katak', '407']
if stem:
    unknowns.remove('terlaris')
    unknowns.append('laris')
    unknowns.remove('ph.d.')
    unknowns.append('ph d')
unknowns_dict = {k: 0 for k in unknowns}

for tag, attr in training_data["tags"].items():
    if tag == "<S>":
        continue
    
    attr["type"].update(unknowns_dict)
    for v in types:
        if v in attr['type']:
            continue
        else:
            attr['type'][v] = 0
    attr["count"] += len(attr["type"])
    for t in attr["type"]:
        attr["type"][t] += 1
    
            

with io.open(FILE_OUT, 'w', encoding='utf-8-sig') as raw_training_data:
    json.dump(training_data, raw_training_data, ensure_ascii=False)