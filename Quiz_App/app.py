from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import pandas as pd
import dbHandler

app = Flask(__name__,template_folder='templates')
app.secret_key = 'your_secret_key'  # Needed for session management

questions = []

@app.route('/',methods=['GET', 'POST'])
def index():
    # Sample questions
    questions.clear()
    df = pd.read_csv('Z:\Python\Flask\My_Quize_Web_App\Quiz_App\QuestionDB\ETIchp2.csv', index_col=False)
    print(list(df.iterrows())[0][1]['Questions'])

    for i, row in df.iterrows():
        d = {'question': row['Questions'].replace('\t', ''),
             'choices': [row['op1'].replace('\t', ''), row['op2'].replace('\t', ''), row['op3'].replace('\t', ''),
                         row['op4'].replace('\t', '')], 'answer': str(row['ans']).replace('\t', '')}
        questions.append(d)

    session['current_question'] = 0
    session['score'] = 0
    session['answers'] = []
    session['uName'] = ""
    session['QuesAddName'] = ""
    session['Qtype'] = ""
    session['total_questions'] = len(questions)
    if request.method == 'POST':
        return redirect(url_for('quiz'))
    
    # else:
    #     return redirect(url_for('add_que'))
    return render_template('index.html')

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

        if selected_choice == correct_answer:
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
    
    if current_question < len(questions):
        question = questions[session['current_question']]
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

