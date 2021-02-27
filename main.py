from flask import Flask, render_template, redirect
from data import db_session
from data.users import User, Job
import datetime
from forms.user import RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")
    # add_users()
    # add_jobs()
    app.run(port=8080, host='127.0.0.1')


def add_users():
    crew = [
        {
            'surname': 'Scott',
            'name': 'Ridley',
            'age': 21,
            'position': 'captain',
            'speciality': 'research engineer',
            'address': 'module_1',
            'email': 'scott_chief@mars.org'
        },
        {
            'surname': 'Weir',
            'name': 'Andy',
            'age': 24,
            'position': 'researcher',
            'speciality': 'biologist',
            'address': 'module_2',
            'email': 'andy_weir@mars.org'
        },
        {
            'surname': 'Watny',
            'name': 'Mark',
            'age': 25,
            'position': 'researcher',
            'speciality': 'terraform engineer',
            'address': 'module_3',
            'email': 'mark_watny@mars.org'
        },
        {
            'surname': 'Kapoor',
            'name': 'Vincent',
            'age': 22,
            'position': 'director',
            'speciality': 'climatologist',
            'address': 'module_4',
            'email': 'vincent_kapoor@mars.org'
        }
    ]
    db_sess = db_session.create_session()
    for person in crew:
        user = User()
        user.surname = person['surname']
        user.name = person['name']
        user.age = person['age']
        user.position = person['position']
        user.speciality = person['speciality']
        user.address = person['address']
        user.email = person['email']
        db_sess.add(user)
    db_sess.commit()


def add_jobs():
    occupations = [
        {
            'team_leader': 1,
            'job': 'Deployment of residential modules 1 and 2',
            'work_size': 15,
            'collaborators': '2, 3',
            'start_date': datetime.datetime.now(),
            'is_finished': False
        },
        {
            'team_leader': 2,
            'job': 'Exploration of mineral resources',
            'work_size': 15,
            'collaborators': '4, 3',
            'start_date': datetime.datetime.now(),
            'is_finished': False
        },
        {
            'team_leader': 3,
            'job': 'Development of a management system',
            'work_size': 25,
            'collaborators': '5',
            'start_date': datetime.datetime.now(),
            'is_finished': False
        }
    ]
    db_sess = db_session.create_session()
    for occupation in occupations:
        job = Job()
        job.team_leader = occupation['team_leader']
        job.job = occupation['job']
        job.work_size = occupation['work_size']
        job.collaborators = occupation['collaborators']
        job.start_date = occupation['start_date']
        job.is_finished = occupation['is_finished']
        db_sess.add(job)
    db_sess.commit()


@app.route('/')
def fill_in_jobs():
    jobs = []
    db_sess = db_session.create_session()
    for job in db_sess.query(Job).all():
        for user in db_sess.query(User).filter(User.id == job.team_leader):
            data = [job.job, user.surname + ' ' + user.name, job.work_size, job.collaborators]
            if job.is_finished:
                data.append('Is finished')
            else:
                data.append('Is not finished')
            jobs.append(data)
    return render_template('occupation.html', jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register form',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register form',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            age=int(form.age.data),
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login')
def login():
    return 'Вы были успешно зарегистрированы'


if __name__ == '__main__':
    main()