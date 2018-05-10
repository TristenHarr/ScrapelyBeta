from Forms._SuperTable import *
from flask import session, render_template
import sqlite3
from Manager._TableWork import SuperTable

def _SuperTable(request, table, action):
    dropform = DropForm(request.form)
    swapform = SwapForm(request.form)
    tableform = TableForm(request.form)
    savenew = SaveNew(request.form)
    pushform = PushForm(request.form)
    newrow = NewRow(request.form)
    if action == "drop" and request.method == 'POST' and dropform.validate():
        select = dropform.droptype.data
        droptable = dropform.dropselection.data
        print(select, droptable)

    elif action == 'swap' and request.method == "POST" and swapform.validate():
        swaptype = swapform.swaptype.data
        swap1 = swapform.swapselection1.data
        swap2 = swapform.swapselection2.data
        print(swaptype, swap1, swap2)
    elif action == 'select_table' and request.method == 'POST' and tableform.validate():
        table = tableform.table.data
        print(table)
    elif action == 'save_new' and request.method == "POST" and savenew.validate():
        name = savenew.name.data
        print(name)
    elif action == 'push' and request.method == 'POST' and pushform.validate():
        password = pushform.password.data
        print(password)
    elif action == 'new_row' and request.method == "POST" and newrow.validate():
        datatype = newrow.datatype.data
        rowname = newrow.rowname.data
        backfill = newrow.backfill.data
        print(datatype, rowname, backfill)
    return render_template('User/SuperTable.html',
                           dropform=dropform,
                           swapform=swapform,
                           tableform=tableform,
                           savenew=savenew,
                           pushform=pushform,
                           newrow=newrow,
                           table=table,
                           superdata=SuperTable(table, session['username']).send_off())