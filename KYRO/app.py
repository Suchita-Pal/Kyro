import os
import speech_recognition as sr
import pyttsx3
from flask import Flask,render_template , request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

current_dir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(current_dir,"database.sqlite3")

app.config['SQLALCHEMY_MODIFICATION'] = False

db = SQLAlchemy(app)

app.app_context().push()

###############################  Models and Tables  ##############################

class User(db.Model):
    __tablename__ = 'user'
    UserID = db.Column(db.Integer, primary_key = True, autoincrement =True)
    UserName = db.Column(db.String(500), nullable =False)
    Email =  db.Column(db.String(500), nullable =False)
    Password = db.Column(db.String(500), nullable =False) 

    analyzerR = db.relationship('Analyzer',backref='user',lazy=True)
    

class Analyzer(db.Model):
    __tablename__ = 'analyzer'
    ID = db.Column(db.Integer, primary_key = True, autoincrement =True)
    UserName = db.Column(db.String(500), db.ForeignKey('user.UserName'), nullable =False)
    Transcription = db.Column(db.String(5000), nullable =False)
    FreqWords = db.Column(db.String(500), nullable = False)

@app.route('/usersignup', methods=['GET','POST'])
def usersignup():
    if request.method =='POST':
        UserName = request.form['username']
        Email = request.form['email']
        Password = request.form['password']

        user = User(UserName=UserName, Email=Email, Password=Password)
        db.session.add(user)
        db.session.commit()

        return "signup done"



@app.route('/userlogin', methods=['GET','POST'])
def userlogin():
    if request.method =='POST':
        UserName = request.form['username']
        Password = request.form['password']

        user = User.query.filter_by(UserName=UserName, Password=Password, Role='User').first()
        
        if user:
            return "User Login Done"
        else:
            return "User Login failed"       
        
@app.route('/transcript', methods=['GET','POST'])
def transcript(command):
    if request.method =='POST':
        UserName = request.form['username']
        

        user = User.query.filter_by(UserName=UserName, Role='User').first()
        
       # Initialize the recognizer 
    r = sr.Recognizer() 
 
     
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command) 
    engine.runAndWait()
     
     
    # Loop infinitely for user to
    # speak
 
    while(1):    
     
    
        try:
            
            with sr.Microphone() as source2:
             
           
                r.adjust_for_ambient_noise(source2, duration=0.2)
             
            
                audio2 = r.listen(source2)
             
            # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
 
                print("Did you say ",MyText)
                SpeakText(MyText)
             
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
         
        except sr.UnknownValueError:
            print("unknown error occurred")        


@app.route('/')
def hello():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)