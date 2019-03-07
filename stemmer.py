import csv
import io

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


factory = StemmerFactory()
stemmer = factory.create_stemmer()
punctuations = [".", ",","\\\"",":","(","/",")","-","?","'",";","&","--","...","!"]
train_flag = True if input('stem training data?').lower() == 'y' else False
stem = True

FILE_IN = 'training-data.tsv' if train_flag else 'test-data.tsv'
FILE_OUT = 'training-data-stemmed.tsv' if train_flag else 'test-data-stemmed.tsv'

print(FILE_IN, FILE_OUT, train_flag)
if stem:
    with open(FILE_IN) as training_data:
        reader = csv.reader(training_data, delimiter="\t")
        with open(FILE_OUT, 'wt', newline='') as stemmed_training_data:
            writer = csv.writer(stemmed_training_data, delimiter="\t")
            for row in reader:
                if len(row) == 0:
                    writer.writerow([''])
                else:
                    stemmed_word = row[0] if row[0] in punctuations else stemmer.stem(
                        row[0])
                    if train_flag:
                        writer.writerow([stemmed_word, row[1]])
                    else:
                        writer.writerow([stemmed_word])
else:
    with open('test-data_manual_tag.tsv') as manual_tag:
        reader = csv.reader(manual_tag, delimiter='\t')
        sentence = ""
        tags = ""
        counter = 1
        for row in reader:
            if len(row) == 0:
                print("Kalimat",counter)
                print(sentence)
                print("Manual tagging:",tags)
                print('')
                sentence = ""
                tags = ""
                counter += 1
            else:
                sentence += row[0] + " "
                tags += row[1] + " "
        print("Kalimat",counter)
        print(sentence)
        print("Manual tagging:",tags)
        print('')