from prettytable import PrettyTable
x = PrettyTable(title="function: bubbleSort")

x.add_row(["Adelaide", 1295, 1158259, 600.5])
x.add_row(["Brisbane", 5905, 1857594, 1146.4])

print(x)




print(x.rows[1][0])


yfd = PrettyTable(title="bubbleSort",header=False)

yfd.add_row(["function", "bubbleSort", "(integer[],integer):void ", x])

x = PrettyTable(title="global", header=False)
print(yfd)
x.add_row([yfd])
x.add_row([yfd])

print(x)

print("""""""""""")

ors = PrettyTable(title="Class bubbleSort",header=False)

ors.add_row(["function", "bubbleSort", "(integer[],integer):void ", ""])
ors.add_row(["dsd", "bubbleSdsdort", "dsd", ""])
ors.add_row(["","","",x])

x = PrettyTable(title="global", header=False)
print(yfd)
x.add_row([yfd])
x.add_row([yfd])


print(x)


from prettytable import PrettyTable

table = PrettyTable(["Column 1", "Column 2", "Column 3"])
table.add_row(["A", "B", "C"])
table.add_row(["F", "O", "O"])
table.add_row(["B", "A", "R"])

print(table)
print(table.rows[2][0])

table2 = PrettyTable(["Column 1", "Column 2", "Column 3"])
table2.add_row(["1", "2", "3"])
table2.add_row(["4", "5", "6"])
table2.add_row(["7", "8", table])

print(table2)

# for row in table:
#     row.border = False
#     row.header = False
#     print (row.get_string(fields=["Column 2"]).strip() )# Column 1

for row in table2:
    row.border = False
    row.header = False
    print(row)
#modify entries
table2.rows[2][2].rows[0][1] = "C"
print(table2.rows[2][2].rows[0][1])

#set title after
print(table2.title)
table2.title="Goog"
print(table2)

print(ors.title)


x = PrettyTable(title="func 1")

x.field_names = ["inherlist", "dataTable", "functions", "location"]
x.add_rows(
    [
        ["LINEAR", 1295, 1158259, 600.5],
        ["poly", 5905, 1857594, 1146.4],
        ["", 112, 120900, 1714.7],
        ["Hobart", 1357, 205556, 619.5],
        ["Sydney", 2058, 4336374, 1214.8],
        ["Melbourne", 1566, 3806092, 646.9],
        ["Perth", 5386, 1554769, 869.4],
    ]
)


print(x)
print(x.get_string(fields=["inherlist", "dataTable"], start = 4, end=5).strip())

print(x.rows[1][2])

for row in x:
    print(row.get_string(fields=["inherlist", "dataTable"]).strip())


x2 = PrettyTable(title="func 2")

x2.field_names = ["inherlist", "dataTable", "functions", "location"]
x2.add_rows(
    [
        ["LINEAR", 1295, 1158259, 600.5],
    ]
)


y = PrettyTable(title="class B")

y.field_names = ["inherlist", "dataTable", "functions", "location"]
y.add_rows(
    [
        [["LINEAR", "poly"], table, [x,x2,x], 2],
    ]
)

print(y)

func2 = y.rows[0][2][1]

print(func2)