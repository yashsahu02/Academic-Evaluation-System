from flask import Flask,render_template,render_template_string,request,redirect,session,url_for
import mysql.connector
import os

app=Flask(__name__)
app.secret_key=os.urandom(24)

conn=mysql.connector.connect(host="localhost",user="root",password="yash",database="academic_evaluation_db", auth_plugin='mysql_native_password')
cursor=conn.cursor()

## mysql_native_password, which is no longer the default. Assuming we're using the correct connector for your version we need to specify the auth_plugin argument when instantiating our connection object


@app.route("/")
def login():
    return render_template('login.html')

@app.route('/admin_login')
def add_user():
    return render_template('adminLogin.html')

@app.route('/admin_dashboard')
def go_to_admin_dashboard():
    return render_template('adminDashboard.html')

@app.route('/admin_teachers')
def go_to_admin_teachers():
    return render_template('adminTeachers.html')

@app.route('/admin_students')
def go_to_admin_students():
    return render_template('adminStudents.html')

@app.route('/admin_evaluation')
def go_to_admin_evaluaiton():
    return render_template('adminEvaluation.html')

@app.route('/admin_profile')
def go_to_admin_profile():
    return render_template('adminProfile.html')

# @app.route('/admin_dashboard')
# def go_to_admin_dashboard():
#     return render_template('adminDashboard.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')
    
@app.route('/admin_login_validation',methods=['POST'])
def admin_login_validation():
    code=request.form.get('code')
    
    if code=="9460":
        return render_template("adminDashboard.html")
    else:
        return render_template('message.html',message="Wrong Code! Enter the valid code... Press Back and Try again." )


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
        return render_template('message.html',message="Invalid UserID or Password....<a href='/'>Try Again!</a>")
       
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
                return render_template('message.html',message="User Added Successfully... Press Back to Return!")
            
            else:
                return render_template('message.html',message="User Exist for this UserID..... Press Back and use other UsedID!")
                
        
        except IndexError:
            return "Return from except........"
        
        # cursor.execute("""SELECT * FROM `login` WHERE `userid` LIKE '{}'""".format(userid))
        # myuser=cursor.fetchall()
        # session['user_id']=myuser[0][0]
        # return redirect('/home')   
    else:
        return render_template('message.html',message="Wrong Code!.. Please press Back and Enter the valid code....")
    
    
@app.route('/logout',methods=['POST'])
def logout():
    # session.pop('code')
    return redirect('/')
    # return render_template("login.html")

## we will add this logout in our home page
    
################ Actions Admin Can Perform after Login #########################    
  
### Action to perform when admin search for any teacher
@app.route('/search_teacher',methods=['POST'])
def search_teacher():
    userid=request.form.get('userid') 
     
    userid=userid.replace(' ','')
    
    cursor.execute("""SELECT * FROM `login` WHERE `USERID` LIKE '{}'""".format(userid))
    user_detail=cursor.fetchall()
    if len(user_detail)==0:
        # return "No any Teacher exist for this userid....."
        return render_template('adminTeachers.html',noUser_visibility="visible",noUser_display="block",initialImage_visibility="hidden",initialImage_display="none",userid=userid)
        
    category=user_detail[0][2]
    if category=="S":
        # return "No any Teacher exist for this userid....."
        return render_template('adminTeachers.html',noTeacher_visibility="visible",noTeacher_display="block",initialImage_visibility="hidden",initialImage_display="none",userid=userid)
    
    else:
        cursor.execute("""SELECT login.userid,login.password,teacher.full_name,teacher.email,teacher.phone,department.department_name,teacher.gender,teacher.address FROM `login` INNER JOIN `teacher` ON login.userid=teacher.teacher_id INNER JOIN department ON teacher.department_id = department.department_id WHERE login.userid='{}';""".format(userid))
        result=cursor.fetchall()
        return render_template('message.html',message=result)
        # return render_template('adminTeachers.html',showTeacherDetail_visibility="visible",showTeacherDetail_display="block",initialImage_visibility="hidden",initialImage_display="none",Result=result)


##### form to show when admin clicks for update teacher details 
@app.route('/show_update_teacher_details_form')
def show_update_teacher_details_form():
    return render_template('updateTeacherDetails.html')


##### actions to perform when admin clicks for update teacher details (submit admin details update form)
@app.route('/update_teacher_details',methods=['POST'])
def update_teacher_details():
    userid=request.form.get('userid')  
    userid=userid.replace(' ','')
    password=request.form.get('password')
    ## Here we need to specify the category 
    category="F"
    full_name=request.form.get('full_name')
    email=request.form.get('email')
    phone=request.form.get('phone')
    department_id=request.form.get('department')
    designation=request.form.get('designation')
    salary=request.form.get('salary')
    gender=request.form.get('gender')
    address=request.form.get('address')
    
     
    cursor.execute("""SELECT * FROM `login` WHERE `USERID` LIKE '{}'""".format(userid))
    user_login_detail=cursor.fetchall()
    
    if(len(user_login_detail)>0): ## it means user exist 
        category=user_login_detail[0][2]
        if(category=="F"): ## if category is "F"
            try:
                # Update details
                cursor.execute("""UPDATE `teacher` SET `full_name` = %s, `email`= %s, `phone` = %s, `department_id` = %s, `designation` = %s, `salary` = %s, `gender` = %s `address` = %s WHERE userid = %s""",(full_name,email,phone,department_id,designation,salary,gender,address,userid))
                # Update password
                cursor.execute("""UPDATE `login` SET password = %s WHERE userid = %s""",(password,userid))
                conn.commit()
                return render_template('message.html',message="Details updated successfully. Press Back to Return!")
                
            except Exception as e:
                conn.rollback()
                return render_template('message.html',message=f"An error occurred: {str(e)}")    
        else:
            return render_template('message.html',message="This is userid of a student. Please press Back to return!")    
                             
    else:
        return render_template('message.html',message="No user exist for this userid '{}'. Please press Back to return!".format(userid))
            
