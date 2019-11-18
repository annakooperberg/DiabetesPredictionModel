import csv
from icd9 import ICD9 # not python3 compatible

tree = ICD9('./codes.json')

def cluster_codes(dataset_path, level=2):
    """
    levels
    - 1 top (eg 'Endocrine, Nutritional And Metabolic Diseases, And Immunity Disorders')
    - 2 super (eg 'Diseases Of Other Endocrine Glands')
    - 3 basic (eg 'Diabetes mellitus')
    - 4 sub (eg 'Diabetes mellitus without mention of complication')
    - 5 specific (eg 'Diabetes mellitus without mention of complication, type II or unspecified type, not stated as uncontrolled')
    """
    with open(dataset_path) as data_f:
        data = csv.reader(data_f, delimiter=',')
        diagnosis_codes = {}
        results = []
        for i, line in enumerate(data):
            if i == 0:
                diag_index = line.index('diag_1')
                line.append('diag_1_desc')
                line.append('diag_2_desc')
                line.append('diag_3_desc')
                results.append(line)
                continue
            diag_1 = line[diag_index]
            diag_2 = line[diag_index+1]
            diag_3 = line[diag_index+2]
            for j,diag in enumerate([diag_1, diag_2, diag_3]):
                if diag not in diagnosis_codes and diag != '?':
                    new_diag = diag
                    node = tree.find(new_diag)
                    while node is None and new_diag:
                        new_diag = new_diag[:-1]
                        node = tree.find(new_diag)
                    if new_diag:
                        if len(node.parents) > level:
                            diagnosis_codes[diag] = node.parents[level]
                        else:
                            diagnosis_codes[diag] = node.parents[-1]
                    elif node is None:
                        diagnosis_codes[diag] = None
                if diag != '?':
                    if diagnosis_codes[diag] is not None:
                        line[diag_index+j] = diagnosis_codes[diag].code
                        line.append(diagnosis_codes[diag].description)
                    else:
                        line.append(None)
                else:
                    line.append(None)
            results.append(line)
        with open('./dataset_diabetes/diabetic_data_clustered{}.csv'.format(level), mode='w') as out_f:
            out_writer = csv.writer(out_f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for line in results:
                out_writer.writerow(line)

cluster_codes('./dataset_diabetes/diabetic_data.csv', 5)
