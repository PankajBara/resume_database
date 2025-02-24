from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # SQLite database
db = SQLAlchemy(app)

# Define the Resume model
class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    skills = db.Column(db.String(200), nullable=False)
    experience = db.Column(db.String(500), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Submit resume page
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        skills = request.form['skills']
        experience = request.form['experience']

        # Save to database
        new_resume = Resume(name=name, email=email, phone=phone, skills=skills, experience=experience)
        db.session.add(new_resume)
        db.session.commit()

        return redirect(url_for('view'))
    return render_template('submit.html')

# View resumes page
@app.route('/view')
def view():
    resumes = Resume.query.all()
    return render_template('view.html', resumes=resumes)

if __name__ == '__main__':
    app.run(debug=True)