import csv

with open('ucod.txt', 'r', encoding = "ISO-8859-1") as f:
    data = f.readlines()
    diagnosis_codes = {}
    for line in data:
        split_line = line.replace('"', '').split()
        if len(split_line) > 0:
            if len(split_line[0]) == 3 and split_line[0].isnumeric():
                diagnosis_codes[split_line[0]] = " ".join(split_line[1:])

with open('icd_codes.csv', 'w', newline='') as csv_f:
    writer = csv.writer(csv_f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Code', 'Diagnosis'])
    for code in diagnosis_codes.keys():
        writer.writerow([code, diagnosis_codes[code]])
