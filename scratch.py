from data import db_session
from data.users import User, Job


global_init(input())
db_sess = create_session()
for user in db_sess.query(User).filter(User.address == 'module_1', User.position.notlike('%engineer%'),
                                       User.speciality.notlike('%engineer%')):
    print(user.id)
