import json
import io
import csv
import itertools

with io.open('training-data-2_smoothed.json', 'r', encoding='utf-8-sig') as raw_training_data:
    training_data = json.load(raw_training_data)

# Extract necessary datas for unigram calculation

types_count = {}
tokens_count = 0

for tag, tag_attr in training_data["tags"].items():
    if tag == '<S>':
        continue

    tokens_count += tag_attr["count"]

    for tipe, tipe_count in tag_attr["type"].items():
        if tipe in types_count:
            types_count[tipe] += tipe_count
        else:
            types_count[tipe] = tipe_count

# 1-gram prediction function

def predict(sequence, types_count, tokens_count, tags):
    prediction = []

    for token in sequence:
        if token not in types_count:
            prediction.append(None)
            continue
        
        token_probability = types_count[token] / tokens_count
        possible_tag, max_probability = None, 0

        for tag, tag_attr in tags.items():
            if tag == '<S>':
                continue
            
            tag_probability = tag_attr["count"] / tokens_count

            unigram_probability = tag_probability * token_probability
            if unigram_probability > max_probability:
                max_probability = tag_probability
                possible_tag = tag

        prediction.append(possible_tag)

    return prediction

# testing

with open('test-data.tsv', 'r') as raw_test_data:
    reader = csv.reader(raw_test_data, delimiter='\t')

    cleaned_data = [s.strip().lower() for s in list(itertools.chain(*reader))]

test_data = [list(y) + ['.'] for x, y in itertools.groupby(
    cleaned_data, lambda z: z == '.') if not x]

counter = 1
for test in test_data:
    print(f'Kalimat {counter}')
    print(' '.join(test))
    print(' '.join(predict(test, types_count, tokens_count, training_data["tags"])), '\n')

    counter += 1