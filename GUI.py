"""
Created on Fri Sep  4 16:35:46 2021
GUI
@author: Ray
"""
from utils.utils import *
from shapely.geometry import box
import pandas as pd
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox
import geopandas as gpd
from fiona.crs import from_epsg

# A Interface
class GUI:

    def __init__(self, master):
        
        # Setting
        self.master = master
        self.master.geometry('600x500')
        self.master.resizable(0, 0)
        self.master.title("SOLUTION")
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)
        
        # Filemenu
        self.fileMenu = Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="File", underline=1, menu=self.fileMenu)
        self.fileMenu.add_command(label="Open", underline=1, command=self.openfolder)
        self.fileMenu.add_command(label="Exit", underline=1, command=self.master.destroy)

        # Input box
        self.label1 = Label(self.master, text="Cloud Coverage (smaller than)? (0~100)")
        self.label1.place(x=20, y=325)
        self.inputbox = Entry(self.master)
        self.inputbox.place(x=40, y=350)
        self.label2 = Label(self.master, text="How Many Data? (1~50)")
        self.label2.place(x=20, y=375)
        self.inputbox2 = Entry(self.master)
        self.inputbox2.place(x=40, y=400)
        self.label3 = Label(self.master, text="Top y")
        self.label3.place(x=400, y=325)
        self.inputbox3 = Entry(self.master, width=5)
        self.inputbox3.place(x=400, y=350)
        self.label4 = Label(self.master, text="Right x")
        self.label4.place(x=470, y=360)
        self.inputbox4 = Entry(self.master, width=5)
        self.inputbox4.place(x=470, y=385)
        self.label5 = Label(self.master, text="Left x")
        self.label5.place(x=330, y=360)
        self.inputbox5 = Entry(self.master, width=5)
        self.inputbox5.place(x=330, y=385)
        self.label6 = Label(self.master, text="Buttom y")
        self.label6.place(x=395, y=400)
        self.inputbox6 = Entry(self.master, width=5)
        self.inputbox6.place(x=400, y=425)

        # Button
        self.greet_button = Button(self.master, text="Search Data", command=self.survey)
        self.greet_button.place(x=250, y=460)
        
        # Text
        self.text = Text(self.master)
        self.text.insert(INSERT, "Hello!" + '\n')
        self.text.pack(side='top')
    
    # Survey current image file
    def survey(self):
        cloud_cover = self.inputbox.get()
        data_num = self.inputbox2.get()
        maxy = float(self.inputbox3.get())
        maxx = float(self.inputbox4.get())
        minx = float(self.inputbox5.get())
        miny = float(self.inputbox6.get())
        bbox = box(minx, miny, maxx, maxy)
        bounds = gpd.GeoDataFrame({'geometry': bbox}, index=[0], crs=from_epsg(4326))
        # Check value
        if isfloat(cloud_cover) == False or data_num.isnumeric() == False:
            messagebox.showwarning("Warning", "Invalid Input" )
            
        elif len(cloud_cover) == 0 or len(data_num) == 0:
            messagebox.showwarning("Warning", "Invalid Input" )
            
        else:
            cloud_cover = np.float32(cloud_cover)
            data_num = int(data_num)
        
            if cloud_cover > 100 or cloud_cover < 0 or data_num > 50 or data_num < 1:
                messagebox.showwarning("Warning", "Invalid Input" )
                
            else:
                self.survey_data = data_survey(bounds, cloud_cover, data_num)
                self.surveyed = self.survey_data.find_current_image()
            
                # Check Data
                if len(self.surveyed) == data_num:
                    self.text.insert(INSERT,'\n' + "Current Image Files (Information)")
                    self.text.pack()
                    self.text.insert(INSERT,'\n' + str(self.surveyed.iloc[:,2:5]))
                    self.text.pack()
                    self.newWindow = Toplevel(self.master)
                    self.app = popup(self.newWindow, self.surveyed, self.text, data_num)

                    
                elif len(self.surveyed) > 0 and len(self.surveyed) < data_num:
                    self.text.insert(INSERT,'\n' + "Only found {} Files (Information)".format(len(self.surveyed)) + '\n')
                    self.text.pack()
                    self.text.insert(INSERT,'\n' + str(self.surveyed.iloc[:,2:5]))
                    self.text.pack()
                    self.newWindow = Toplevel(self.master)
                    self.app = popup(self.newWindow, self.surveyed, self.text, data_num)
                    
                else:
                    messagebox.showwarning("Warning", "Found 0 Files" )
        
    # Open folder contain image files
    def openfolder(self):
        
        global check
        check = 1
        self.filename = fd.askdirectory(title="Select Folder")
        if len(self.filename) > 0:
            self.text.insert(INSERT, '\n' + "Folder Loaded")
            self.text.pack()

# Popup window
class popup():
    
    def __init__(self, master, surveyed, text, data_num):
        self.popup = master
        self.surveyed = surveyed
        self.text = text
        self.data_num = data_num
        self.popup.title("Select ONE File or Mutiple Files")
        
        # Variable
        var = list(self.surveyed.iloc[:self.data_num,2])
        var2 = StringVar()
        var2.set(var)
        
        # Scrollbar of listbox
        self.scrollbar = Scrollbar(self.popup)
        self.scrollbar.pack(side="right", fill="y")
        
        # Listbox
        self.listbox = Listbox(self.popup, listvariable=var2, yscrollcommand = self.scrollbar.set, selectmode=EXTENDED)
        self.listbox.pack()

        self.scrollbar.config(command=self.listbox.yview)
        self.down_button = Button(self.popup, text="Download Selected File", command=self.downloader)
        self.down_button.pack()
        
    # Download image file
    def downloader(self):
        index = self.listbox.curselection()
        
        # Check if user click a data
        if len(index) == 0:
            messagebox.showwarning("Warning", "Please Select Files" )
        else:
            for i in index:
                download = []
                download.append(self.surveyed.iloc[i])
                download_frame = pd.concat(download, 1).T
                self.downloaded = data_downloader(download_frame)
                saved_dir = self.downloaded.output_dir()
                self.text.insert(INSERT, '\n' + "Already Downloaded and Saved in: {}".format(saved_dir))
                self.text.pack()

if __name__ == '__main__':
    root = Tk()
    image = GUI(root)
    root.mainloop()