library(aod)
library(dplyr)
library(ggplot2)
library(ISLR)
library(rockchalk)

TEST_FRAC = 0.15

## open dataset
data <- read.csv("~/Desktop/Classes/IDS.012/DiabetesPredictionModel/dataset_diabetes/diabetic_data.csv", header=TRUE)

## remove duplicate patient numbers
data <- data %>% distinct(patient_nbr, .keep_all = TRUE)

## make binary response variable
data$readmitted <- combineLevels(data$readmitted, levs = c("<30",">30"), newLabel = "YES")

## divide dataset
train_size = floor((1 - TEST_FRAC)*nrow(data))
set.seed(123)
train_ind = sample(seq_len(nrow(data)),size = train_size)
train =data[train_ind,]
test =data[-train_ind,]

## logistic regression
mylogit <- glm(readmitted ~ race + gender + age + admission_type_id +
                 discharge_disposition_id + admission_source_id +
                 time_in_hospital + payer_code + medical_specialty +
                 num_lab_procedures + num_procedures + num_medications +
                 number_outpatient + number_emergency + number_inpatient +
                 diag_1, data = train, family = "binomial")



