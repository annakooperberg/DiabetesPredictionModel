# DiabetesPredictionModel
Project for 6.419/IDS.012

# Using ICD Codes
- Use 'dataset_diabetes/diabetic_data_cleaned.csv', which has cleaned ICD codes, to load data. (generated from 'dataset-description.Rmd'
- Use 'icd_codes.csv' to get the diagnosis in words for each code.
- To cluster at different levels, truncate the codes in 'dataset_diabetes/diabetic_data_cleaned.csv'.
  - Use 'truncate_codes' with the power of 10 at which you want to truncate. This function will write to a csv file in 'dataset_diabetes' with all diagnosis codes truncated at the appropriate level.
  - You can then match the diagnosis codes to the codes in 'icd_codes.csv' to get the diagnosis at the appropriate clustering level.
  - For example, to truncate all codes to the nearest integer, use 'truncate_codes(dataset, 0)'. To truncate codes to the first decimal place, use 'truncate_codes(dataset, -1)'.
  - Codes that do not contain enough information to cluster at that level will be retained using the most information possible. (Truncating 250 at the first decimal place will produce 250.)