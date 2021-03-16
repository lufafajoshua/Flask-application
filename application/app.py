from flask import Flask, session, redirect, url_for, escape, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy 
import os
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import pymysql.cursors
from models import db, Member, Account, DepMember, Department
from datetime import datetime 
import datetime
from forms import MemberForm, SearchForm, AdminForm, ImageForm, EditForm, FamilyForm, DepartmentForm, DepartmentMemberForm, AddMemberForm, MemberEditForm 
from config2 import db2#this is the connection to use in providing functiobnality with mysql.connector
import mysql.connector #use this to create connection 
from tables import Search_Results, ALL_Data, Family_Results, All_Departments
import re

basedirectory = os.path.abspath(os.path.dirname(__file__))#basedir to use in imageloading

#import pymysql
app = Flask(__name__)#this is our application instance

app.config.from_pyfile('finalapp.cfg')

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedirectory, 'static/img') 
PHOTO_FOLDER = os.path.join('static', 'img')
app.config['UPLOAD_FOLDER'] = PHOTO_FOLDER

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

PHOTO_FOLDER = os.path.join('static', 'img')#This is where the image files are going to be uploaded

#db = SQLAlchemy(app) #initialise the database configuration with sqlalchemy

db.init_app(app)
#bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('examples/dashboard.html')

def edit_member(member, form, new=False):#This is for the edit function which doesnt take into account the image field because its ediying is handled elsewhere
    #member.image_file = picture_fn#The filename is the picture filename from the caller function new_member
    member.full_name = form.full_name.data
    member.gender = form.gender.data  
    member.date_added = form.date_added.data #Use the current datetime object to automatically add the date the member objects have been added
    member.telephone_no = form.telephone_no.data  
    member.address = form.address.data 
    member.a_o_residence = form.a_o_residence.data 
    member.d_o_birth = form.d_o_birth.data
    member.age = form.age.data 
    member.m_status = form.m_status.data   
    member.no_children = form.no_children.data 
    member.occupation = form.occupation.data 
    member.l_o_educ = form.l_o_educ.data 
    member.p_o_work = form.p_o_work.data
    member.employer = form.employer.data  
    member.nationality = form.nationality.data
    member.tribe = form.tribe.data
    member.clan = form.clan.data
    member.ch_born = form.ch_born.data 
    member.f_faith = form.f_faith.data
    member.d_o_baptism = form.d_o_baptism.data
    member.ch_of_baptism = form.ch_of_baptism.data
    member.ch_family = form.ch_family.data
    member.l_o_AY = form.l_o_AY.data 
    member.lang_spoken = form.lang_spoken.data
    member.skills = form.skills.data 
    member.inc_projects = form.inc_projects.data 
    member.hobbies = form.hobbies.data
    member.ch_programs = form.ch_programs.data
    
    if new:
        db.session.add(member)
    db.session.commit()#save the newly created member or the edited member

def save(member, form, new=False):#member args to pass data to our, form is the argument to pass the data to the member model, This includes saving the image filename in the database
    #member.image_file = picture_fn#The filename is the picture filename from the caller function new_member
    member.full_name = form.full_name.data
    member.gender = form.gender.data  
    member.date_added = form.date_added.data #Use the current datetime object to automatically add the date the member objects have been added
    member.telephone_no = form.telephone_no.data  
    member.address = form.address.data 
    member.a_o_residence = form.a_o_residence.data 
    member.d_o_birth = form.d_o_birth.data
    member.age = form.age.data 
    member.m_status = form.m_status.data   
    member.no_children = form.no_children.data 
    member.occupation = form.occupation.data 
    member.l_o_educ = form.l_o_educ.data 
    member.p_o_work = form.p_o_work.data
    member.employer = form.employer.data  
    member.nationality = form.nationality.data
    member.tribe = form.tribe.data
    member.clan = form.clan.data
    member.ch_born = form.ch_born.data 
    member.f_faith = form.f_faith.data
    member.d_o_baptism = form.d_o_baptism.data
    member.ch_of_baptism = form.ch_of_baptism.data
    member.ch_family = form.ch_family.data
    member.l_o_AY = form.l_o_AY.data 
    member.lang_spoken = form.lang_spoken.data
    member.skills = form.skills.data 
    member.inc_projects = form.inc_projects.data 
    member.hobbies = form.hobbies.data
    member.ch_programs = form.ch_programs.data
    
    if new:
        db.session.add(member)
    db.session.commit()#save the newly created member or the edited member 

    # """
    # This defines the models for the admin account
    # for both login and regestration
    # """
    # class Account(db.Model):#This is the admins model.py file
    #     __tablename__ = 'admin_account'

    #     id = db.Column(db.Integer, primary_key=True)
    #     username = db.Column(db.String(128), index=False, nullable=False)
    #     password = db.Column(db.String(128), index=False, nullable=False)  

    #     def __repr__(self):
    #         return '<Account {}>'.format(self.username)    

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    #This methid uses the form-data directly from the login.html file not from the defined wtf forms in forms.py file 
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        #account = Account()#Query the account object directly without assigning it to a variable
        #qry = db.session.query(Account).filter(id==id).filter(Account.username.contains(username)).filter(Account.password.contains(password))
        qry = db.session.query(Account).filter(id==id).filter(Account.username==username).filter(Account.password==password)
        #Query the database to see if the account exists
        existing_account = qry.first()
        if existing_account:
            session['loggedin'] = True
            session['id'] = existing_account.id
            session['username'] = existing_account.username
            msg = 'successfully logged in' 
            return redirect(url_for('index'))
        else:
            msg = 'Invalid username or password!'
            #return redirect('login') redirect back to the login page
    return render_template('login2.html', msg=msg)#Dont forgeet to change back to the original form ie login template instead of login2         

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

