import csv

def cluster_codes(diagnosis, level=3):
    with open('icd_codes.csv') as data_f:
        data = csv.reader(data_f, delimiter=',')
        diagnosis_codes = {}
        for i, line in enumerate(data):
            if i == 0:
                continue
            diagnosis_codes[line[0]] = line[1]
    print(diagnosis_codes)
    super_diagnosis = diagnosis[:level]
    super_diagnosis_codes = {}

cluster_codes('h')
