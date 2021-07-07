def file_append(file_name):
    from itertools import islice
    with open('abc.txt', 'w') as f:
        f.write('Madina Kazbek\n')
        f.write('KBTU: FIT\n')
        f.write('Python Language\n')
        f.write('Jujutsu Kaisen')
    txt = open(file_name)
    print(txt.read())

file_append('abc.txt')