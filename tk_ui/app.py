from customtkinter import CTk, CTkFont, CTkButton, CTkFrame, CTkLabel, CTkImage, CTkScrollableFrame, CTkButton, CTkToplevel, set_appearance_mode, filedialog
from PIL.Image import open as image_open 
from tktooltip import ToolTip

#import ctypes
#scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)/100

from os.path import exists


def prepare_nets(text:str) -> list:
    text = text.strip().replace(' ', '')
    
    chars = [';', ',', '\n']
    for c in chars:
        if c in text: return text.split(c)
    return []

def read_nets() -> list:
    filename = 'nets.txt'
    if exists(filename):
        with open(filename) as f:
            text = f.read()
            return prepare_nets(text)
    else: return []



class App(CTk):
    set_appearance_mode('dark')
    
    TIP = '''
    Внимание!!!
    Если параметры прокси-сетей были открыты, то результат не появится,
    необхоидимо закрыть и снова открыть данные параметры.
    '''

    def __init__(self, assets_path:str, title:str, width:int, height:int, icon:str, adderer):
        super().__init__()
        self.assets_path = assets_path
        self.title(title)
        #screenwidth = self.winfo_screenwidth()
        #screenheight = self.winfo_screenheight()
        #geometry = '%dx%d+%d+%d' % (width, height, int((screenwidth - width) / 2*scaleFactor), int((screenheight - height) / 2*scaleFactor))
        geometry = f'{width}x{height}'
        self.geometry(geometry)
        self.wm_iconbitmap(icon)
        self.resizable(width=False, height=False)
        
        self.adresses_list = read_nets()
        self.ads = AddressList(self, self.adresses_list)
        
        def choice_file_with_addresses():
            
            title = 'Выберите файл с адресами'
            file_types = [("Адреса", "*")]
            f = filedialog.askopenfile(title=title, filetypes=file_types)
            
            if f != None:
                text = f.read()
                self.adresses_list = prepare_nets(text)
                check_btn()
                self.ads.update_adresses(self.adresses_list)
                self.ads.unbind()
                self.ads.pack(expand=True,fill='both', padx=10, pady=(10, 0))
                self.update_idletasks()
                f.close()

        def save_exceptions():
            adderer.save_proxy_exeptoins(self.adresses_list)


        folder_icon_img = image_open(self.__get_path('folder_icon.png'));
        folder_icon = CTkImage(light_image=folder_icon_img, dark_image=folder_icon_img, size=(10,10))
        self.open_file_btn = CTkButton(self, text='Выбрать файл с адресами', hover_color='purple', image=folder_icon, command=choice_file_with_addresses, width=0)
        self.set_btn = CTkButton(self, text='Добавить в исключение', command=save_exceptions, hover_color='purple', width=0)
        
        ToolTip(self.set_btn, msg=self.TIP, delay=0.02,
        parent_kwargs={"bg": "purple", "padx": 2, "pady": 2},
        fg="#ffffff", bg="#1c1c1c", padx=10, pady=10)
        
        def check_btn():    
            if not self.adresses_list: 
                self.set_btn.configure(state='disabled')
            else:
                self.set_btn.configure(state='normal')

        if self.adresses_list:
            self.ads.pack(expand=True,fill='both', padx=10, pady=(10, 0))
            
        self.clue_window = None
            
        def open_toplevel():
            if self.clue_window is None or not self.clue_window.winfo_exists():
                self.clue_window = ClueWindow(self, header=self.clue_title, icon_path=icon)
                self.clue_window.focus()
            else:
                self.clue_window.focus()  
        
        self.clue_title = 'Об автоматике'
        self.clue_btn = CTkButton(self, text=self.clue_title, command=open_toplevel, hover_color='purple', width=0)
        
        self.clue_btn.pack(fill='both', padx=10, pady=(5, 10), side='bottom')
        
        check_btn()
        self.set_btn.pack(fill='both', padx=10, pady=5, side='bottom')
        self.open_file_btn.pack(fill='both', padx=10, pady=5, side='bottom')
        
        
        
    def __get_path(self, file):
        return f"{self.assets_path}\\{file}".replace('\\', '/')
    
class AddressList(CTkFrame):
    
    TITLE = 'Адреса'
    
    def __init__(self, master, addresses:list):
        super().__init__(master=master, corner_radius=5)
        self.addresses = addresses   
        self.scroll_list = CTkScrollableFrame(self, label_text=self.TITLE, label_fg_color='purple')
        self.scroll_list.pack(expand=True, fill='both')
        self.build_list()
    
    def update_adresses(self, addresses):
        self.addresses = addresses
        self.clear_list()
        self.build_list()
        self.update_idletasks()
    
    def build_list(self):
        self.controls=[
            CTkLabel(self.scroll_list, text=address, width=5) for address in self.addresses
        ] 
        
        for i, control in enumerate(self.controls):
            control.grid(padx=10, pady=5, row=i, column=0, sticky='w')
            
    def clear_list(self):
        for c in self.controls:
            c.destroy()
            
class ClueWindow(CTkToplevel):
    
    CLUE = '''
    Для автоматической загрузки адресов при входе 
    приложите к программе файл nets.txt.
    В нём должны быть перечислены адреса 
    через указанные символы: [';', ',', '\\n(абзац)'].
    Допускаются пробелы: 
    vk.com, yandex.ru  
    vk.com; yandex.ru и т. д.
    '''
    
    def __init__(self, master, header, icon_path):
        super().__init__(master=master)
        width, height = 400, 200
        geometry = f'{width}x{height}'
        # screenwidth = self.winfo_screenwidth()
        # screenheight = self.winfo_screenheight()
        # geometry = '%dx%d+%d+%d' % (width, height, int((screenwidth - width) / 2*scaleFactor), int((screenheight - height) / 2*scaleFactor))
        self.geometry(geometry)
        self.resizable(width=False, height=False)
        self.title(header)
        self.after(200, lambda:  self.iconbitmap(icon_path))
       
        self.clue_text = CTkLabel(self, text=self.CLUE, anchor='e', width=200, justify='left', font=CTkFont(size=15))
        self.clue_text.pack(padx=5, pady=5)