def save_user(account, new=False):# This view is to save the new administrative user for the system
    account.username = request.form.get('username')#Alternatively use the form data
    account.password = request.form.get('password')#Alternatively use the form data
    if new:
        db.session.add(account)
        db.session.commit()

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = AdminForm(request.form)#we are using data from the htnl template directlt and not the form
    username = request.form.get('username')#form.username.data, alternatively use the form data
    password = request.form.get('password')#form.password.data
    password1 = request.form.get('password1')#form.password1.data
    msg = ''
    if request.method == 'POST':
        account = Account()
        #Query the database and retrieve an account with similar data and if it exists, display errors
        qry = db.session.query(Account).filter(id==id).filter(Account.username==username).filter(Account.password==password)
        existing_account = qry.first()
        #print(existing_account.username)
        if existing_account:
            msg = 'Account already exists'
            # elif not re.match(r'[A-Za-z0-9]+', username):#Validate username to use only numbers and letters
            #     msg = 'User name must contain only letters and numbers'#Dont forget to check how to validate frontend fields with re.match 
        elif password != password1:#authenticate password validation
            msg = 'Passwords didnt match'    
        else:  
            save_user(account, new=True)  
            msg = 'Successfully registered' 
    
    elif request.method == 'POST':
        msg = 'Please Fill in the form'
    return render_template('register2.html', msg=msg)#Incase of form errors use the form again to register   

@app.route('/member', methods=['GET', 'POST'])
def new_member(): #this is the function to add our new member
    flash("Welcome to this site")  
    form = MemberForm() 

    if request.method == 'POST' and form.validate_on_submit():
        member = Member()#Instantiate the member model   
        #call the save function and pass the forem and member arguments 
        save(member, form, new=True)#incase you want to add the picture _fn to be saved along with the data initially
        flash("Successfully created new member")
        return redirect(url_for('all_data'))#redirect to the home page
    else:
        form = MemberForm()
        file_url = None    

    return render_template('examples/member.html', form=form) 

@app.route('/search', methods=['GET', 'POST'])
def search():
    search_form = SearchForm(request.form) #if errors, you can pass the request.form argument here (request.form)   
    if request.method == 'POST':
        return search_data(search_form)
    return render_template('examples/search.html', form=search_form)

@app.route('/results', methods=['GET', 'POST'])
def search_data(search_form):
        # form = SearchForm(request.form) #if errors, you can pass the request.form argument here (request.form)   
        # if request.method == 'POST':
    msg = ''    
    search_string = search_form.search.data#incase of erors use form.data['search] after passing the request.form argument in the form instatiation
    results = []
    if search_string:#provided options for the search query perform a search query 
        if search_form.data['select'] == 'Member':
            qry = db.session.query(Member).filter(id==id).filter(Member.full_name.contains(search_string)) 
            results = qry.all()#[item[0] for item in qry.all()]
        elif search_form.data['select'] == 'church family':
            qry = db.session.query(Member).filter(Member.ch_family.contains(search_string))
            results = qry.all()
        elif search_form.data['select'] == 'gender':
            qry = db.session.query(Member).filter(Member.gender==search_string)#When you use the contains word then strings with that word will be returned which may not be the case for male, it would also return female coz the word male is in female
            results = qry.all()  
        else:
            qry = db.session.query(Member)
            results = qry.all()
    else:
        qry = db.session.query(Member)
        results = qry.all()                 
    
    if not results:
        msg = 'Not Found'
        return msg#redirect('search')#Return to the search page after displaying the message

    else:
        table = Search_Results(results)#create a table to use in displaying the search results
        table.border = False
        #table.column = True
        return render_template('examples/results.html', table=table, msg=msg)

