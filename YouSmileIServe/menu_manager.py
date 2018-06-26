import fire


def remove(menu, meal):
    print(meal)
    with open('/home/pi/.config/YouSmileIServe/menu/{}_menu.txt'.format(menu), 'r') as f:
        menu_read = [item.strip() for item in f.readlines()]
    menu_read.remove(meal)
    with open('/home/pi/.config/YouSmileIServe/menu/{}_menu.txt'.format(menu), 'w') as f:
        for item in menu_read:
            f.write(item)


def add(menu, meal):
    print(meal)
    with open('/home/pi/.config/YouSmileIServe/menu/{}_menu.txt'.format(menu), 'r') as f:
        menu_read = [item.strip() for item in f.readlines()]
    menu_read.append(meal)
    with open('/home/pi/.config/YouSmileIServe/menu/{}_menu.txt'.format(menu), 'w') as f:
        for item in menu_read:
            f.write(item + '\n')


def show(menu):
    menulist = []
    print("{} menu , you could order:".format(menu))
    with open('/home/pi/.config/YouSmileIServe/menu/{}_menu.txt'.format(menu), 'r') as f:
        for item in [meal.strip() for meal in f.readlines()]:
            print(item)
            menulist.append(item)
    print("\n")
    return menulist

def run_cli():
    fire.Fire({
        'add': add,
        'remove': remove,
        'show': show
    })
