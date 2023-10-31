# this script only reads the last input from the buffer
# it will ignore all carriage returns
# teststream.txt will have all the contents of the buffer

textfile = 'teststream.txt'

def cleansn(text):
    list = text.split("\n")
    if len(list)>1:
        list = [i for i in list if i]
        last = list[len(list)-1]
    else:
        last = list
    return last

# text file
buffer = []
with open(textfile, 'r') as f:
    buffer = f.read()
f.closed

print(buffer)

sn = cleansn(buffer)

print(sn)