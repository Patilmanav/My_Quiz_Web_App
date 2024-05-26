import  pymysql
import Quiz_App.aws_credentials as rds
conn = pymysql.connect(
    host= rds.host,
    port=rds.port,
    user=rds.user,
    password=rds.password,
    db=rds.db,
)

def add_result(uname,questions,score,total_questions):
    uname = str(uname).replace(' ','')
    cursor = conn.cursor()

    cursor.execute(f'DROP TABLE IF EXISTS {uname}')
    create_table1 = f'''
        CREATE TABLE {uname}(
            question VARCHAR(200),
            selected VARCHAR(200),
            correct VARCHAR(200)
        );
    '''
    cursor.execute(create_table1)

    for que in questions:
        cursor.execute(f'''
            INSERT INTO user_info.{uname} (question, selected, correct)
            VALUES('{que['question']}', '{que['selected']}', '{que['correct']}');
        ''')
        conn.commit()

    cursor.execute(f'INSERT INTO user_info.AllUserScore(name,score,total_questions,timestamp1) VALUES("{uname}", {score}, {total_questions},CURRENT_TIMESTAMP);')
    conn.commit()
    # create_table2 = f'''
    #     CREATE TABLE AllUserScore(
    #         id INT AUTO_INCREMENT PRIMARY KEY,
    #         name VARCHAR(255),
    #         score INT,
    #         total_questions INT,
    #         timestamp TIMESTAMP
    #     );
    # '''
    # cursor.execute(create_table2)