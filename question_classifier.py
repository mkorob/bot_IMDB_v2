# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 00:55:18 2022

@author: maria
"""

from transformers import BertTokenizer, BertForSequenceClassification
tokenizer = RobertaTokenizer.from_pretrained('mkorob/classifier_sent')

from transformers import BertTokenizer
from datasets import Dataset
train_data = Dataset.from_pandas(train_data)
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
encoded_dataset = [tokenizer(item['Questions'], return_tensors="pt", padding='max_length', truncation=True, max_length=128) for item in train_data]
import torch
for enc_item, item in zip(encoded_dataset, train_data):
    enc_item['labels'] = torch.LongTensor([item['Category']])
from transformers import BertForSequenceClassification, Trainer, TrainingArguments
model = BertForSequenceClassification.from_pretrained('bert-base-cased', num_labels=5)
training_args = TrainingArguments(
    num_train_epochs=5,
    per_device_train_batch_size=4,
    output_dir='results',
    logging_dir='logs',
    no_cuda=False,  # defaults to false anyway, just to be explicit
)
for item in encoded_dataset:
    for key in item:
        item[key] = torch.squeeze(item[key])
trainer = Trainer(
    model=model,
    tokenizer=tokenizer,
    args=training_args,
    train_dataset=encoded_dataset,
)
trainer.train()


from transformers import AutoTokenizer, AutoModelForSequenceClassification
tokenizerClass = AutoTokenizer.from_pretrained("mkorob/results")
modelClass = AutoModelForSequenceClassification.from_pretrained("mkorob/results")
text = "Show me a photo of Angelina Jolie."
encoded_input = tokenizerClass(text, return_tensors='pt')
output = modelClass(**encoded_input)



## build data
slice_movies = setup.all_films_names[0:1000]
import pandas as pd
test_questions = pd.read_excel("question_builder.xlsx", header = 1)

#movie questions
movie_questions = []
test_q_movies = test_questions['Regquestion'][test_questions['Cat_fill'] == "f"]
for movie in test_q_movies.values:
    for film in slice_movies:
        movie_questions.append(movie % film)
        

train_data = test_questions[["QuestionS", "Category"]].iloc[0:31]

from simpletransformers.classification import ClassificationModel, ClassificationArgs
# creating a model on simpletransformers
model_args = ClassificationArgs(num_train_epochs=5, manual_seed=42, train_batch_size=4, max_seq_length=128)
# Create a ClassificationModel
bert_model = ClassificationModel(
    "bert", "bert-base-cased", args=model_args, use_cuda=False
)
bert_model.train_model(train_data, output_dir='test_2')


