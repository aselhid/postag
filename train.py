import json
import io
import matplotlib.pyplot as plt
from pomegranate import *

data = {}
with io.open('training-data-2.json', 'r', encoding='utf-8-sig') as training_data:
    data = json.load(training_data)

states = {}
for tag in data["tags"]:
    distribution = {}

    for tipe in data["tags"][tag]["type"]:

        distribution[tipe] = data["tags"][tag]["type"][tipe] / \
            data["tags"][tag]["count"]

    states[tag] = State(DiscreteDistribution(distribution), name=tag)

model = HiddenMarkovModel('pos-tag-nlp')
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
model.plot()
plt.show()