### form to show when admin clicks for add teacher    
@app.route('/show_add_teacher_form')
def show_add_teacher_form():
    return render_template('addNewTeacher.html')

### actions to perform when admin fills the add teacher form and submit it
@app.route('/add_new_teacher',methods=['POST'])
def add_new_teacher():
    userid=request.form.get('userid')  
    userid=userid.replace(' ','')
    password=request.form.get('password')
    ## Here we need to specify the category 
    category="F"
    full_name=request.form.get('full_name')
    email=request.form.get('email')
    phone=request.form.get('phone')
    department_id=request.form.get('department')
    designation=request.form.get('designation')
    salary=request.form.get('salary')
    gender=request.form.get('gender')
    address=request.form.get('address')
    
     
    cursor.execute("""SELECT * FROM `login` WHERE `USERID` LIKE '{}'""".format(userid))
    user_login_detail=cursor.fetchall()
    
    if(len(user_login_detail)>0): 
        return render_template('message.html',message="A teacher is already registered with this User ID. Please press Back to return and try again.")                        
    else:
        # insert values in "login" table for new teacher
        cursor.execute("""INSERT INTO `login`(`userid`,`password`,`category`) VALUES('{}','{}','{}')""".format(userid,password,category))
        conn.commit()
        
        # add details for teacher in "facultyinfo" table 
        cursor.execute("""INSERT INTO `teacher`(`teacher_id`,`full_name`,`email`,`phone`,`department_id`,`designation`,`salary`,`gender`,`address`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(userid,full_name,email,phone,department_id,designation,salary,gender,address))
        conn.commit()
        return render_template('message.html',message="New Teacher Added Successfully! Please press Back and move to previous tab....")
        

####### Admin Actions with respect to Student ----->

### Action to perform when admin search for any student
@app.route('/search_student',methods=['POST'])
def search_student():
    userid=request.form.get('userid') 
     
    userid=userid.replace(' ','')
    
    cursor.execute("""SELECT * FROM `login` WHERE `USERID` LIKE '{}'""".format(userid))
    user_detail=cursor.fetchall()
    if len(user_detail)==0:
        # return "No any Teacher exist for this userid....."
        return render_template('adminStudents.html',noUser_visibility="visible",noUser_display="block",initialImage_visibility="hidden",initialImage_display="none",userid=userid)
        
    category=user_detail[0][2]
    if category=="F":
        # return "No any Student exist for this userid....."
        
        return render_template('adminStudents.html',noStudent_visibility="visible",noStudent_display="block",initialImage_visibility="hidden",initialImage_display="none",userid=userid)
    
    else:
        cursor.execute("""SELECT login.userid,login.password,student.full_name,student.email,student.phone,student.department_id,student.course_name,student.course_branch,student.gender,student.address FROM `login` INNER JOIN `student` ON login.userid=student.student_id and login.userid='{}';""".format(userid))
        ## These are total 11 values
        result=cursor.fetchall()
        return render_template('adminStudents.html',showStudentDetail_visibility="visible",showStudentDetail_display="block",initialImage_visibility="hidden",initialImage_display="none",Result=result)
     

     
     
### form to show when admin clicks for add student    
@app.route('/show_add_student_form')
def show_add_student_form():
    return render_template('addNewStudent.html')


### actions to perform when admin fills the add student form and submit it
@app.route('/add_new_student',methods=['POST'])
def add_new_student():
    userid=request.form.get('userid')  
    userid=userid.replace(' ','') ## remove whitespaces (extra spaces)
    password=request.form.get('password')
    ## Here we need to specify the category 
    category="S"
    full_name=request.form.get('full_name')
    dob=request.form.get('dob')
    
    gender=request.form.get('gender')
    email=request.form.get('email')
    phone=request.form.get('phone')
    admission_year=request.form.get('admission_year')
    department_id=request.form.get('department')
    course_name=request.form.get('course')
    course_branch=request.form.get('course_branch')
    address=request.form.get('address')
    
     
    cursor.execute("""SELECT * FROM `login` WHERE `USERID` LIKE '{}'""".format(userid))
    user_login_detail=cursor.fetchall()
    
    # if user already exist 
    if(len(user_login_detail)>0):
        return render_template('message.html',message="User (Student) already exist for this userid. Press Back to go back...")
                              
    else:
        # insert values in "login" table for new Student
        cursor.execute("""INSERT INTO `login`(`userid`,`password`,`category`) VALUES('{}','{}','{}')""".format(userid,password,category))
        conn.commit()
        
        # add details for student in "student" table 
        cursor.execute("""INSERT INTO `student`(`student_id`,`full_name`,`dob`,`gender`,`email`,`phone`,`address`,`admission_year`,`department_id`,`course_name`,`course_branch`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(userid,full_name,dob,gender,email,phone,address,admission_year,department_id,course_name,course_branch))
        conn.commit()
        return render_template('message.html',message="New Student Added Successfully! You can press Back and move to previous tab....")
        


if __name__=="__main__":
    app.run(debug=True)