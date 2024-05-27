from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import pandas as pd
from Quiz_App import dbHandler
import random

app = Flask(__name__,template_folder='templates')
app.secret_key = 'your_secret_key'  # Needed for session management

ETIChapter1 = ['ETIchp1.csv']
ETIChapter2 = ['ETIchp2.csv']
ETIChapter3 = ['ETIchp3.csv']
ETIChapter4 = ['ETIchp4.csv']
ETIChapter5 = ['ETIchp5.csv']
ETIChapter6 = ['ETIchp6.csv']
ETIAllChapters = []
questions = list()
# Sample questions
chplist = [ETIChapter1,ETIChapter2,ETIChapter3,ETIChapter4,ETIChapter5,ETIChapter6]
for ch in chplist:
    # ch2questions.clear()
    try:
        df = pd.read_csv(f'Quiz_App/QuestionDB/{ch[0]}', index_col=False)
        # print(list(df.iterrows())[0][1]['Questions'])

        for i, row in df.iterrows():
            d = {'question': row['Questions'].replace('\t', ''),
                 'choices': row['Options'].split(' | '),
                  'answer': str(row['Answer']).replace('\t', '')}
            ch.append(d)
    except Exception as e:
        print("Error reading CSV:",e)
        ch.clear()
        print(ETIChapter1)
    else:
        del ch[0]
        print(ch)

ETIAllChapters = ETIChapter1+ETIChapter2+ETIChapter3+ETIChapter4+ETIChapter5+ETIChapter6
# ...........................
@app.route('/', methods=['GET','POST'])
def index():
    session['current_question'] = 0
    session['score'] = 0
    session['answers'] = []
    session['uName'] = ""
    session['QuesAddName'] = ""
    session['Qtype'] = ""
    if request.method == 'POST':
        subject = request.form['subject']
        chapter = request.form['chapter']
        return redirect(url_for('No_of_Que',subject = subject,chapter=chapter))
    return render_template('index.html')

@app.route('/No_of_Que/<subject>/<chapter>',methods=['GET', 'POST'])
def No_of_Que(subject,chapter):


    print(subject)
    print(chapter)

    chp = ['Chapter1', 'Chapter2', 'Chapter3', 'Chapter4', 'Chapter5', 'Chapter6', 'AllChapters']
    d = {'ETIChapter1': ETIChapter1, 'ETIChapter2': ETIChapter2, 'ETIChapter3': ETIChapter3, 'ETIChapter4': ETIChapter4,
         'ETIChapter5': ETIChapter5, 'ETIChapter6': ETIChapter6,'ETIAllChapters':ETIAllChapters}
    if subject == 'MAN':
        return "<h1>Database ERROR: Management MCQ's are not updated yet!!"

    if d[subject + chapter] == []:
        return f"{chapter} Database not updated yet!!"

    if request.method == 'POST':
        num_questions = request.form.get('num_questions')
        print(num_questions)
        if subject == 'ETI':
            if chapter in chp:
                try:
                    global questions
                    questions = random.sample(d[subject + chapter],int(num_questions))
                except Exception as e:
                    print(f'{num_questions}: {e}')
                    return "Please Enter Valid Number"
                if questions == []:
                    return f"{chapter} Database not updated yet!!"
                session['total_questions'] = len(questions)
                print(questions)
                return redirect(url_for('quiz'))
        elif subject == 'MAN':
            return "<h1>Database ERROR: Management MCQ's are not updated yet!!"
    return render_template('NumOfQue.html',subject = subject,chapter=chapter)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():

    current_question = session.get('current_question', 0)
    score = session.get('score', 0)
    answer = session.get('answers',[])
    isNameEntered = 0

    if request.method == 'POST':
        selected_choice = request.form.get('choice')
        correct_answer = questions[current_question]['answer']

        if request.form.get('name')!=None:
            print(session['uName'])
            if session['uName'] == "":
                session['uName'] = request.form.get('name')
            isNameEntered = 1

        if selected_choice.strip().split(".")[0] in correct_answer.strip().replace("Ans:",""):
            session['score'] = score + 1
        
        answer.append({
            'question': questions[session['current_question']]['question'],
            'selected': selected_choice,
            'correct': correct_answer
        })
        
        session['answers'] = answer
        session['current_question'] = current_question + 1
        
        if current_question + 1 >= len(questions):
            return redirect(url_for('results'))
    print("current_question = ",current_question,len(questions))
    if current_question < len(questions):
        question = questions[session['current_question']]
        print("Questions are: ",question)
        return render_template('quiz.html',isNameEntered = isNameEntered ,question=question, current_question=current_question, total_questions=session['total_questions'])
    else:
        return redirect(url_for('results'))

@app.route('/add_que',methods=['GET', 'POST'])
def add_que():
    if request.method == 'POST':
        name = request.form.get('name')
        key = request.form.get('key')
        type1 = request.form.get('type')
        if key == "123":
            session['QuesAddName'] = name
            session['Qtype'] = type1
            return redirect(url_for('Questions'))

    return render_template('AddQues.html')

@app.route('/Questions',methods = ['GET','POST'])
def Questions():
    name = session['QuesAddName']
    type1 = session['Qtype']
    return render_template('Questions.html',name = name,Qtype = type1)

@app.route('/results')
def results():
    name = session['uName']
    score = session.get('score', 0)
    total_questions = session.get('total_questions')
    answers = session.get('answers', [])
    try:
        dbHandler.add_result(uname=name,questions=answers,score=score,total_questions=total_questions)

    except Exception as e:
        print("Data not Added...",e)
    else:
        print("Data Added Successfully!!")

    return render_template('results.html', Uname=name, score=score, total_questions=total_questions, answers=answers)

