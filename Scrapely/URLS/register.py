from Forms._register import RegistrationForm
from Manager._CreateUser import CreateUser
from Manager._FileController import FileController
from flask import render_template, redirect


def _register(request):
    form = RegistrationForm(request.form)
    data_dict = {}
    if request.method == 'POST' and form.validate():
        data_dict['email'] = form.email.data
        data_dict['username'] = form.username.data
        data_dict['password'] = form.password.data
        data_dict['email'] = form.email.data
        user = CreateUser(data_dict)
        success = user.make_account()
        if not success:
            return render_template('Arrival/signup.html', form=form, nameerror="That username is taken")
        else:
            FileController().file_handler(data_dict['username'])
            return redirect("login")
    return render_template('Arrival/signup.html', form=form)
