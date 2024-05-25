import pandas as pd

# Sample questions
# questions = [
#     {'question': 'What is the capital of France?', 'choices': ['Paris', 'London', 'Berlin', 'Madrid'], 'answer': 'Paris'},
#     {'question': 'What is 2 + 2?', 'choices': ['3', '4', '5', '6'], 'answer': '4'},
#     {'question': 'What is the color of the sky?', 'choices': ['Blue', 'Green', 'Red', 'Yellow'], 'answer': 'Blue'}
# ]

q = []

df = pd.read_csv('My_Quize_Web_App//QuestionDB//ETIchp2.csv',index_col=False)
print(list(df.iterrows())[0][1]['Questions'])

for i, row in df.iterrows():
    d = {'question':row['Questions'].replace('\t',''), 'choices':[row['op1'].replace('\t',''),row['op2'].replace('\t','') ,row['op3'].replace('\t','') ,row['op4'].replace('\t','') ],'answer':str(row['ans']).replace('\t','')}
    q.append(d)

print(q)
    