from utilpy.vault import Vault


def menu():
    print("______________________________")
    print("| o: create or open database |")
    print("| i: insert/update a register|")
    print("| g: get a register          |")
    print("| l: list registers          |")
    print("| d: delete a register       |")
    print("| x: exit ___________________|")

v = None

shouldExit = False
while not shouldExit:
    menu()
    op = input('\nChoose an option: ')
    if op not in ['o','i','g','l','d','x']:
        print ('Invalid option.')
        continue

    if op == 'o':
        dbName = input('\nEnter a database path/name: ')
        v = Vault(dbName)
        continue

    if op == 'i':
        if v == None:
            print('Please, create a new database first!')
            continue
        key = input('Please, enter the key value: ')
        username = input('Please, enter the username value: ')
        password = input('Please, enter the password value: ')
        v.put(key,username,password)
        print('Register inserted!')
        continue

    if op == 'g':
        if v == None:
            print('Please, create a new database first!')
            continue
        key = input('Please, enter the key value: ')
        k = v.get(key)
        if k == None:
            print('Key not found!')
            continue
        print(f'Username: [{k[0]}], Password: [{k[1]}]')
        continue

    if op == 'l':
        if v == None:
            print('Please, create a new database first!')
            continue
        for k in v.getAll():
            print(f'Key: [{k[0]}], Username: [{k[1]}], Password: [{k[2]}]')
        continue

    if op == 'd':
        if v == None:
            print('Please, create a new database first!')
            continue
        key = input('Please, enter the key value: ')
        print(f'Rows deleted: [{v.delete(key)}]')
        continue

    if op == 'x':
        shouldExit = True
        try:
            v.close()
        except: pass
        