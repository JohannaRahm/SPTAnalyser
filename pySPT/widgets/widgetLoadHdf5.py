# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 09:14:39 2019

@author: Johanna Rahm

Research group Heilemann
Institute for Physical and Theoretical Chemistry, Goethe University Frankfurt a.M.

Handling widgets of trackStatistics JNB.
"""

import tkinter as tk 
import os
import os.path
import tkinter.filedialog as fd
from ipywidgets import widgets
from IPython.display import display
from IPython.display import clear_output
import datetime

class WidgetLoadHdf5():
    def __init__(self):
        # Load cell.h5 files
        #self.data_set_dir = ""  # directory of cell file search
        self.file_names = []  # list of file names for cell files
        self.suffix = ".h5"
        self.dir_button = self.create_dir_button()
        self.dir_box = self.create_dir_box()
        self.dir_name = ""  # input for directory
        self.init_cells_button = self.create_init_cells_button()
        # Load bg.h5 files
        self.init_background_button = self.create_init_background_button()
        self.dir_name_bg = ""  # directory of bg file search
        self.dir_button_bg = self.create_dir_button_bg()
        self.dir_box_bg = self.create_dir_box_bg()
        self.file_names_bg = []  # list of file names for bg files
        self.chosen_cell = ""
        self.cell_options = []  # list of filtered cells for drop down menu
        self.trajectory_options = []  # list of filtered trajectories for drop down menu
        self.drop_down_cells = self.create_drop_down_cells()
        self.drop_down_trajectories = self.create_drop_down_trajectories()
        self.plot_button = self.create_plot_button()
        self.filter_button = self.create_filter_button()
        self.min_length_box = self.create_min_length_box()
        self.min_length = 0  
        self.max_length_box = self.create_max_length_box()
        self.min_D_box = self.create_min_D_box()
        self.max_D_box = self.create_max_D_box()
        self.immob_type_check_box = self.create_immob_type_check_box()
        self.confined_type_check_box = self.create_confined_type_check_box()
        self.free_type_check_box = self.create_free_type_check_box()
        #self.analyse_successful_check_box = self.create_analyse_successful_check_box()
        self.analyse_not_successful_check_box = self.create_analyse_not_successful_check_box()
        self.plot_diffusions_button = self.create_plot_diffusions_button()
        # Calculate the dynamic localization error
        self.calc_sigma_dyn_button = self.create_calc_sigma_dyn_button()
        # Plot diffusion histogram
        self.bin_size_box = self.create_bin_size_box()
        # Save statistics
        self.save_dir_button = self.create_save_dir_button()
        self.save_dir_box = self.create_save_dir_box()
        self.save_name_box = self.create_save_raw_base_name_box()
        self.dir_save = ""
        self.filtered_dataset_checkbox = self.create_filtered_dataset_checkbox()
        self.hmm_trc_checkbox = self.create_hmm_trc_checkbox()
        self.save_button = self.create_save_button()
        self.save_folder_name_box = self.create_save_folder_name_box()
        #self.current_date = ""
    
    def search_sub_folders(self, dir_name, is_cell=True):
        if dir_name:
            for root, dirs, files in os.walk(dir_name):
                self.extend_list(root, files, is_cell)

    def extend_list(self, root, files, is_cell=True):
        for name in files:
            if name.endswith(self.suffix):
                if is_cell:
                    self.file_names.append(os.path.join(root, name))
                else:
                    self.file_names_bg.append(os.path.join(root, name))
                
    def create_dir_button(self):
        """
        Button to load a directory as search platform.
        """
        button = widgets.Button(
                description='browse',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltip='browse for directory')
                #icon='check')
        return button    
    
    def open_dir(self, b):
        root = tk.Tk()
        root.withdraw()
        root.update()
        root.name = fd.askdirectory(initialdir=os.getcwd(),title='Please select a directory') 
        root.update()
        root.destroy()
        self.dir_name = root.name
        self.dir_box.value=self.dir_name
        #self.got_dir = True
        
    def create_dir_box(self, val = "directory to be searched in", desc = "directory"):  # val = in box, desc = infront of box; val = "C:\\Users\\pcoffice37\\Documents\\testing_file_search"
        """
        Box for inserting the directory with description, alternative for dir loading button.
        """
        style = {'description_width': 'initial'}  # display too long desc
        text = widgets.Text(value=str(val), placeholder='Type something', description=str(desc), disabled=False, style = style)
        return text
    
    def change_dir_box(self, change):
        self.dir_name = self.dir_box.value  
        #self.got_dir = True
        
    def create_init_cells_button(self):
        """
        Initialize objects
        """
        button = widgets.Button(
                description='initialize',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltip='initialize objects')
                #icon='check')
        return button    
    
    # Load bg.h5 files
    
    def create_dir_button_bg(self):
        """
        Button to load a directory as search platform.
        """
        button = widgets.Button(
                description='browse',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltip='browse for directory')
                #icon='check')
        return button    
    
    def open_dir_bg(self, b):
        root = tk.Tk()
        root.withdraw()
        root.update()
        root.name = fd.askdirectory(initialdir=os.getcwd(),title='Please select a directory') 
        root.update()
        root.destroy()
        self.dir_name_bg = root.name
        self.dir_box_bg.value = self.dir_name_bg
        #self.got_dir_bg = True
        
    def create_dir_box_bg(self, val = "directory to be searched in", desc = "directory"):  # val = in box, desc = infront of box; val = "C:\\Users\\pcoffice37\\Documents\\testing_file_search"
        """
        Box for inserting the directory with description, alternative for dir loading button.
        """
        style = {'description_width': 'initial'}  # display too long desc
        text = widgets.Text(value=str(val), placeholder='Type something', description=str(desc), disabled=False, style = style)
        return text
    
    def change_dir_box_bg(self, change):
        self.dir_name_bg = self.dir_box_bg.value  
        #self.got_dir_bg = True
    
    def create_init_background_button(self):
        """
        Initialize objects
        """
        button = widgets.Button(
                description='initialize',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltip='initialize objects')
                #icon='check')
        return button  
    
    def create_drop_down_cells(self):
        drop_down_cells = widgets.Dropdown(
                options=self.cell_options,
                description='Number:',
                disabled=False)
        return drop_down_cells
    
    def create_drop_down_trajectories(self):
        drop_down_trajectories = widgets.Dropdown(
                options=self.trajectory_options,
                description='Number:',
                disabled=False)
        return drop_down_trajectories
    
    def get_trajectory_numbers(self, cell, cell_trajectories):
        trajectory_numbers = []
        for trajectory in cell_trajectories[cell]:
            trajectory_numbers.append(trajectory)
        self.drop_down_trajectories.options = trajectory_numbers
        return trajectory_numbers
    
    def get_cell_names(self, cells, filtered_cell_trajectories):
        """
        :param cells: list of cell objects from coverslip.
        :param cell_trajectories_filtered: list with trajectories (for each cell 1 list).
        """
        cell_names = []
        for cell in cells:
            if filtered_cell_trajectories[cells.index(cell)]:  # if cell has trajectory entries 
                cell_names.append(cell.name)
        self.drop_down_cells.options = sorted(cell_names)  # alphabetically sorted
        return sorted(cell_names)
    
    def create_plot_button(self):
        button = widgets.Button(
                description="plot",
                disabled=False,
                button_style="",
                tooltip = "plot chosen trajectory")
        return button
    
    def create_clear_output(self):
        clear_output()
    
    def create_filter_button(self):
        button = widgets.Button(
                description="apply filter",
                disabled=False,
                button_style="",
                tooltip = "apply filter")
        return button
    
    def create_min_length_box(self, val = "min length" , desc = "Trajectory"):  # val = in box, desc = infront of box; val = "C:\\Users\\pcoffice37\\Documents\\testing_file_search"
        """
        Box for inserting the minimum length of a trajectory.
        """
        style = {'description_width': 'initial'}  # display too long desc
        text_min = widgets.Text(value=str(val), placeholder='Type something', description=str(desc), disabled=False, style = style)
        return text_min
    
    def create_max_length_box(self, val = "max length", desc = "Trajectory"):  # val = in box, desc = infront of box; val = "C:\\Users\\pcoffice37\\Documents\\testing_file_search"
        """
        Box for inserting the max length of a trajectory.
        """
        style = {'description_width': 'initial'}  # display too long desc
        text = widgets.Text(value=str(val), placeholder='Type something', description=str(desc), disabled=False, style = style)
        return text
    
    def create_min_D_box(self, val = "min value" , desc = "Diffusion coefficient"):  # val = in box, desc = infront of box; val = "C:\\Users\\pcoffice37\\Documents\\testing_file_search"
        """
        Box for inserting the minimum D value.
        """
        style = {'description_width': 'initial'}  # display too long desc
        text = widgets.Text(value=str(val), placeholder='Type something', description=str(desc), disabled=False, style = style)
        return text
    
    def create_max_D_box(self, val = "max value", desc = "Diffusion coefficient"):  # val = in box, desc = infront of box; val = "C:\\Users\\pcoffice37\\Documents\\testing_file_search"
        """
        Box for inserting the max D value.
        """
        style = {'description_width': 'initial'}  # display too long desc
        text = widgets.Text(value=str(val), placeholder='Type something', description=str(desc), disabled=False, style = style)
        return text
    
    def create_immob_type_check_box(self):
        """
        True -> check box is already selected; False -> check box is not selected.
        """
        checkbox = widgets.Checkbox(value=True,
                         description='Immobile',
                         disabled=False)
        return checkbox
    
    def create_confined_type_check_box(self):
        checkbox = widgets.Checkbox(value=True,
                         description='Confined',
                         disabled=False)
        return checkbox
    
    def create_free_type_check_box(self):
        checkbox = widgets.Checkbox(value=True,
                         description='Free',
                         disabled=False)
        return checkbox

    def create_analyse_not_successful_check_box(self):
        checkbox = widgets.Checkbox(value=False,
                         description='Type determination not successful',
                         disabled=False)
        return checkbox
    
    def create_plot_diffusions_button(self):
        button = widgets.Button(
                description="plot",
                disabled=False,
                button_style="",
                tooltip = "plot diffusion coefficients")
        return button
    
    def create_calc_sigma_dyn_button(self):
        """
        Button to calculate the dynamic localization error.
        """
        button = widgets.Button(
                description='calc',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltip='dynamic localization error')
                #icon='check')
        return button  
    
    # Plot diffusion histogram
    
    def create_bin_size_box(self, val = "0.1" , desc = "bin size"):  # val = in box, desc = infront of box; val = "C:\\Users\\pcoffice37\\Documents\\testing_file_search"
        """
        Box for inserting the bin size for log10(D) histogram.
        """
        style = {'description_width': 'initial'}  # display too long desc
        text = widgets.Text(value=str(val), placeholder='size for log10(D) histogram', description=str(desc), disabled=False, style = style)
        return text
    
    # Save h5 statistics

    def create_save_dir_button(self):
        """
        Button to select directory for saving statistics h5 file.
        """
        button = widgets.Button(
                description='browse',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltip='browse for directory')
                #icon='check')
        return button  
    
    def save_open_dir(self, b):
        root = tk.Tk()
        root.withdraw()
        root.update()
        root.name = fd.askdirectory(initialdir=os.getcwd(),title='Please select a directory') 
        root.update()
        root.destroy()
        self.dir_save = root.name
        self.save_dir_box.value=self.dir_save
        
    def create_save_dir_box(self, val = "", desc = "directory"):  # val = in box, desc = infront of box; val = "C:\\Users\\pcoffice37\\Documents\\testing_file_search"
        """
        Box for inserting the directory with description, alternative for dir loading button.
        """
        style = {'description_width': 'initial'}  # display too long desc
        text = widgets.Text(value=str(val), placeholder='directory for filtered data', description=str(desc), disabled=False, style = style)
        return text
    
    def change_save_dir_box(self, change):
        self.dir_save = self.save_dir_box.value   
    
    def create_save_raw_base_name_box(self, val = "statistics", desc = "file name"):
        """
        Box for inserting the raw base name for statistics h5 file.
        """
        style = {'description_width': 'initial'}  # display too long desc
        text = widgets.Text(value=str(val), placeholder='name for statistics .h5 file', description=str(desc), disabled=False, style = style)
        return text
    
    def calc_date(self):
        now = datetime.datetime.now()
        year = str(now.year)
        year = year[2:]
        month = str(now.month)
        day = str(now.day)
        if len(month) == 1:
            month = str(0) + month
        if len(day) == 1:
            day = str(0) + day
        date = str(year + month + day)
        return date
    
    def create_save_folder_name_box(self, desc = "folder name"):
        """
        Box for inserting the raw base name for statistics h5 file.
        """
        current_date = self.calc_date()
        style = {'description_width': 'initial'}  # display too long desc
        text = widgets.Text(value=str(current_date + "_filtered"), placeholder='name of folder', description=str(desc), disabled=False, style = style)
        return text
        
    def create_filtered_dataset_checkbox(self):
        checkbox = widgets.Checkbox(value=True,
                         description='Save filtered dataset',
                         disabled=False)
        return checkbox
    
    def create_hmm_trc_checkbox(self):
        checkbox = widgets.Checkbox(value=True,
                         description='Save filtered .trc files',
                         disabled=False)
        return checkbox
    
    def create_save_button(self):
        button = widgets.Button(
                description="save",
                disabled=False,
                button_style="",
                tooltip = "save statistics")
        return button

    