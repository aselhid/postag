import json
import io
import csv
import itertools

with io.open('training-data-3_smoothed.json', 'r', encoding='utf-8-sig') as raw_training_data:
    training_data = json.load(raw_training_data)

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


def predict(sequence, training_data):
    prediction = []

    first_tag, second_tag = '<S>', '<S>'        
    for token in sequence:
        if token not in types_count:
            return ['??' for _ in range(len(sequence))]
        
        possible_tag, max_probability = None, 0
        for tag in training_data["tags"].keys():
            if tag == '<S>':
                continue

            trigram = f'{first_tag}-{second_tag}-{tag}'
            bigram = f'{second_tag}-{tag}'

            if trigram not in training_data["transitions"]:
                tri_transition = 0
            else:
                tri_transition = training_data["transitions"][trigram]

            if bigram not in training_data["transitions"]:
                bi_transition = 0
            else:
                bi_transition = training_data["transitions"][bigram]

            d = .1

            transition_probability = (tri_transition + d) / (bi_transition + (len(training_data["tags"]) - 1) * d)
            emission_probability = training_data["tags"][tag]["type"][token] / training_data["tags"][tag]["count"]

            prob = transition_probability * emission_probability

            if prob > max_probability:
                max_probability = prob
                possible_tag = tag

        first_tag, second_tag = second_tag, possible_tag
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
    print(' '.join(predict(test, training_data)), '\n')

    counter += 1
