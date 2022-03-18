from prettytable import PrettyTable
x = PrettyTable(title="Hdsd")

x.add_row(["Adelaide", 1295, 1158259, 600.5])
x.add_row(["Brisbane", 5905, 1857594, 1146.4])


x = x.get_string(title="Australian cities")
print(x)

x.add_row(["dsdds", 5905, 1857594, 1146.4])
print(x)

yfd = PrettyTable()

yfd.add_row(["12", 1295, 1158259, 600.5])
yfd.add_row(["123", 5905, 1857594, 1146.4])

va = "herwr"

print(yfd)
