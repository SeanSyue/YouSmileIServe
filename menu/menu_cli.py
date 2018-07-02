from os.path import join as join_path
import fire

MENU_PATH = '/home/pi/WORKSPACE/YouSmileIServe/menu'


def remove(menu, meal):
    print(meal)
    with open(join_path(MENU_PATH, '{}_menu.txt'.format(menu)), 'r') as f:
        menu_read = [item.strip() for item in f.readlines()]
    menu_read.remove(meal)
    with open(join_path(MENU_PATH, '{}_menu.txt'.format(menu)), 'w') as f:
        for item in menu_read:
            print(item, file=f)


def add(menu, meal):
    print(meal)
    with open(join_path(MENU_PATH, '{}_menu.txt'.format(menu)), 'r') as f:
        menu_read = [item.strip() for item in f.readlines()]
    menu_read.append(meal)
    with open(join_path(MENU_PATH, '{}_menu.txt'.format(menu)), 'w') as f:
        for item in menu_read:
            print(item, file=f)


def show(menu):
    menu_list = []
    print("===== {} menu ======".format(menu))
    with open(join_path(MENU_PATH, '{}_menu.txt'.format(menu)), 'r') as f:
        for item in [meal.strip() for meal in f.readlines()]:
            # print(item)
            menu_list.append(item)
    # print("\n")
    return menu_list


# def run_cli():
#     fire.Fire({
#         'add': add,
#         'remove': remove,
#         'show': show
#     })

if __name__ == '__main__':
    fire.Fire({
        'add': add,
        'remove': remove,
        'show': show
    })
