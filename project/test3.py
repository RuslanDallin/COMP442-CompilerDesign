from prettytable import PrettyTable
x = PrettyTable(title="function: bubbleSort", header=False)

x.add_row(["Adelaide", 1295, 1158259, 600.5])
x.add_row(["Brisbane", 5905, 1857594, 1146.4])




# x = x.get_string(title="Australian cities")
print(x)


yfd = PrettyTable(header=False)

yfd.add_row(["function", "bubbleSort", "(integer[],integer):void ", x])


print(yfd)
