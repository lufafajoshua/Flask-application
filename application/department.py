from models import Member

class Department(db.Model):
    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=False, nullable=False)#Name of each created department

        # member_id = db.column(db.Integer, db.ForeignKey('member.id', nullable=True))#Reference a member from the memebr model to avoid redundancy
        # position = db.Column(db.String(128), index=False, nullable=True)

    def __repr__(self):
        return '<Department {}>'.format(self.name)  

class DepartmentMember(db.Model):#This is the table for the memebrs in the department
    __tablename__ = 'department_members'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.column(db.Integer, db.ForeignKey('member.id', nullable=True))#Reference a member from the memebr model to avoid redundancy
    position = db.Column(db.String(128), index=False, nullable=True)
    department = db.relationship('Department', backref=db.backref('departmentmembers', lazy=True))#Create a reationship with the departmrnt model
    
    def __repr__(self):
        return '<DepartmentMembers {}>'.format(self.member_id)  

@app.route('/department', methods=['GET', 'POST'])
def create_department():
    #pass the model where the data is to be sent for saving ie department model

    #Pass the form data from the frontend
    name = request.form.get('name')
    if request.method == 'POST':
        department = Department()
        department.name = request.form.get('name')


    #point to a function to add members to the department with their respective positions

    return render_template('department.html')

@app.route('/add_member/<int:id>')
def add_member():
    #Pass the department member model where the data is passed to be saved to the databse

    #first get the department that you are adding members too
    qry = db.session.query(Department).filter(Department.id==id)#the department id for the department trying to add the members
    department = qry.first()

    position = request.form.get('position')#The position of the member
    #Query the member model for a particular member object
    department.departmentmembers.append(member)#The member parameter points to the member id in the front end
    db.session.add(department)
    return render_template('add_member.html')

@app.route('/select_member/<int:id>', methods=['GET', 'POST'])#The id for the member object to be added to the department
def select_member():
    qry = db.session.query(Member).filter(Member.id==id)#Make this a button 
    member = qry.first()
    #Send the member object to the department object to be added as a member

    return render_template('select_member.html')

@app.route('/all', methods=['GET', 'POST'])
def all_members():
    qry = db.session.query(Member)
    results = qry.all() 
    table = Department_Member(results)
    table.border = True
    return render_template('department_data.html', table=table)
    




    
    





