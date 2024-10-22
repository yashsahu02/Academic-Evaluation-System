from flask import Flask,render_template,request
import mysql.connector

app=Flask(__name__)

conn=mysql.connector.connect(host="localhost",user="root",password="yash",database="academic_evaluation")
cursor=conn.cursor()


@app.route("/")
def home():
    return render_template('login.html')

@app.route('/add_user')
def add_user():
    return render_template('addUser.html')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    userid=request.form.get('userid')
    password=request.form.get('password')
    
    cursor.execute("""SELECT * FROM `login` WHERE `USERID` LIKE '{}' AND `PASSWORD` LIKE '{}'""".format(userid,password))
    
    user_detail=cursor.fetchall()
    print(user_detail)
    if len(user_detail)>0:
        return render_template('home.html')
    else:
        return render_template('login.html')
    
        
    # return "UserID: {} and Password: {}".format(userid,password)
    return "Hello"

@app.route('/register',methods=['POST'])
def register():
    code=request.form.get('code')
    userid=request.form.get('userid')
    password=request.form.get('password')
    category=request.form.get('category')
    
    if code=="9460":
        cursor.execute("""INSERT INTO `login`(`userid`,`password`,`category`) VALUES('{}','{}','{}')""".format(userid,password,category))
        conn.commit()
        return "User Added Successfully...."
    else:
        return "Wrong Code!.. Please Enter the valid code...."
    
    


if __name__=="__main__":
    app.run(debug=True)