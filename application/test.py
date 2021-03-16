import pymysql
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import VARCHAR, TEXT 
from sqlalchemy.orm import relationship, backref
import mysql.connector
from wtforms import FormField, StringField, SelectField, FieldList, HiddenField, SelectMultipleField, widgets, IntegerField 
import calendar
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flaskwebgui import FlaskUI
from wtforms.validators import DataRequired, Length
from tables import All_Departments
#from models import Member

app = Flask(__name__)

# this userpass assumes you did not create a password for your database
# and the database username is the default, 'root'
userpass = 'mysql+pymysql://joshlufafa:fhdu23AJ8j3hmvbluf@'
basedir  = '127.0.0.1'
# change to YOUR database name, with a slash added as shown
dbname   = '/kyambogosda'
# this socket is going to be very different on a Windows computer
#socket   = '?unix_socket=/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'


# put them all together as a string that shows SQLAlchemy where the database is
app.config['SQLALCHEMY_DATABASE_URI'] = userpass + basedir + dbname

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'Agdgajj938n2!gjjskg@;[pbqbktofd'
#app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads')

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)
    
ui = FlaskUI(app)

def dow_name(dow):
    return calendar.day_name(dow)
 

#Table for joing the members to different departments
departmentals = db.Table('departmentals',
    #db.Column('id', db.Integer, primary_key=True),
    db.Column('member_id', db.Integer, db.ForeignKey('department_member.id', ondelete="cascade")),
    db.Column('department_id', db.Integer, db.ForeignKey('department.id', ondelete="cascade"))
)

class Member(db.Model):
    __tablename__ = 'department_member'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=False)
    position = db.Column(db.String(120), index=False)
    department = db.relationship('Department', secondary=departmentals, lazy='subquery', backref=db.backref('department_member', lazy=True))
    def __repr__(self):
        return '<Member {}>'.format(self.name)  

class Department(db.Model):
    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=False, nullable=False)#Name of each created department
        # member_id = db.column(db.Integer, db.ForeignKey('member.id', nullable=True))#Reference a member from the memebr model to avoid redundancy
        # position = db.Column(db.String(128), index=False, nullable=True)
    def __repr__(self):
        return '<Department {}>'.format(self.name)  

class DepartmentForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    
class AddMemberForm(FlaskForm):
    name = StringField('Name', [DataRequired()]) 
    position = SelectField('Position', choices=[('head', 'Head'), ('secretary', 'Secretary'), ('treasurer', 'Treasurer'), ('publicity', 'Publicity'), ('communications', 'Communications')])
       
class MemberForm(FlaskForm):#Form for the member to be added to the department
    name = StringField('Name', [DataRequired()])
    position = SelectField('Position', choices=[('head', 'Head'), ('secretary', 'Secretary'), ('treasurer', 'Treasurer'), ('publicity', 'Publicity'), ('communications', 'Communications')])
    
    departments = SelectMultipleField('Departments', coerce=int,  widget=widgets.ListWidget(prefix_label=True), option_widget=widgets.CheckboxInput())

    def set_choices(self):
        self.departments.choices = [(d.id, d.name) for d in Department.query.all()]

class EditForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    position = SelectField('Position', choices=[('head', 'Head'), ('secretary', 'Secretary'), ('treasurer', 'Treasurer'), ('publicity', 'Publicity'), ('communications', 'Communications')])


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
    form = MemberForm(request.form)
    form.departments.choices = [(d.id, d.name) for d in Department.query.all()]
    if request.method == 'POST':
        member = Member()
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
        member = Member()
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
    qry = db.session.query(Member).filter(Member.id==id)#When you use the contains word then strings with that word will be returned which may not be the case for male, it would also return female coz the word male is in female
    member = qry.first() 
    if member:
        form = EditForm(formdata=request.form, obj=member)
        print(form.position.data)
        if request.method == 'POST' and form.validate():
            member.name = form.name.data
            member.position = form.position.data
            db.session.add(member)
            db.session.commit()
    return render_template('departments/edit_member.html', form=form, member=member)

@app.route('/delete_member/<int:id>', methods=['GET', 'POST'])
def delete_member(id):
    qry = db.session.query(Member).filter(Member.id==id)#When you use the contains word then strings with that word will be returned which may not be the case for male, it would also return female coz the word male is in female
    member = qry.first()
    if member:#Consider providing a form for deleting the member specified
        db.session.delete(member)
        db.session.commit()
        #return a redirect to the department id where you have deleted the member
        return redirect('department') 
    else:
        return 'Error deleting #{id}'.format(id=id)    

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    qry = db.session.query(Department).filter(Department.id==id)
    department = qry.first()
    if department:
        form = DepartmentForm(formdata=request.form, obj=department)
        """ This will delete the member objects associated with the department from the members' database"""
        for member in department.department_member:#This displays the individual member objects associated with the department object
            qry = db.session.query(Member).filter(Member.id==member.id)
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

    # def delete_member(id):
    #     #Query the department_members table for the members that belong to the department being deleted
    
db.create_all()
if __name__ == '__main__':
    app.run(debug=True) 
#ui.run()          

 