import sqlite3

import pandas as pd
#from Manager._SuperTable import SuperTable
from Manager._User import User
from ScraperTools.TwitterScraper import Scraper
from conf import load_in
from flask import render_template, Response, stream_with_context, session, redirect
settings = load_in()


def _datasets(request):
    from Forms._datasets import ScrapeKeywordsForm, ExportForm
    form = ScrapeKeywordsForm(request.form)
    form2 = ExportForm(request.form)
    if request.method == 'POST' and form.validate():
        limit = form.limit.data
        limit_type = form.limit_type.data
        keywords = form.keywords.data
        table = form.table.data
        password = form.password.data
        con = sqlite3.connect(settings['MAIN_DB'])
        con.execute("""CREATE TABLE IF NOT EXISTS {tn} (username TEXT,
                                       table_name TEXT,
                                       keywords TEXT,
                                       PRIMARY KEY (username, table_name))""".format(tn="KeywordTable"))
        con.execute("""INSERT INTO KeywordTable VALUES (?,?,?)""", (session['username'], table, keywords))
        con.commit()
        con.close()
        my_list = list(map(lambda x: x.strip(), keywords.split(',')))

        def load_stuff(lim_type, lim, mylist, the_table, current_session):
            if User(current_session['username']).login_user(password):
                thing = Scraper('track')
                thing.set_limit(lim_type, lim)
                thing.set_languages(['en'])
                thing.search_configure(mylist)
                thing.database_config(current_session['username'], the_table)
                thing.set_keys(User(current_session['username']).load_in_keys())
                User(session['username']).make_data(table)
                thing.scrape()
            stuff = User(current_session['username']).load_user()
            current_session['data_tables'] = stuff['data_tables']
            current_session['table_count_keywords'] = stuff['table_count_keywords']
            yield render_template('User/datasets.html',
                                  form=form,
                                  form2=form2,
                                  session=current_session)

        return Response(stream_with_context(load_stuff(limit_type, limit, my_list, table, session)))
    elif request.method == 'POST' and form2.validate():
        table = form2.table.data
        selected = form2.choice.data
        con = sqlite3.connect(settings['USERS_DB'].format(session['username']))
        if table in session['data_tables']:
            my_frame = pd.read_sql_query("SELECT * FROM '{}'".format(table), con)
            if selected == 'json':
                file = my_frame.to_json()
                mimetype = "application/json"
                filetype = '.json'
            elif selected == 'csv':
                file = my_frame.to_csv()
                mimetype = 'test/csv'
                filetype = ".csv"
            elif selected == 'excel':
                file = my_frame.to_excel(pd.ExcelWriter('output.xlsx'))
                mimetype = 'application/vnd.ms-excel'
                filetype = '.xlsx'
            elif selected == 'html':
                file = my_frame.to_html()
                mimetype = 'text/html'
                filetype = '.html'
            elif selected == 'LaTeX':
                file = my_frame.to_latex()
                mimetype = 'application/x-latex'
                filetype = '.tex'
            return Response(file, mimetype=mimetype, headers={'Content-disposition':
                                                              "attachment; filename={}{}".format(table,
                                                                                                     filetype)})
        return render_template("User/datasets.html", form=form, session=session, form2=form2)
    else:
        return render_template("User/datasets.html", form=form, session=session, form2=form2)


def _delete_table(request, item):
    User(session['username']).delete_data(item)
    session['data_tables'] = User(session['username']).fetch_table_list()
    con = sqlite3.connect(settings['MAIN_DB'])
    con.execute("DELETE FROM KeywordTable  WHERE username=? AND table_name=?", (session['username'], item))
    con.commit()
    con.close()
    con = sqlite3.connect(settings['USERS_DB'].format(session['username']))
    con.execute("DROP TABLE IF EXISTS {}".format(item))
    con.commit()
    con.close()
    stuff = User(session['username']).load_user()
    session['data_tables'] = stuff['data_tables']
    session['table_count_keywords'] = stuff['table_count_keywords']
    return redirect("/datasets")

def _view_table(request, table):
    con = sqlite3.connect(settings['USERS_DB'].format(session['username']))
    pd.set_option('display.max_colwidth', -1)
    my_frame = pd.read_sql_query("SELECT hashtags, tweet, tweeted_time, user_name, user_description, user_handle FROM '{}'".format(table), con)
    my_dict = my_frame.to_dict()
    hashtags = []
    tweets = []
    tweet_time = []
    tweeter = []
    desc = []
    looplist = [('None', 'None', 'None', 'None', 'None')]
    for i in range(len(my_dict['hashtags'])):
        items = [my_dict['hashtags'][i],
                 my_dict['tweet'][i],
                 my_dict['tweeted_time'][i],
                 my_dict['user_name'][i],
                 my_dict['user_description'][i]]
        if len(items[0]) == 0:
            hashtags.append("None")
        else:
            hashtags.append("  ".join(list(map(lambda y: "#" + y, items[0].strip('`').split('`')))))
        tweets.append(items[1])
        tweet_time.append(items[2])
        tweeter.append(items[3])
        desc.append(items[4])
        looplist = list(zip(tweeter, tweets, hashtags, desc, tweet_time))
    return render_template("User/TableView.html", items=looplist)

def _supertable(request, table):
    x = SuperTable('tweet', table, session['username'])
    x.generate_functions()
    x.main_maker()
    return Response(x.table_starter(10))
