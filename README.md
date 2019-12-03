# DiabetesPredictionModel
Project for 6.419/IDS.012

# Using ICD Codes
- Use 'util.py' to generate a new csv with clustered codes.
- Calling cluster_codes(filename, level) will replace all codes in the file with the corresponding code at the proper hierarchy. It will also append the description in words for each diagnosis to the end of each row.
- Where finding a particular hierarchical level is not possible, the existing level will be used. For example, asking for a more specific level than was provided in the original data, or if the original data contained a '?'.