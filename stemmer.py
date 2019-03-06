import csv
import io

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


factory = StemmerFactory()
stemmer = factory.create_stemmer()
punctuations = [".", ",","\\\"",":","(","/",")","-","?","'",";","&","--","...","!"]
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