@app.route('/search_family', methods=['GET', 'POST'])
def search_family():
    family_form = FamilyForm(request.form) 
    if request.method == 'POST':#Perform a validation on the forms ysing the validate method
        return family(family_form)
    return render_template('examples/search_family.html', form=family_form)

def family(family_form):
    msg = ''
    search_string = family_form.data['select']
    results = []#This will handle the results from the query
    if search_string: 
        qry = db.session.query(Member).filter(Member.ch_family.contains(search_string))
        results = qry.all()
    else:
        msg = 'Cant Search For Input'#
    if not results:
        msg = 'Not Found'
        return msg
    else:
        table = Family_Results(results)
        table.border = False
        return render_template('examples/family.html', table=table, msg=msg)

@app.route('/all_data', methods=['GET', 'POST'])
def display():
    qry = db.session.query(Member)
    results = qry.all()
    #order the results according to ascending order 
    #sorted_results = sorted(results, key = lambda x: x[0])
    table = ALL_Data(results)
    #table.allow_sort = True#This will sort all the data in the table
    return render_template('examples/all_data.html', table=table)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    #check whether the item id exists in the database
    qry = db.session.query(Member).filter(Member.id==id)
    member = qry.first()

    if member:# if the record exists
        image = member.image_file#Get the image_file from the database and check whether the image has been uploaded or not 
        if image == "noavatar92":#Incase the user image is not yet uploaded 
            image_file = url_for('static', filename='img/' + member.image_file+'.png')#Manually add the extension to the image file from the database incase the user image hadnt been added already  
        else:           
            image_file = url_for('static', filename='img/' + member.image_file)#set the image file to the current filename stored in the database
        print(image_file)
        #pass the member objects stored in the database to the form for display and editing
        form = EditForm(formdata=request.form, obj=member)
        if request.method == 'POST' and form.validate(): 
            picture_fn = member.image_file#Pass the image file of the current image for the current ovject since its not edited here
            edit_member(member, form)#pass the newly edited form to the member model to be saved in the database
            flash('successfully updated the record')
            return redirect(url_for('search_family'))

        return render_template('examples/edit.html', form=form, image_file=image_file, member=member)
  
    else: 
        return 'Error loading {id}'.format(id=id)#pass the <int:id> to convert the id to int

@app.route('/edit-image/<int:id>', methods=['GET', 'POST'])
def edit_image(id):
    member = Member()#this is the member object from which the id is to be searched and then set the image_file to a new value
    form = ImageForm()#This is the member form that doesnt use a request method
    qry = db.session.query(Member).filter(Member.id==id)#Id from the invoking object
    member = qry.first()
    image = member.image_file#Get the image_file from the database and check whether the image has been uploaded or not 
    if image == "noavatar92":#Incase the user image is not yet uploaded 
        image_file = url_for('static', filename='img/' + member.image_file+'.png')#Manually add the extension to the image file from the database  
    else:           
        image_file = url_for('static', filename='img/' + member.image_file)#when a user image was initially uploaded
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
        f_name, f_ext = os.path.splitext(filename)
        picture_fn = f_name + f_ext
        picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
        member.image_file = picture_fn#Dont forget to change the image path if it workd later on
        db.session.commit()
    else:
        file_url = None
    return render_template('edit-image.html', form=form, file_url=file_url, image_file=image_file)

