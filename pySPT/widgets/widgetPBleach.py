# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 17:14:19 2019

@author: Johanna Rahm

Research group Heilemann
Institute for Physical and Theoretical Chemistry, Goethe University Frankfurt a.M.
"""

import tkinter as tk 
from tkinter.filedialog import askopenfilename
from ipywidgets import widgets
from IPython.display import display
from IPython.display import clear_output

class WidgetPBleach():
    def __init__(self):
        self.file_name = ""
        self.got_file_name = False
        self.file_text_box = self.create_file_box()
        self.file_button = self.create_file_button()
        self.run_button = self.create_run_button()
        self.save_button = self.create_save_button()
        self.clear_output = self.create_clear_output()
        self.init_k = self.create_init_k_box()
        self.integration_time = self.create_init_integration_time_box()
        
    def create_file_button(self):
        """
        Button to load the file.
        """
        button = widgets.Button(
                description='browse',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltip='browse for file')
                #icon='check')
        return button

    def open_file(self, b):  # b = ???
        """
        Give the file button opening powers.
        """
        root = tk.Tk()  # window class
        root.withdraw()  # close the window 
        root.update()  # close the window
        root.name = askopenfilename(title="Import tracked.seg file", filetypes=(("text files", "*.txt"),("all files", "*.*")))
        self.file_name = root.name
        root.update()
        root.destroy()
        self.file_text_box.value = self.file_name  # inserts path in box for inserting the path
        self.got_file_name = True
        
    def create_file_box(self, val = "path", desc = "Complete path"):  # val = in box, desc = infront of box
        """
        Box for inserting the path with description, alternative for file loading button.
        """
        style = {'description_width': 'initial'}  # display too long desc
        text = widgets.Text(value=str(val), placeholder='Type something', description=str(desc), disabled=False, style = style)
        return text
    
    def change_file_box(self, change):
        self.file_name = self.file_text_box.value  
        self.got_file_name = True
        
    def create_init_k_box(self, val = "0.01", desc = "Initial k"): 
        """
        Box for inserting the initial k.
        """
        style = {'description_width': 'initial'}  # display too long desc
        text = widgets.Text(value=str(val), placeholder='Type something', description=str(desc), disabled=False, style = style)
        #self.file_name = text.value
        #self.got_file_name = True
        return text
    
    def create_init_integration_time_box(self, val = "0.02", desc = "Camera integration time [s]"):  # val = in box, desc = infront of box
        """
        Box for inserting the integration time in s.
        """
        style = {'description_width': 'initial'}  # display too long desc
        text = widgets.Text(value=str(val), placeholder='Type something', description=str(desc), disabled=False, style = style)
        return text    
        
    def create_run_button(self):
        """
        Button for running the analysis, has an on click event.
        """
        button = widgets.Button(
                description='run',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltip='run the analysis')
                #icon='check')
        return button        

    def create_save_button(self):
        """
        Button to save the results, has an on click event.
        """
        button = widgets.Button(
                description='save',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltip='save the results')
                #icon='check')
        return button    
        
    def create_clear_output(self):
        clear_output()
        
    def warning_file(self):
        print("No file was loaded.")
        
    def warning_columns(self):
        print("A file with false columns was loaded.")
    
    
def main():
    pass
        

if __name__ == "__main__":
    main()
    