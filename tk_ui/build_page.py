from os.path import dirname, realpath
from .app import App
from build_s import name as title


path = dirname(realpath(__file__)).replace('\\tk_ui', '')

def start_app(adderer):
    width, height = 350, 500
    assets_path = f'{path}\\assets'
    icon = assets_path + '\\' + 'icon.ico'

    app = App(assets_path, title, width, height, icon, adderer)
    app.mainloop()