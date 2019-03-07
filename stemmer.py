import csv
import io

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


factory = StemmerFactory()
stemmer = factory.create_stemmer()
punctuations = [".", ",","\\\"",":","(","/",")","-","?","'",";","&","--","...","!"]
stem = False
if stem:
    with open('training-data.tsv') as training_data:
        reader = csv.reader(training_data, delimiter="\t")
        with open('training-data-stemmed.tsv', 'wt', newline='') as stemmed_training_data:
            writer = csv.writer(stemmed_training_data, delimiter="\t")
            for row in reader:
                if len(row) == 0:
                    writer.writerow([''])
                else:
                    stemmed_word = row[0] if row[0] in punctuations else stemmer.stem(
                        row[0])
                    writer.writerow([stemmed_word, row[1]])
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