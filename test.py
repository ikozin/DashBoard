#data = "1,2,3".split(",")
#print(data)
#print ('%s.' % ', '.join(data))
#data = ('1', '2', '3')
#print ('%s.' % ', '.join(data))

print("1,".split(","))
print("1,".split(","))
print()

def func(*args):

    print(args, end=" ")
    print(len(args))

    step = int(args[0]) if len(args) == 1 else 1
    print(step)


func(-2)
