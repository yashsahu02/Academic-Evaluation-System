from flask import Flask,render_template,request,redirect,session
import mysql.connector
import os

app=Flask(__name__)
app.secret_key=os.urandom(24)

conn=mysql.connector.connect(host="localhost",user="root",password="yash",database="academic_evaluation")
cursor=conn.cursor()


@app.route("/")
def login():
    return render_template('login.html')

@app.route('/add_user')
def add_user():
    return render_template('addUser.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    userid=request.form.get('userid')
    userid=userid.replace(" ","")
    
    password=request.form.get('password')
    
    cursor.execute("""SELECT * FROM `login` WHERE `USERID` LIKE '{}' AND `PASSWORD` LIKE '{}'""".format(userid,password))
    
    #### Here I will try to apply try and except ---------->
    
    user_detail=cursor.fetchall()
    print(user_detail)
    if(len(user_detail)>0):
        
        # cursor.execute("""SELECT * FROM `login` WHERE EXISTS (SELECT `userid` FROM `login` WHERE `userid` LIKE '{}' AND `password` LIKE '{}')""".format(userid,password))
        
        # check_password = cursor.fetchall()
        
        if(password==user_detail[0][1]):
            category=user_detail[0][2]
            ## activating session when the user has logged in
            session['user_id']=user_detail[0][0]    ## session setting
            if category=="S": 
                ## if category is "S" go to studentHome.html
                return render_template("studentHome.html")
            else:
                ## otherwise category will be "F" so go to facultyHome.html
                return render_template("facultyHome.html")
            
        else:
            return "Wrong Password........."
            
    else:
        return "Invalid UserID or Password...."
       
    # return "UserID: {} and Password: {}".format(userid,password)

@app.route('/register',methods=['POST'])
def register():
    code=request.form.get('code')
    userid=request.form.get('userid')
    userid=userid.replace(" ","")
    password=request.form.get('password')
    category=request.form.get('category')
    
    if code=="9460":
        
        cursor.execute("""SELECT `userid` FROM `login` WHERE EXISTS (SELECT `userid` FROM `login` WHERE `userid` LIKE '{}')""".format(userid))
        
        userid_details=cursor.fetchall()
        
        try:
            if(len(userid_details)==0):
                cursor.execute("""INSERT INTO `login`(`userid`,`password`,`category`) VALUES('{}','{}','{}')""".format(userid,password,category))
                conn.commit()
                return "User Added Successfully...."
            
            else:
                return "User Exist for this userid......."
                
        
        except IndexError:
            return "Return from except........"
        
        # cursor.execute("""SELECT * FROM `login` WHERE `userid` LIKE '{}'""".format(userid))
        # myuser=cursor.fetchall()
        # session['user_id']=myuser[0][0]
        # return redirect('/home')
        
        
    else:
        return "Wrong Code!.. Please Enter the valid code...."
    
    
    

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

## we will add this logout in our home page
        
    
    


if __name__=="__main__":
    app.run(debug=True)