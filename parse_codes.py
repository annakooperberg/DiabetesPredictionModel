import csv

with open('ucod.txt', 'r', encoding = "ISO-8859-1") as f:
    data = f.readlines()
    diagnosis_codes = {}
    for line in data:
        split_line = line.replace('"', '').replace(',', '').split()
        if len(split_line) > 0:
            if len(split_line) > 1:
                if split_line[1] == '|' or ':' in split_line[1]:
                    continue
            if len(split_line) > 0:
                if split_line[0][-1] == '.':
                    continue
            try:
                float(split_line[0])
                diagnosis_codes[split_line[0]] = " ".join(split_line[1:])
            except ValueError:
                continue

with open('icd_codes.csv', 'w', newline='') as csv_f:
    writer = csv.writer(csv_f, delimiter=',', quoting=csv.QUOTE_NONE)
    writer.writerow(['Code', 'Diagnosis'])
    for code in diagnosis_codes.keys():
        if '"' in diagnosis_codes[code]:
            print(diagnosis_codes[code])
        writer.writerow([code, diagnosis_codes[code]])
    writer.writerow(['V45', 'Automatic implantable cardiac defibrillator in situ'])
    writer.writerow(['996', 'Complications peculiar to certain specified procedures'])
    writer.writerow(['V57', 'Care involving other physical therapy'])
    writer.writerow(['820', 'Fracture of neck of femur'])
    writer.writerow(['998', 'Other complications of procedures not elsewhere classified'])
    writer.writerow(['997', 'Complications affecting specified body system not elsewhere classified'])
