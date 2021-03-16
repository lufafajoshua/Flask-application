from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, RadioField, DateField, FileField, FormField, IntegerField, SelectField, BooleanField, FormField, FieldList, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length
from wtforms import validators
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class


photos = UploadSet('photos', IMAGES)

class ImageForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(['png', 'jpg', 'jpeg']), FileRequired('File was empty!')])
    name = StringField('name')
    
class ImageSearch(FlaskForm):
    name = StringField('Photo name')
        # class ImageForm(FlaskForm):
        #     name = StringField('name')
        #     submit = SubmitField('Ok')

class SearchForm(FlaskForm):
    select = SelectField('select:', choices=[('Member','Member'), ('church family','Church family'), ('gender','gender')])#provide a criteria for searching data
    search = StringField('search:', [DataRequired()])
    #submit = SubmitField('ok')
    #select = SelectField('select', choices=[('Member', 'church family', 'gender')])#provide a criteria for searching data

class FamilyForm(FlaskForm):
    select = SelectField('select:', choices=[('judha','Judha'), ('mathew','Mathew'), ('mark','Mark'), ('john','John'), ('luke','Luke'), ('gad','Gad')])

class TelephoneForm(FlaskForm):
    country_code = IntegerField('Country Code', [DataRequired()])
    number       = StringField('Number') 

class AdminForm(FlaskForm):
    username = StringField('username', [DataRequired()])
    password = PasswordField('password', [DataRequired()])
    password1 = PasswordField('confirm password', [DataRequired()])#compare with the first password entered to ensure that the user is aware of his password

class EditForm(FlaskForm):#This does not include The image filefield coz its updated separately
    full_name = StringField('Full name', [DataRequired()])
    gender = RadioField('Gender', [DataRequired()], choices=[('Male', 'Male'), ('Female', 'Female')]) 
    date_added = DateField('Date Added')
    telephone_no = StringField('Telephone Contact')#create a telephone form class which ths value subclasses 
    address = StringField('Address', [DataRequired()]) 
    a_o_residence = StringField('Area of Residence', [DataRequired()]) 
    d_o_birth = DateField('Date Of Birth', [DataRequired()])#this stores the date of birth
    age = IntegerField('Age', [DataRequired()]) 
    m_status = RadioField('Marital Status', [DataRequired()], choices=[('single', 'Single'), ('married', 'Married')]) 
    no_children = IntegerField('Number of children') #number of children, provide a default value
    occupation = StringField('Occupation') 
    l_o_educ = SelectField('Level of Education', choices=[('primary', 'Primary'), ('secondary', 'Secondary'), ('university', 'University')])#level of education
    p_o_work = StringField('Place of work')#place of work
    employer = StringField('Employer')  
    nationality = StringField('Nationality', [DataRequired()])
    tribe = StringField('Tribe')
    clan = StringField('Clan')
    ch_born = SelectField('Church born!', choices=[('yes', 'Yes'), ('no', 'No')])#church born or no true or false check for usage of the boolean field
    f_faith = StringField('former Faith') # this is the former faith
    d_o_baptism = DateField('Date Of Baptism')#date of baptism
    ch_of_baptism = StringField('Church of baptism', [DataRequired()])#chrch of baptism
    ch_family = StringField('church family',[DataRequired()])
    l_o_AY = SelectField('level of AY progression', choices=[('ambassadors', 'Ambassadors'), ('adventurer', 'Adventurer'), ('pathfinder', 'Pathfinder'), ('master guide', 'Master guide')])#level of AY progression
    lang_spoken = TextAreaField('Languages Spoken')#languages spoken
    skills = TextAreaField('Skills')#skills obtained by the member, text datatype
    inc_projects = TextAreaField('Income Generating Projects') #income generating projects, text 
    hobbies = TextAreaField('Hobbies')# text
    ch_programs = TextAreaField('Church Programs To Improve Upon')#ch programs to improve upon
    #submit = SubmitField('OK')

class MemberForm(FlaskForm):
    #id = (db.Integer, primary_key=True)#you can also specify the user string to refer to the id
    #photo = FileField(validators=[FileAllowed(photos, 'Image only!')])#, FileRequired('File was empty!')
    full_name = StringField('Full name', [DataRequired()])
    gender = RadioField('Gender', [DataRequired()], choices=[('Male', 'Male'), ('Female', 'Female')]) 
    date_added = DateField('Date Added')
    telephone_no = StringField('Telephone Contact')#create a telephone form class which ths value subclasses 
    address = StringField('Address', [DataRequired()]) 
    a_o_residence = StringField('Area of Residence', [DataRequired()]) 
    d_o_birth = DateField('Date Of Birth', [DataRequired()])#this stores the date of birth
    age = IntegerField('Age', [DataRequired()]) 
    m_status = RadioField('Marital Status', [DataRequired()], choices=[('single', 'Single'), ('married', 'Married')]) 
    no_children = IntegerField('Number of children') #number of children, provide a default value
    occupation = StringField('Occupation') 
    l_o_educ = SelectField('Level of Education', choices=[('primary', 'Primary'), ('secondary', 'Secondary'), ('university', 'University')])#level of education
    p_o_work = StringField('Place of work')#place of work
    employer = StringField('Employer')  
    nationality = StringField('Nationality', [DataRequired()])
    tribe = StringField('Tribe')
    clan = StringField('Clan')
    ch_born = SelectField('Church born!', choices=[('yes', 'Yes'), ('no', 'No')])#church born or no true or false check for usage of the boolean field
    f_faith = StringField('former Faith') # this is the former faith
    d_o_baptism = DateField('Date Of Baptism')#date of baptism
    ch_of_baptism = StringField('Church of baptism', [DataRequired()])#chrch of baptism
    ch_family = StringField('church family',[DataRequired()])
    l_o_AY = SelectField('level of AY progression', choices=[('ambassadors', 'Ambassadors'),('adventurer', 'Adventurer'), ('pathfinder', 'Pathfinder'), ('master guide', 'Master guide')])#level of AY progression
    lang_spoken = TextAreaField('Languages Spoken')#languages spoken
    skills = TextAreaField('Skills')#skills obtained by the member, text datatype
    inc_projects = TextAreaField('Income Generating Projects') #income generating projects, text 
    hobbies = TextAreaField('Hobbies')# text
    ch_programs = TextAreaField('Church Programs To Improve Upon')#ch programs to improve upon
    #submit = SubmitField('save')

class DepartmentForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    
class AddMemberForm(FlaskForm):
    name = StringField('Name', [DataRequired()]) 
    position = SelectField('Position', choices=[('head', 'Head'), ('secretary', 'Secretary'), ('treasurer', 'Treasurer'), ('publicity', 'Publicity'), ('communications', 'Communications')])
       
class DepartmentMemberForm(FlaskForm):#Form for the member to be added to the department
    name = StringField('Name', [DataRequired()])
    position = SelectField('Position', choices=[('head', 'Head'), ('secretary', 'Secretary'), ('treasurer', 'Treasurer'), ('publicity', 'Publicity'), ('communications', 'Communications')])
    
    departments = SelectMultipleField('Departments', coerce=int,  widget=widgets.ListWidget(prefix_label=True), option_widget=widgets.CheckboxInput())

    def set_choices(self):
        self.departments.choices = [(d.id, d.name) for d in Department.query.all()]

class MemberEditForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    position = SelectField('Position', choices=[('head', 'Head'), ('secretary', 'Secretary'), ('treasurer', 'Treasurer'), ('publicity', 'Publicity'), ('communications', 'Communications')])

 