@app.route('/delete/<int:id>', methods=['Get', 'POST'])
def delete(id):#delete item matching the url-id for uniqueness of the operation 
    #query the database and retrieve the member id for deleting
    qry = db.session.query(Member).filter(Member.id==id)
    member = qry.first()
    if member:
        image = member.image_file#Get the image_file from the database and check whether the image has been uploaded or not 
        if image == "noavatar92":#Incase the user image is not yet uploaded 
            image_file = url_for('static', filename='img/' + member.image_file+'.png')#Manually add the extension to the image file from the database  
        else:           
            image_file = url_for('static', filename='img/' + member.image_file)
        form = EditForm(formdata=request.form, obj=member)#Use the edit form since it doesnt include the phto filefield input
        if request.method == 'POST' and form.validate():
            db.session.delete(member)
            db.session.commit()

            flash("Successfully deleted member from database")
            return redirect('/')
        return render_template('examples/delete.html', form=form, image_file=image_file, member=member)
    else:
        return 'Error deleting #{id}'.format(id=id)

@app.route('/profile/<int:id>', methods=['GET', 'POST'])#This method loads the the profile object for view in the html page
def view_profile(id):
    qry = db.session.query(Member).filter(Member.id==id)#You can invoke the member id by Member.id==id
    member = qry.first()

    if member:
        image = member.image_file#Get the image_file from the database and check whether the image has been uploaded or not 
        if image == "noavatar92":#Incase the user image is not yet uploaded 
            image_file = url_for('static', filename='img/' + member.image_file+'.png')#Manually add the extension to the image file from the database  
        else:           
            image_file = url_for('static', filename='img/' + member.image_file)
        form = EditForm(formdata=None, obj=member)#incase of errors, return to using request.form in the formdata instance
    return render_template('examples/profile.html', form=form, image_file=image_file, member=member)    
    
@app.route('/summary')
def summary(): #creat a summary of the entire records in the database, eg tota l number of females, males 
    results = []       
    sql_query = ("SELECT *, COUNT(*) FROM members_data")#select all the data
    db2.dbcursor.execute(sql_query)
    results = db2.dbcursor.fetchall()
    for i in results:
        row1 = i[0]
        total_membership = i[30]#get the rows with which the summary of the data is to created
        #print("Total membership: ", row28) #this is the total number of
    sql_query1 = "SELECT gender, COUNT(gender) FROM members_data WHERE gender='female'"
    db2.dbcursor.execute(sql_query1)
    results = db2.dbcursor.fetchall()
    for i in results:
        row0 = i[0]
        female = i[1]#this constitutes the total number of females in the database
        #print(row0, row1)
    sql_query2 = "SELECT gender, COUNT(gender) FROM members_data WHERE gender='male'"
    db2.dbcursor.execute(sql_query2)
    results = db2.dbcursor.fetchall()
    for i in results:
        row0 = i[0]
        male = i[1]#this constitutes the total number of males in the database
        #print(row0, row1)
    sql_query3 = "SELECT m_status, COUNT(m_status) FROM members_data WHERE m_status='single'"
    db2.dbcursor.execute(sql_query3)
    results = db2.dbcursor.fetchall()
    for i in results:
        row0 = i[0]
        single = i[1]#this constitutes the total number of singles in the database
        #print(row0, row1)
    sql_query4 = "SELECT m_status, COUNT(m_status) FROM members_data WHERE m_status='married'"
    #sql_query5 = "SELECT gender,COUNT(gender) FROM member_data WHERE gender='female'" #just in case of another summary to make
    db2.dbcursor.execute(sql_query4)
    results = db2.dbcursor.fetchall()
    for i in results:
        row0 = i[0]
        married = i[1]#this constitutes the total number of married couples in the database
        #print(row0, row1)

    results = {'total_membership': total_membership, 'female': female, 'male': male, 'single': single, 'married': married}    

    return render_template('examples/summary.html', results=results)#pass the result object as a context to the summary.html page    

@app.route('/create_department', methods=['GET', 'POST'])
def create_department():
    #pass the model where the data is to be sent for saving ie department model
    #Pass the form data from the frontend
    form = DepartmentForm(request.form)
    if request.method == 'POST':
        department = Department()
        department.name = form.name.data
        db.session.add(department)
        db.session.commit()
    return render_template('departments/create_department.html', form=form)

@app.route('/add_member', methods=['GET', 'POST'])
def create_member():
    form = DepartmentMemberForm(request.form)
    form.departments.choices = [(d.id, d.name) for d in Department.query.all()]
    if request.method == 'POST':
        member = DepMember()
        member.name = form.name.data
        member.position = form.position.data
        member.departments = form.departments.data
        print(member.departments)
        db.session.add(member)
        db.session.commit()
        selected_department = Department.query.get(form.departments.data)
        member.department.append(selected_department)#Either way the association table will add the related fields to the database
        #selected_department.department_member.append(member)
        db.session.commit()
    return render_template('department/add_member.html', form=form)

