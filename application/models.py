from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  #initialise the database configuration with sqlalchemy 

class Member(db.Model):
    __tablename__ = 'members_data'

    id = db.Column(db.Integer, primary_key=True)#you can also specify the user string to refer to the id
    image_file = db.Column(db.String(120), index=False, nullable=True, default="noavatar92")
    full_name = db.Column(db.String(128), unique=False, nullable=False)
    gender = db.Column(db.String(128), unique=False, nullable=False) 
    date_added = db.Column(db.DateTime, index=False, nullable=False)
    telephone_no = db.Column(db.String(100), unique=False, index=False, nullable=True) 
    address = db.Column(db.Text, index=False, nullable=True) 
    a_o_residence = db.Column(db.Text, index=False, nullable=True) 
    d_o_birth = db.Column(db.DateTime, index=True, nullable=False)#this stores the date of birth
    age = db.Column(db.Integer, index=True, nullable=False) 
    m_status = db.Column(db.String(128), index=True, nullable=False) 
    no_children = db.Column(db.Integer, index=False, nullable=True) #number of children
    occupation = db.Column(db.String(128), index=True, nullable=True) 
    l_o_educ = db.Column(db.String(128), index=False, nullable=False)#level of education
    p_o_work = db.Column(db.Text, index=False, nullable=True)#place of work
    employer = db.Column(db.String(120), index=False, nullable=True)  
    nationality = db.Column(db.String(120), index=True, nullable=False)
    tribe = db.Column(db.Text, index=False, nullable=False)
    clan = db.Column(db.Text, index=False, nullable=True)
    ch_born = db.Column(db.String(120), index=False, nullable=True)#church born or no true or false
    f_faith = db.Column(db.Text, index=False, nullable=True) # this is the former faith
    d_o_baptism = db.Column(db.DateTime, index=False, nullable=False)#date of baptism
    ch_of_baptism = db.Column(db.Text, index=False, nullable=False)#chrch of baptism
    ch_family = db.Column(db.Text, index=False, nullable=False)
    l_o_AY = db.Column(db.String(120), index=True, nullable=True)#level of AY progression
    lang_spoken = db.Column(db.Text, index=False, nullable=True)#languages spoken
    skills = db.Column(db.Text, index=False, nullable=True)#skills obtained by the member, text datatype
    inc_projects = db.Column(db.Text, index=False, nullable=True) #income generating projects, text 
    hobbies = db.Column(db.Text, index=False, nullable=True)# text
    ch_programs = db.Column(db.Text, index=False, nullable=True)#ch programs to improve upon

    def __repr__(self):
        return '<Member {}>'.format(self.full_name)  

#Table for joing the members to different departments
departmentals = db.Table('departmentals',
    #db.Column('id', db.Integer, primary_key=True),
    db.Column('member_id', db.Integer, db.ForeignKey('department_member.id', ondelete="cascade")),
    db.Column('department_id', db.Integer, db.ForeignKey('department.id', ondelete="cascade"))
)

class DepMember(db.Model):
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

""" Admin accounts creation is handles by this model"""
class Account(db.Model):#This is the admins model.py file
    __tablename__ = 'admin_account'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=False, nullable=False)
    password = db.Column(db.String(128), index=False, nullable=False)  

    def __repr__(self):
        return '<Account {}>'.format(self.username)    



# class Image(db.Model):#This is the admins model.py file
#     __tablename__ = 'image_data1'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120), index=False, nullable=True) 
#     image_file = db.Column(db.String(120), index=False, nullable=True)
    
#     def __repr__(self):
#         return '<Image {}>'.format(self.name) 


