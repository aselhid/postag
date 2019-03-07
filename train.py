import json
import io
import matplotlib.pyplot as plt
import itertools
import csv
from pomegranate import *

smoothed = True if input('smoothed?').lower() == 'y' else False
stemmed = True if input('stemmed?').lower() == 'y' else False

if smoothed:
    if stemmed:
        train_data_name = 'training-data-2-stemmed_smoothed.json'
    else:
        train_data_name = 'training-data-2_smoothed.json'
else:
    if stemmed:
        train_data_name = 'training-data-2-stemmed.json'
    else:
        train_data_name = 'training-data-2.json'

print("loading from",train_data_name)
data = {}
with io.open(train_data_name, 'r', encoding='utf-8-sig') as training_data:
    data = json.load(training_data)
unknowns = ['berekor', 'setibanya', 'multibudaya', 'humanis', 'wings', 'album', 'terlaris', 'gaon', 'album', 'chart', 'google', 'larry', 'page', 'sergey', 'brin', 'ph.d.', 'stanford', 'kemarau', 'katak', '407']
states = {}
for tag in data["tags"]:
    distribution = {k: 0 for k in unknowns} if not smoothed else {}

    for tipe in data["tags"][tag]["type"]:

        distribution[tipe] = data["tags"][tag]["type"][tipe] / \
            data["tags"][tag]["count"]

    states[tag] = State(DiscreteDistribution(distribution), name=tag)

model = HiddenMarkovModel('pos-tag-nlp', start=states['<S>'])
model.add_states(list(states.values()))
for transition in data['transitions']:
    tag_a, tag_b = transition.split("-")
    if tag_a == '<S>':
        state_a = model.start
    else:
        state_a = states[tag_a]
    state_b = states[tag_b]
    transition_prob = data['transitions'][transition] / \
        data['tags'][tag_a]['count']

    model.add_transition(state_a, state_b, transition_prob)

model.bake()
# model.plot()
# plt.show()

# TESTING
TEST_DATA = 'test-data-stemmed.tsv' if stemmed else 'test-data.tsv'
with open(TEST_DATA, 'r') as test_file:
    raw_test_data = csv.reader(test_file, delimiter='\t')

    cleaned_data = [s.strip().lower()
                    for s in list(itertools.chain(*raw_test_data))]

test_data = [list(y) + ['.'] for x, y in itertools.groupby(
    cleaned_data, lambda z: z == '.') if not x]

counter = 1
for test in test_data:
    print('Kalimat',counter)
    counter += 1
    try:
        print(' '.join(test))
        print('map :', ' '.join([model.states[i].name if i >= 0 else '??' for i in model.predict(test)]))
        print('viterbi :', ' '.join([model.states[i].name for i in model.predict(test, algorithm='viterbi')]))
    except:
        print('Warning : Sequence is impossible.')

    finally:
        print()
