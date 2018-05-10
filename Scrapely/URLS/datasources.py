import sqlite3
from Forms._datasources import *
from Manager._User import User
from conf import load_in
from cryptography.fernet import Fernet, MultiFernet
from flask import session, render_template, redirect
settings = load_in()


def _datasources(request):
    form = TwitterForm(request.form)
    if request.method == 'POST' and form.validate():
        m1 = form.access_token.data
        m2 = form.access_token_secret.data
        m3 = form.consumer_key.data
        m4 = form.consumer_secret.data
        my_list = [bytes(m1, 'utf-8'), bytes(m2, 'utf-8'), bytes(m3, 'utf-8'), bytes(m4, 'utf-8')]
        first = Fernet.generate_key()
        second = Fernet.generate_key()
        key1 = Fernet(first)
        key2 = Fernet(second)
        x = MultiFernet([key1, key2])
        token1 = x.encrypt(my_list[0])
        token2 = x.encrypt(my_list[1])
        token3 = x.encrypt(my_list[2])
        token4 = x.encrypt(my_list[3])
        con = sqlite3.connect(settings['MAIN_DB'])
        con.execute("""CREATE TABLE IF NOT EXISTS {tn} (username TEXT,
                               key1 BLOB,
                               key2 BLOB, PRIMARY KEY (username))""".format(tn="secret_keys"))
        con.execute("""INSERT INTO secret_keys VALUES (?,?,?)""", (session['username'], first, second))
        con.execute("""CREATE TABLE IF NOT EXISTS {tn} (username TEXT,
                       access_token BLOB,
                       access_token_secret BLOB,
                       consumer_key BLOB,
                       consumer_secret BLOB, PRIMARY KEY (username))""".format(tn="secrets"))
        con.execute("""INSERT INTO secrets VALUES (?,?,?,?,?)""", (session['username'], token1, token2, token3, token4))
        con.commit()
        con.close()
        User(session['username']).create_data_source("Twitter")
        session['data_sources'] = User(session['username']).fetch_data_list()
        sources = User(session['username']).fetch_data_list()
        return render_template('User/datasources.html', form=form, sources=sources)
    else:
        sources = User(session['username']).fetch_data_list()
        return render_template('User/datasources.html', form=form, sources=sources)


def _delete_datasource(request, item):
    User(session['username']).delete_source(item)
    session['data_sources'] = User(session['username']).fetch_data_list()
    con = sqlite3.connect(settings['MAIN_DB'])
    con.execute("DELETE FROM secrets WHERE username='{}'".format(session['username']))
    con.execute("DELETE FROM secret_keys WHERE username='{}'".format(session['username']))
    con.commit()
    con.close()
    return redirect("/datasources")