@app.route('/all_departments', methods=['GET', 'POST'])
def all_departments():
    qry = db.session.query(Department)
    results = qry.all()
    table = All_Departments(results)
    return render_template('departments/all_departments.html', table=table)

@app.route('/department/<int:id>', methods=['GET', 'POST'])
def department(id):#Get the department by id and the add members to it
    department = Department()
    qry = db.session.query(Department).filter(Department.id==id)
    department = qry.first()#Handle exception for missing id in the databse
    return render_template('departments/department.html', department=department)#Display the department and the various members and ther positions

@app.route('/addmembers/<int:department_id>', methods=['GET', 'POST'])
def addmembers(department_id):#Pass the department id for the department adding members
    #Get the department by its id 
    qry = db.session.query(Department).filter(Department.id==department_id)
    department = qry.first()
    form = AddMemberForm(request.form)
    if form.validate():
        member = DepMember()
        member.name = form.name.data
        member.position = form.position.data
        db.session.add(member)
        db.session.commit()
        selected_department = department
        selected_department.department_member.append(member)
        db.session.commit()
    return render_template('departments/addmembers.html', form=form, department=department)    

@app.route('/view-departmental', methods=['GET', 'POST'])
def view():
    qry = db.session.query(Department).filter(Department.name=="personal ministries")#When you use the contains word then strings with that word will be returned which may not be the case for male, it would also return female coz the word male is in female
    department = qry.all() 
    #departmentals = department.department_members
    if department:
        form = DepartmentForm(formdata=None, obj=department)

    return render_template('department/view-departmental.html', form=form, department=department)

@app.route('/edit_department/<int:id>', methods=['GET', 'POST'])
def edit_department(id): 
    qry = db.session.query(Department).filter(Department.id==id)#When you use the contains word then strings with that word will be returned which may not be the case for male, it would also return female coz the word male is in female
    department = qry.first() 
    if department:
        form = DepartmentForm(formdata=request.form, obj=department)#You can also pass None to the formdata parameter
        if request.method == 'POST' and form.validate():
            department.name = form.name.data
            db.session.add(department)
            db.session.commit()
    return render_template('departments/edit_department.html',department=department, form=form)

@app.route('/edit_member/<int:id>', methods=['GET', 'POST'])
def edit_member(id):
    qry = db.session.query(DepMember).filter(DepMember.id==id)#When you use the contains word then strings with that word will be returned which may not be the case for male, it would also return female coz the word male is in female
    member = qry.first() 
    if member:
        form = MemberEditForm(formdata=request.form, obj=member)
        print(form.position.data)
        if request.method == 'POST' and form.validate():
            member.name = form.name.data
            member.position = form.position.data
            db.session.add(member)
            db.session.commit()
    return render_template('departments/edit_member.html', form=form, member=member)

@app.route('/delete_member/<int:id>', methods=['GET', 'POST'])
def delete_member(id):
    qry = db.session.query(DepMember).filter(DepMember.id==id)#When you use the contains word then strings with that word will be returned which may not be the case for male, it would also return female coz the word male is in female
    member = qry.first()
    if member:#Consider providing a form for deleting the member specified
        db.session.delete(member)
        db.session.commit()
        #return a redirect to the department id where you have deleted the member
        return redirect('department') 
    else:
        return 'Error deleting #{id}'.format(id=id)    

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_department(id):
    qry = db.session.query(Department).filter(Department.id==id)
    department = qry.first()
    if department:
        form = DepartmentForm(formdata=request.form, obj=department)
        """ This will delete the member objects associated with the department from the members' database"""
        for member in department.department_member:#This displays the individual member objects associated with the department object
            qry = db.session.query(DepMember).filter(DepMember.id==member.id)
            member = qry.first()
            db.session.delete(member)
            db.session.commit()
        if request.method == 'POST' and form.validate():
            db.session.delete(department)
            db.session.commit()
            #pass a redirect after deleting the department object
        return render_template('departments/delete.html', form=form, department=department)
    else:
        return 'Error deleting #{id}'.format(id=id)    

with app.app_context():
    db.create_all() # change the storage engine to InnoDB  
if __name__ == '__main__':
    app.run(debug=True)
 
 
