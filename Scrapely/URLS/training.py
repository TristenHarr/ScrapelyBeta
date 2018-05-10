import sqlite3

from Forms._datasources import *
from Manager._User import User
from conf import load_in
import random
from flask import session, render_template, redirect
from Manager._FileController import FileController
import os
from ScraperTools.BuildModel import MakeModel, TestModel
import pickle
settings = load_in()
settings['unique'] = settings["USERS_DB"][0:settings['USERS_DB'].rfind('/')]


def _training(request):
    from Forms._training import MultiBayesForm, MultiBayesTest, MultiBayesMultiTest
    form = MultiBayesForm(request.form)
    form2 = MultiBayesTest(request.form)
    form3 = MultiBayesMultiTest(request.form)
    if request.method == "POST" and form.validate():
        a = form.traininga.data
        b = form.trainingb.data
        print(a)
        print(b)
        return redirect('/training/{}/{}'.format(a, b))
    elif request.method == "POST" and form2.validate():
        a = form2.testinga.data
        b = form2.testingb.data
        c = form2.controla.data
        d = form2.controlb.data
        return redirect('/testing/{}/{}/{}/{}'.format(c, d, a, b))
    elif request.method == "POST" and form3.validate():
        a = form3.controls
        return redirect('/testing/{}/'.format(a))
    return render_template("User/training.html", form=form, form2=form2)

def _train_table(request, traina, trainb):
    con = sqlite3.connect(settings['USERS_DB'].format(session['username'])).cursor()
    traininga = con.execute("SELECT plain_text FROM {}".format(traina)).fetchall()
    trainingb = con.execute("SELECT plain_text FROM {}".format(trainb)).fetchall()
    a, b = [], []
    for item in traininga:
        a.append(item[0])
    for item in trainingb:
        b.append(item[0])
    my_list = [(item, 0) for item in a]
    my_list2 = [(item, 1) for item in b]
    my_list.extend(my_list2)
    random.shuffle(my_list)
    train1 = []
    train2 = []
    for item in my_list:
        train1.append(item[0])
        train2.append(item[1])
    print(traina, trainb)
    print(train1, train2)
    model = MakeModel(train1, train2, [traina, trainb])
    x = FileController()
    file = x.fetch_path(session['username'])
    f = open(file+"/{}_{}.pickle".format(traina, trainb), 'wb')
    pickle.dump(model, f)
    f.close()
    User(session['username']).create_model("{} VS. {}".format(traina, trainb))
    session['models'] = User(session['username']).fetch_models()
    # f.write('hi')
    # f.close()


    # print(traina, trainb, testa, testb)
    # print("{}/{}v{}".format(x.fetch_path(session['username']), traina, trainb))
    # testlist = [(item, 0) for item in c]
    # testlist2 = [(item, 1) for item in d]
    # testlist.extend(testlist2)
    # print(my_list, testlist)
    return redirect("/training")

def _test_table(request, traina, trainb, testa, testb):
    con = sqlite3.connect(settings['USERS_DB'].format(session['username'])).cursor()
    traininga = con.execute("SELECT plain_text FROM {}".format(testa)).fetchall()
    trainingb = con.execute("SELECT plain_text FROM {}".format(testb)).fetchall()
    a, b = [], []
    for item in traininga:
        a.append(item[0])
    for item in trainingb:
        b.append(item[0])
    my_list = [(item, 0) for item in a]
    my_list2 = [(item, 1) for item in b]
    my_list.extend(my_list2)
    random.shuffle(my_list)
    train1 = []
    train2 = []
    for item in my_list:
        train1.append(item[0])
        train2.append(item[1])
    x = FileController()
    file = x.fetch_path(session['username'])
    f = open(file + "/{}_{}.pickle".format(traina, trainb), 'rb')
    model = pickle.load(f)
    f.close()
    testcase = TestModel(model, train1, train2)
    print(testcase['plain_text'])
    print(testcase['guess'])
    print(testcase['answer'])
    print(testcase['percent'])
    return render_template('User/results.html', training=testcase)

def _delete_model(request, model):
    items = model.replace(' VS. ', '_')
    User(session['username']).delete_model(model)
    session['models'] = User(session['username']).fetch_models()
    x = FileController()
    file = x.fetch_path(session['username'])
    os.remove(file+"/{}.pickle".format(items))
    return redirect("/training")