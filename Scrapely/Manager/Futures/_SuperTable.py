import pandas as pd
import sqlite3
from conf import load_in
settings = load_in()


class SuperTable(object):

    def __init__(self, primary_key, table, username):
        self.table = table
        self.primary_key = primary_key
        self.con = sqlite3.connect(settings['USERS_DB'].format(username))
        pd.set_option('display.max_colwidth', -1)
        self.frame = pd.read_sql_query("SELECT * FROM '{}'".format(table), self.con)
        self.Pkeys = pd.read_sql_query("SELECT {} FROM '{}'".format(primary_key, table), self.con)
        self.indices = list(self.frame.keys())
        self.functions = {}
        self.function_text = ""
        self.main_op = ""

    def generate_functions(self):
        for i,item in enumerate(list(self.frame.keys())):
            left = "{"
            right = "}"
            the_string = """
            function {item}_finder() {left}
                var input, filter, table, tr, td, i, maybe;
                maybe = [];
                input = document.getElementById("{item}");
                filter = input.value.toUpperCase();
                table = document.getElementById("{tn}");
                tr = table.getElementsByTagName("tr");
                for (i = 0; i < tr.length; i++) {left}
                    td = tr[i].getElementsByTagName("td")[{i}];
                    if (td) {left}
                        if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {left}
                            {right} else {left}
                            maybe.push(i)
                                        {right}
                            {right}
                        {right}
                    return maybe;
                {right}
            """.format(item=item, tn=self.table, left=left, right=right, i=i)
            self.functions[item] = ["{}_finder()".format(item), "{}_array".format(item)]
            self.function_text += the_string

    def main_maker(self):
        prev = ""
        starter = """function main() {
                        var i, table, tr;
                        """
        for i, item in enumerate(self.functions[sorted(self.functions.keys())[i]] for i in range(len(self.functions))):
            if i == 0:
                starter += "var {} = {};\n".format(item[1], item[0])
                prev = item[1]
            else:
                stringss = """var {} = {}.concat({});\n""".format(item[1], prev, item[0])
                starter += stringss
                prev = item[1]
        else:
            ender = """table = document.getElementById("{tb}");
                        tr = table.getElementsByTagName("tr");
                        for (i = 0; i < tr.length; i++) {left}
                            if ({prev}.includes(i)){left}
                            tr[i].style.display = "none";
                            {right} else {left}
                        tr[i].style.display = "";
                        {right}
                    {right}
                {right}""".format(tb=self.table, prev=prev, left="{", right="}")
        self.main_op = self.function_text+starter+ender


    def table_starter(self, width):
        start = """
<!DOCTYPE html>
<html>
    <head>
    <style>
    * {left}
    box-sizing: border-box;
    {right}

    #{tb} {left}
    border-collapse: collapse;
    width: 100%;
    border: 1px solid #ddd;
    font-size: 18px;
    {right}
    
    #{tb} th, #myTable td {left}
    text-align: left;
    padding: 12px;
    {right}

    #{tb} tr {left}
    border-bottom: 1px solid #ddd;
    {right}

    #{tb} tr.header, #myTable tr:hover {left}
    background-color: #f1f1f1;
    {right}
    </style>
    <script>""".format(tb=self.table, left="{", right="}")+self.main_op+"</script>"

        start +="""</head><body>"""+"""<table id="{tb}">
      <tr class="header">""".format(tb=self.table)
        body = """"""
        for item in self.indices:
            body += """
        <th style="width:{wid}%;"><input type="text" id="{item}" onkeyup="main()" placeholder="Search by {item}.." title="Search {item}">
    </th>\n""".format(wid=width, item=item)
        body += "</tr><tr>"
        data = []
        # print(body)
        for row in self.frame.as_matrix():
            data.append(list(zip(row, self.indices)))
        for item in data:
            body +=str("""
            <td contenteditable='true'>{}</td>"""*len(item)).format(*[stuff[0] for stuff in item])+"</tr> <tr>"
        body = body.rstrip('<tr>')+"</table></body></html>"
        return start+body
