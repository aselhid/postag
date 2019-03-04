import json
from pomegranate import *
import io

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
