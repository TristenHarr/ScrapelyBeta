import random

from conf import load_in
from flask import Flask, session, redirect, request






settings = load_in()
app = Flask(__name__)
app.secret_key = bytes(random.getrandbits(16))


########################################################################################################################
#   SESSION CONFIGURATION
########################################################################################################################


def login_required():
    if session['counter'] < 2:
        session.clear()
        return True


def sumsessioncounter():
    try:
        session['counter'] += 1
    except KeyError:
        session['counter'] = 1


########################################################################################################################
#   LOGIN AND REGISTER URLS
########################################################################################################################
from URLS.register import _register
from URLS.login import _login


@app.route('/')
def arrival():
    return redirect('/login')


@app.route('/register', methods=['POST', 'GET'])
def register():
    return _register(request)


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login")


@app.route('/login', methods=["GET", "POST"])
def login():
    sumsessioncounter()
    return _login(request)


########################################################################################################################
#   HOMEPAGE URL
########################################################################################################################
#from URLS.homepage import _homepage

#@app.route('/home')
#def homepage():
#    sumsessioncounter()
#    if login_required():
#        return redirect("/login")
#    return _homepage(request)


########################################################################################################################
#   DATASOURCES URLS
########################################################################################################################
from URLS.datasources import _datasources, _delete_datasource

@app.route('/datasources', methods=['POST', 'GET'])
def datasources():
    sumsessioncounter()
    if login_required():
        return redirect('/login')
    return _datasources(request)


@app.route('/datasources/delete/<item>')
def delete_datasource(item):
    sumsessioncounter()
    if login_required():
        return redirect('/login')
    return _delete_datasource(request, item)



########################################################################################################################
#   DATASETS URLS
########################################################################################################################
from URLS.datasets import _datasets, _delete_table, _view_table

@app.route('/datasets', methods=['POST', 'GET'])
def datasets():
    sumsessioncounter()
    if login_required():
        return redirect('/login')
    return _datasets(request)

@app.route('/datasets/delete/<item>')
def delete_table(item):
    sumsessioncounter()
    if login_required():
        return redirect('/login')
    return _delete_table(request, item)


@app.route('/datasets/view/<table>')
def view_table(table):
    sumsessioncounter()
    if login_required():
        return redirect('/login')
    return _view_table(request, table)

# FUTURES

#@app.route('/datasets/supertable/<table>', methods=["POST", "GET"])
#def supertable(table):
#    sumsessioncounter()
#    if login_required():
#        redirect('/login')
#    return _supertable(request, table)

########################################################################################################################
#   SUPER-TABLE FUTURES
########################################################################################################################

#@app.route('/datasets/SUPERTABLE/<table>/<action>', methods=['POST', "GET"])
#def SuperTable(table, action):
#    sumsessioncounter()
#    if login_required():
#        redirect("/login")
#    from URLS.SuperTable import _SuperTable
#    return _SuperTable(request, table, action)
########################################################################################################################
#   Training
########################################################################################################################
@app.route('/training', methods=["POST", "GET"])
def training():
    sumsessioncounter()
    if login_required():
        return redirect('/login')
    from URLS.training import _training
    return _training(request)

@app.route('/training/<traininga>/<trainingb>')
def train(traininga, trainingb):
    sumsessioncounter()
    if login_required():
        return redirect('/login')
    from URLS.training import _train_table
    return _train_table(request, traininga, trainingb)


@app.route('/testing/<traina>/<trainb>/<testinga>/<testingb>', methods=["POST", "GET"])
def testing(traina, trainb, testinga, testingb):
    sumsessioncounter()
    if login_required():
        return redirect('/login')
    from URLS.training import _test_table
    return _test_table(request, traina, trainb, testinga, testingb)

@app.route('/training/delete/<item>')
def delete_model(item):
    sumsessioncounter()
    if login_required():
        return redirect('/login')
    from URLS.training import _delete_model
    return _delete_model(request, item)




if __name__ == '__main__':
    app.run()
