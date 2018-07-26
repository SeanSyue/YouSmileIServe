from setuptools import setup

setup(
    name='yousmileiserve',
    version='0.1.0',
    author='seansyue',
    description='A prototype of custom ordering bot with smile activation',

    packages=['', 'menu', 'CamUtils'],
    package_data={
        'menu': ['rice_menu.txt', 'noodle_menu.txt', 'menu_gui.ui']
    },
    entry_points={
        "console_scripts": ['YouSmileIServe = main_service:run_cli',
                            'menu = menu.menu_cli:run_cli'],
        "gui_scripts": ['menu-gui=menu:run_gui']
    },
)
