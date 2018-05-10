from flask import render_template


def _homepage(request):
    return render_template('User/base.html')
