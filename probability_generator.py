import csv
import json
import io
import operator


INPUT_FILE = 'training-data-2_smoothed.json'
write = False
with io.open(INPUT_FILE, 'r', encoding='utf-8-sig') as training_data:
    data = json.load(training_data)

types = {}
for tag in data["tags"]:
    if write:
        if tag.lower() == '<s>':
            continue
        output_name = 'smoothed_'+tag+'.tsv'
        with open(output_name,'wt', newline='') as output_file:
            writer = csv.writer(output_file, delimiter="\t")
            for tipe in data["tags"][tag]["type"]:
                proabability = data["tags"][tag]["type"][tipe] / \
                    data["tags"][tag]["count"]
                tipe = str(tipe.encode('utf-8'))
                tipe = tipe[2:-1]
                writer.writerow([tipe,proabability])
    else:
        distribution = {}
        for tipe in data["tags"][tag]["type"]:
            proabability = data["tags"][tag]["type"][tipe] / \
                data["tags"][tag]["count"]
            tipe = str(tipe.encode('utf-8'))
            tipe = tipe[2:-1]
            distribution[tipe] = proabability
        types[tag] = distribution
        transition_probability = {}
        for transition in data['transitions']:
            tag_a, tag_b = transition.split("-")
            transition_prob = data['transitions'][transition] / \
                data['tags'][tag_a]['count']
            try:
                transition_probability[tag_a].update({tag_b:transition_prob})
            except:
                transition_probability[tag_a] = {tag_b:transition_prob}
        
sentence = 'Jumlah katak asli Indonesia yang tercatat saat ini ada 407 spesies .'
emission = {}
total_prob = {}
for tag in types:
    if tag.lower() == '<s>':
        continue
    emission[tag] = types[tag]['jumlah']

prev_state = '<S>'
print(len(transition_probability[prev_state]))
for state in transition_probability[prev_state]:
    state_probabilty = transition_probability[prev_state][state] * emission[state]
    total_prob[prev_state+"-"+state] = state_probabilty
    print(prev_state+"-"+state, state_probabilty)
print(max(emission.items(), key=operator.itemgetter(1))[0])


for transition, probs in total_prob:
    