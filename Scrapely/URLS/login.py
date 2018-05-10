from Forms._login import LoginForm
from Manager._User import User
from flask import session, redirect, render_template


def _login(request):
    form = LoginForm(request.form)
    data_dict = {}
    if request.method == 'POST' and form.validate():
        data_dict['username'] = form.username.data
        data_dict['password'] = form.password.data
        user = User(data_dict['username'])
        if user.login_user(data_dict['password']):
            the_dict = user.load_user()
            for items in the_dict.items():
                session[items[0]] = items[1]
            return redirect("/datasets")
    return render_template('Arrival/login.html', form=form)
