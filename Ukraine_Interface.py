from Python.libraries import *
from Python.functions import *

from Python.RSS_puller_parser import main as main_rss
from Python.queries import main as main_queries
from Python.mapper import main as main_mapper

#Activar una vez al día
#main_rss()
main_queries()
main_mapper(busq=2, tresh1=10000, tresh2=50000)

WINDOWS = platform.system() == 'Windows'
LINUX = platform.system() == 'Linux'
MAC = platform.system() == 'Darwin'

class BrowserFrame(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.browser = None
        self.bind('<Configure>', self.on_configure)

    def get_window_handle(self):
        if MAC:
            pass
        elif self.winfo_id() > 0:
            return self.winfo_id()
        else:
            raise Exception('Could not obtain window handle!')

    def on_configure(self, event):
        if self.browser is None:
            # create the browser and embed it in current frame
            rect = [0, 0, self.winfo_width(), self.winfo_height()]
            cef_winfo = cef.WindowInfo()
            win_id = self.get_window_handle()
            cef_winfo.SetAsChild(win_id, rect)
            ##################################################################################################################################################################
            #Abrir archivo index de la carpeta mapas/archivos mapas y cambiar la dirección según Chrome
            #Posteriormente pegar dicha URL abajo
            ##################################################################################################################################################################
            self.browser = cef.CreateBrowserSync(cef_winfo, url=fr'file:///home/jj/Documents/Conflict-Mapper/Mapas/archivos%20mapas/index.html')

            # start the browser handling loop
            self.cef_loop()

        # resize the browser
        if WINDOWS:
            ctypes.windll.user32.SetWindowPos(
                self.browser.GetWindowHandle(), 0,
                0, 0, event.width, event.height, 0x0002)
        else:
            pass

    def cef_loop(self):
        cef.MessageLoopWork()
        self.after(10, self.cef_loop)

    def restart(self):
        self.refresh()
        self.controller.show_frame("StartPage")

    def refresh(self):
        self.weight_entry.delete(0, "end")
        self.text.delete("1.0", "end")

class noticiero(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.actualizar_noticia_en_frame()

    def get_noticia_random(self):
        noticias=cargar_noticias()
        self.longitud_noticias=noticias.shape[0]
        self.noticia_random=randint(0,self.longitud_noticias)
        self.titulo_noticia=noticias.iloc[self.noticia_random]['title']
        self.descripcion_noticia=noticias.iloc[self.noticia_random]['description']

    def actualizar_noticia_en_frame(self):
        self.get_noticia_random()        

        self.titulo = tk.Label(self,text=self.titulo_noticia,justify="left",wraplength=1920)
        self.titulo.configure(font=("Lato black",25))
        self.titulo.grid(row=0, sticky="nws",padx=40, pady=(20,10))

        self.descripcion = tk.Label(self,text=self.descripcion_noticia,justify="left",wraplength=1920)
        self.descripcion.configure(font=("Lato light",14))
        self.descripcion.grid(row=1, sticky="nws",padx=40, pady=(10,20))

class mapper(tk.Tk):
    def __init__(self):
        super().__init__()

        ############################################################################
        #Config basica
        ############################################################################

        self.title('Ukranian News Mapper')
        self.geometry('1920x1080')
        #self.iconbitmap(fr'./icon.ico')

        ############################################################################
        #Menu de control
        ############################################################################

        menu = tk.Menu(self)
        self.config(menu=menu, padx=10,pady=10)

        fileMenu = tk.Menu(menu,tearoff=0)
        menu.add_cascade(label="Opciones", menu=fileMenu)
        fileMenu.add_command(label="Actualizar noticias", command=self.update_noticias)
        fileMenu.add_command(label="Salir", command=self.quit)

        ############################################################################
        #Frames
        ############################################################################

        #Crear topframe

        self.topframe = tk.Frame(self) #Sección que agrupa navegador y controles
        self.topframe.grid(row=0, sticky='news')

        #Crear bottomframe

        self.bottomframe = tk.Frame(self) #Noticias que se cargan  de clase csv_plotter
        self.bottomframe.grid(row=1, sticky='news', padx=20, pady=20)

        #Crear sección controles

        self.frame_controles = tk.Frame(self.topframe) #Controles
        self.frame_controles.grid(row=0, column=0, sticky='news', padx=10, pady=10)

        #Crear sección browser

        self.home_browser = tk.Frame(self.topframe) #Espacio para meter navegador
        self.home_browser.grid(row=0, column=1, sticky='news', pady=10, padx=10)

        #Meter browser en home_browser
    
        self.browser = BrowserFrame(self.home_browser) #Crea navegador
        self.browser.grid(row=0, column=0, sticky=('news'))

        #Meter frame noticiero en bottom

        self.frame_noticias=tk.Frame(self.bottomframe)
        self.frame_noticias.grid(row=0, column=0, sticky=('news'))

        ############################################################################
        #Pesos
        ############################################################################

        #Configurar columnas base

        #'''
        self.columnconfigure(0, weight=1) #Solo 1 columna
        self.rowconfigure(0, weight=5)    #Columan superior más ancha que inferior
        self.rowconfigure(1, weight=1)    #Columna inferior mitad de superior
        #'''

        #Configurar pesos topframe

        #'''
        self.topframe.columnconfigure(0, weight=0) #Columna left con peso de 2
        self.topframe.columnconfigure(1, weight=3) #Columna right con peso de 5
        self.topframe.rowconfigure(0, weight=1)    #Fila 0 con peso de 1
        self.topframe.rowconfigure(1, weight=0)    #Fila 1 sin peso
        #'''

        #Configurar pesos bottomframe

        #'''
        self.bottomframe.columnconfigure(0, weight=1) #Columna left con peso de 2
        self.bottomframe.columnconfigure(1, weight=0) #Columna right con peso de 5
        self.bottomframe.rowconfigure(0, weight=3)    #Fila 0 con peso de 1
        self.bottomframe.rowconfigure(1, weight=1)    #Fila 1 sin peso
        #'''

        #Configurar pesos frame controles

        #'''
        self.frame_controles.columnconfigure(0, weight=1) #Columna left con peso de 2
        self.frame_controles.rowconfigure(0, weight=1)
        self.frame_controles.rowconfigure(1, weight=1)
        self.frame_controles.rowconfigure(2, weight=1)
        self.frame_controles.rowconfigure(3, weight=1)
        self.frame_controles.rowconfigure(4, weight=1)
        self.frame_controles.rowconfigure(5, weight=1)
        self.frame_controles.rowconfigure(6, weight=1)
        #'''

        #Configurar pesos navegador

        #'''
        self.home_browser.columnconfigure(0, weight=1) #Todo el peso dentro de componente navegador
        self.home_browser.rowconfigure(0, weight=1)    #Todo el peso dentro de componente navegador
        #'''

        ############################################################################
        #Elementos control
        ############################################################################

        #Titulo sección

        self.titulo=tk.Label(self.frame_controles, text='Menu de control')
        self.titulo.config(fg="Black", font=("Lato black",20))
        self.titulo.grid(row=0, padx=40, sticky="ew")

        #Texto de acompañamiento titulo

        self.label_desplegable=tk.Label(self.frame_controles, text='Escoja en el desplegable de abajo la visualización que desea hacer:')
        self.label_desplegable.config(fg="Black", font=("Lato light",12))
        self.label_desplegable.grid(row=1, padx=40,sticky="ew")

        #Desplegable de modo de uso

        self.opciones_menu = tk.StringVar(self.frame_controles)
        OPCIONES = ["Noticias","Población"]
        self.opciones_menu.set("Escoja aquí el método")

        self.menu_desplegable = tk.OptionMenu(self.frame_controles, self.opciones_menu, *OPCIONES)
        self.menu_desplegable.grid(row=2, padx=40, sticky="ew")

        #Confirmar modo de búsqueda

        self.boton_confirmar_metodo_busqueda = tk.Button(self.frame_controles, text='Confirmar método', command=self.confirmar_modo_búsqueda, height=1)
        self.boton_confirmar_metodo_busqueda.grid(row=3, padx=300, sticky="ew")

        ############################################################################
        #Mostrar noticias
        ############################################################################

        self.noticia_noticiero = noticiero(self.frame_noticias)
        self.noticia_noticiero.grid(row=0, sticky="nw")

        self.boton_actualizar_noticia = tk.Button(self.bottomframe, text='Actualizar noticia', command=self.update_noticia_noticiero, height=1)
        self.boton_actualizar_noticia.grid(row=1, sticky="ew")

    def update_noticias(self):
        main_rss()

    def refresh(self):
        if self.browser is not None:
            self.browser.destroy()

        #Esto vuelve a crear el navegador

        self.browser = BrowserFrame(self.home_browser) #Crea navegador
        self.browser.grid(row=0, column=0, sticky=('news'))

    def confirmar_modo_búsqueda(self):

        selector=self.opciones_menu.get()
        if selector=='Noticias':
            opcion=1
            self.sliders=tk.Frame(self.frame_controles)
            self.sliders.grid(row=5, column=0, sticky=('news'), padx=40)

            self.sliders.columnconfigure(0, weight=1) #Columna left con peso de 2
            self.sliders.columnconfigure(1, weight=1) #Columna right con peso de 5
            self.sliders.rowconfigure(0, weight=1)    #Fila 0 con peso de 1
            self.sliders.rowconfigure(1, weight=1)    #Fila 1 sin peso

            self.texto_sliders=tk.Label(self.frame_controles, text='Determine los límites inferiores y superiores para las búsquedas:')
            self.texto_sliders.config(fg="Black", font=("Lato light",12))
            self.texto_sliders.grid(row=4,pady=(0,20))

            self.lv=tk.IntVar()

            self.lowerval=tk.Scale(self.sliders, variable=self.lv, from_=0, to=100, orient='horizontal',label="Límite inferior:")
            self.lowerval.grid(row=1,column=0, sticky="news",padx=(0,10),pady=(10,10))

            self.hv=tk.IntVar()

            self.higherval=tk.Scale(self.sliders, variable=self.hv, from_=0, to=100, orient='horizontal',label="Límite superior:")
            self.higherval.grid(row=1,column=1, sticky="news",padx=(10,0),pady=(10,10))

        elif selector=='Población':
            opcion=2
            self.sliders=tk.Frame(self.frame_controles)
            self.sliders.grid(row=5, column=0, sticky=('news'), padx=40)

            self.sliders.columnconfigure(0, weight=1) #Columna left con peso de 2
            self.sliders.columnconfigure(1, weight=1) #Columna right con peso de 5
            self.sliders.rowconfigure(0, weight=1)    #Fila 0 con peso de 1
            self.sliders.rowconfigure(1, weight=1)    #Fila 1 sin peso

            self.texto_sliders=tk.Label(self.frame_controles, text='Determine los límites inferiores y superiores para las búsquedas:')
            self.texto_sliders.config(fg="Black", font=("Lato light",12))
            self.texto_sliders.grid(row=4,pady=(0,20))

            self.lv=tk.IntVar()

            self.lowerval=tk.Scale(self.sliders, variable=self.lv, from_=0, to=5000000, orient='horizontal',label="Límite inferior:")
            self.lowerval.grid(row=1,column=0, sticky="news",padx=(0,10),pady=(10,10))

            self.hv=tk.IntVar()

            self.higherval=tk.Scale(self.sliders, variable=self.hv, from_=0, to=5000000, orient='horizontal',label="Límite superior:")
            self.higherval.grid(row=1,column=1, sticky="news",padx=(10,0),pady=(10,10))

        else:
            print('Opción inexistente')

        def sel():
            lower_tresh = self.lv.get()
            higher_tresh = self.hv.get()
            return lower_tresh,higher_tresh

        def recargar_mapa():
            lt,ht=sel()
            main_mapper(busq=opcion, tresh1=lt, tresh2=ht)

            self.refresh()

        button = tk.Button(self.frame_controles, text="Generar mapa", command=recargar_mapa)
        button.grid(row=6, padx=300, pady=(40,0), sticky="ew")

    def update_noticia_noticiero(self):

        self.noticia_noticiero.destroy()
        self.noticia_noticiero = noticiero(self.frame_noticias) #Crea navegador
        self.noticia_noticiero.grid(row=0, sticky="nw")

def main():

    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize()
    root = mapper()
    root.mainloop()
    cef.Shutdown()

if __name__ == '__main__':
    main()