# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 14:38:40 2019

@author: pcoffice37

Research group Heilemann
Institute for Physical and Theoretical Chemistry, Goethe University Frankfurt a.M.
"""

import h5py
import numpy as np
import pandas as pd
import os


class LoadHdf5():
    def __init__(self):
        self.file_names = []  # coverslip.cell_files, list with full path file names in loading order
        self.names = []  # cell.name, raw base name of file, has to be distributed to indiv cells
        self.hdf5 = []  # list of xxx objects
        self.trajectory_numbers = []  # amount of trajectories per cell
        self.cell_numbers = 0  # amount of cells
        self.cell_sizes = []  # list of cell sizes -> cell.size
        self.tau_min_trajectory_lengths = []
        self.pixel_sizes = []  # list of pixel sizes -> cell.pixel_size
        self.pixel_amounts = []  # list of amount of pixel of detector -> cell.pixel_amount
        self.dts = []  # integration times -> trajectory.dt
        self.tau_thresholds = []  # -> trajectory.tau_threshold
        self.fit_areas = []  # -> trajectory.fit_area
        self.dofs = []  # -> trajectory.dof
        self.D_mins = []  # -> trajectory.D_min
        # diffusion infos
        self.cells_lengths_trajectories = []  # 
        self.cells_lengths_MSDs = []  # 
        self.cells_trajectories_D = []  #trajectory.D
        self.cells_trajectories_dD = []  # trajectory.dD
        self.cells_trajectories_MSD0 = []  # trajectory.MSD_0
        self.cells_trajectories_chi2_D = []  # trajectory.chi_D
        self.cells_trajectories_number = []  # trajectory.trajectory_number
        # rossier statistics
        self.cells_trajectories_tau = []  # trajectory.tau
        self.cells_trajectories_dtau = []  # trajectory.dtau
        self.cells_trajectories_r = []  # traujectoty.r
        self.cells_trajectories_dr = []  # trajectory.dr
        self.cells_trajectories_Dconf = []  # trajectory.D_conf
        self.cells_trajectories_chi2_rossier = []  # trajectory.dD_conf
        self.cells_trajectories_analyse_successful = []  # trajectory.analyse_successful
        self.cells_trajectories_type = []
        #
        self.cells_trajectories_MSD_fit = []  # trajectory.MSD_fit col0 = dt, col1 = MSD, col2 = fit, col3 = res 
        self.cells_trajectories_MSD_D = []  # trajectory.MSD_D col0 = dt, col1 = MSD, col2 = fit, col3 = res of first 4 values
        self.cells_trajectories_MSDs = []  # trajectory.MSDs
        self.cells_trajectories_times = []  # trajectories.times
        self.trc_files = []  # cell.trc_file
        self.locs = []  # 
        #
        self.cells = []  # list of cell objects ->cover_slip.cells -> needs entire list
        
    def test_create_file_names(self):
        file_name01 = "C:\\Users\\pcoffice37\\Documents\\testing_file_search\\cells\\cell_1_MMStack_Pos0.ome_MIA.h5"
        file_name02 = "C:\\Users\\pcoffice37\\Documents\\testing_file_search\\cells\\subdirectory\\cell_2_MMStack_Pos0.ome_MIA.h5"
        self.file_names.append(file_name01)
        self.file_names.append(file_name02)
        
    def read_h5(self):
        for file_name in self.file_names:
            h5_file = h5py.File(file_name, "r")
            self.hdf5.append(h5_file)
            
    def count_trajectory_numbers(self):
        """
        Create list with numbers of trajectories for each cell [int, int ...].
        """
        for h5 in self.hdf5:
            diffusion_group = h5["diffusion"]
            diffusion_infos_data = diffusion_group["diffusionInfos"].value
            self.trajectory_numbers.append(np.shape(diffusion_infos_data)[0])
        #print(self.trajectory_numbers)

    def count_cells(self):
        """
        Number of cells that were loaded.
        """
        self.cell_numbers = len(self.hdf5)
        
    def get_cell_name(self):
        """
        From a list of paths create the raw base names list.
        """
        for cell in self.file_names:
            base_name = os.path.basename(cell)
            raw_base_name = ""
            for i in base_name:
                if i == ".":
                    break
                else:
                    raw_base_name += i   
            self.names.append(raw_base_name)
        #print("names", self.names)
           
    def settings(self):
        """
        Handling pixel size & amount.
        """
        for h5 in self.hdf5:
            settings_group = h5["settings"]
            settings_data = settings_group["settings"].value  # [[(0.02, 158, 65536, 0.12, 0.6, 4, 0.0065)]]
            self.dts.append(settings_data[0][0][0])
            self.pixel_sizes.append(settings_data[0][0][1])
            self.pixel_amounts.append(settings_data[0][0][2])
            self.cell_sizes.append(settings_data[0][0][3])
            self.tau_thresholds.append(settings_data[0][0][4])
            self.tau_min_trajectory_lengths.append(settings_data[0][0][5])
            self.fit_areas.append(settings_data[0][0][6])
            self.dofs.append(settings_data[0][0][7])
            self.D_mins.append(settings_data[0][0][8])
        #print("settings", self.dts, self.pixel_sizes, self.pixel_amounts, self.tau_thresholds, self.fit_areas, self.dofs, self.D_mins)
        
    def create_np_array(self, length, columns=1):
        """
        :param length: number of np arrays.
        :param columns: amount of entries in a numpy array.
        :return: return a numpy array.
        """
        np_array = np.zeros((length,columns))
        return np_array
        
    def get_diffusion_infos3(self):     
        """
        As np.array.
        """
        for h5 in self.hdf5:
            h5_index = self.hdf5.index(h5)
            max_trajectory_index = self.trajectory_numbers[h5_index]
            diffusion_group = h5["diffusion"]
            diffusion_infos_data = diffusion_group["diffusionInfos"].value
            length_trajectories = self.create_np_array(max_trajectory_index)
            length_MSDs = self.create_np_array(max_trajectory_index)
            for trajectory_index in range(0, max_trajectory_index):
                length_trajectory = diffusion_infos_data[trajectory_index][5]
                length_trajectories[trajectory_index] = length_trajectory
                length_MSDs[trajectory_index] = length_trajectory - 1
            self.cells_lengths_trajectories.append(length_trajectories)
            self.cells_lengths_MSDs.append(length_MSDs)
        #print(self.cells_lengths_trajectories)
        
    def get_diffusion_infos(self):     
        """
        Handling length_MSD, length_trajectory, id, D, dD, MSD_0, chi2.
        
        As np.array. -> x[cell][trajectory][0] 
        """
        for h5 in self.hdf5:
            h5_index = self.hdf5.index(h5)
            max_trajectory_index = self.trajectory_numbers[h5_index]
            diffusion_group = h5["diffusion"]
            diffusion_infos_data = diffusion_group["diffusionInfos"].value
            lengths_trajectories = self.create_np_array(max_trajectory_index)
            lengths_MSDs = self.create_np_array(max_trajectory_index)
            trajectories_number = self.create_np_array(max_trajectory_index)
            trajectories_diffusion = self.create_np_array(max_trajectory_index)
            trajectories_ddiffusion = self.create_np_array(max_trajectory_index)
            trajectories_MSD_0 = self.create_np_array(max_trajectory_index)
            trajectories_chi_D = self.create_np_array(max_trajectory_index)
            for trajectory_index in range(0, max_trajectory_index):
                length_trajectory = diffusion_infos_data[trajectory_index][5]
                lengths_trajectories[trajectory_index] = length_trajectory
                length_MSD = length_trajectory - 1
                lengths_MSDs[trajectory_index] = length_MSD
                diffusion = diffusion_infos_data[trajectory_index][1]
                trajectories_diffusion[trajectory_index] = diffusion
                ddiffusion = diffusion_infos_data[trajectory_index][2]
                trajectories_ddiffusion[trajectory_index] = ddiffusion
                MSD_0 = diffusion_infos_data[trajectory_index][3]
                trajectories_MSD_0[trajectory_index] = MSD_0
                chi_D = diffusion_infos_data[trajectory_index][4]
                trajectories_chi_D[trajectory_index] = chi_D
                number = diffusion_infos_data[trajectory_index][0]
                trajectories_number[trajectory_index] = number
            self.cells_trajectories_chi2_D.append(trajectories_chi_D)
            self.cells_trajectories_D.append(trajectories_diffusion)
            self.cells_trajectories_dD.append(trajectories_ddiffusion)
            self.cells_trajectories_number.append(trajectories_number)
            self.cells_trajectories_MSD0.append(trajectories_MSD_0)
            self.cells_lengths_trajectories.append(lengths_trajectories)
            self.cells_lengths_MSDs.append(lengths_MSDs)
        #print(self.cells_lengths_trajectories)
        #print(self.cells_lengths_trajectories[1][0][0])
        
    def get_rossier_statistics(self):
        """
        Handling immob type, tau, dtau, r, dr, d_conf, chi2.
        
        As np.arrays.
        """
        for h5 in self.hdf5:
            h5_index = self.hdf5.index(h5)
            max_trajectory_index = self.trajectory_numbers[h5_index]
            rossier_group = h5["rossier"]
            rossier_statistics_data = rossier_group["rossierStatistics"]
            trajectories_analyse_successful = self.create_np_array(max_trajectory_index)
            trajectories_tau = self.create_np_array(max_trajectory_index)
            trajectories_dtau = self.create_np_array(max_trajectory_index)
            trajectories_r = self.create_np_array(max_trajectory_index)
            trajectories_dr = self.create_np_array(max_trajectory_index)
            trajectories_dconf = self.create_np_array(max_trajectory_index)
            trajectories_chi_msd = self.create_np_array(max_trajectory_index)
            trajectories_type = self.create_np_array(max_trajectory_index, 3)
            for trajectory_index in range(0, max_trajectory_index):
                trajectory_immob = rossier_statistics_data[trajectory_index][1]  # immob
                trajectory_confined = rossier_statistics_data[trajectory_index][2]  # confined
                trajectory_free = rossier_statistics_data[trajectory_index][3]  # free
                analyse_successful = rossier_statistics_data[trajectory_index][4]
                tau = rossier_statistics_data[trajectory_index][5]
                dtau = rossier_statistics_data[trajectory_index][6]
                r = rossier_statistics_data[trajectory_index][7]
                dr = rossier_statistics_data[trajectory_index][8]
                dconf = rossier_statistics_data[trajectory_index][9]
                chi_msd = rossier_statistics_data[trajectory_index][10]
                trajectories_type[trajectory_index][0] = trajectory_immob
                trajectories_type[trajectory_index][1] = trajectory_confined
                trajectories_type[trajectory_index][2] = trajectory_free
                trajectories_analyse_successful[trajectory_index] = analyse_successful
                trajectories_tau[trajectory_index] = tau
                trajectories_dtau[trajectory_index] = dtau
                trajectories_r[trajectory_index] = r
                trajectories_dr[trajectory_index] = dr
                trajectories_dconf[trajectory_index] = dconf
                trajectories_chi_msd[trajectory_index] = chi_msd
            self.cells_trajectories_analyse_successful.append(trajectories_analyse_successful)
            self.cells_trajectories_tau.append(trajectories_tau)
            self.cells_trajectories_dtau.append(trajectories_dtau)
            self.cells_trajectories_r.append(trajectories_r)
            self.cells_trajectories_dr.append(trajectories_dr)
            self.cells_trajectories_Dconf.append(trajectories_dconf)
            self.cells_trajectories_chi2_rossier.append(trajectories_chi_msd)
            self.cells_trajectories_type.append(trajectories_type)

    def get_MSDs(self):
        """
        Handle full dt & MSD values.
        [[nparray, nparray][nparray]] each list is a cell, that contains np arrays
        of different lengh for each trajectory.
        """
        for h5 in self.hdf5:
            h5_index = self.hdf5.index(h5)
            max_trajectory_index = self.trajectory_numbers[h5_index]
            MSD_group = h5["MSD"]
            cell_trajectories_MSDs = []
            cell_trajectories_times = []
            for trajectory_index in range(0, max_trajectory_index):
                trajectory_key = "Trajectory" + self.trajectory_number_set_digits(trajectory_index)
                trajectory_data = MSD_group[trajectory_key].value
                MSDs = np.zeros(len(trajectory_data))
                times = np.zeros(len(trajectory_data))
                for duration in range(0, len(trajectory_data)):
                    MSDs[duration] = trajectory_data[duration][1]  # MSDs
                    times[duration] = trajectory_data[duration][0]  # dt
                cell_trajectories_MSDs.append(MSDs)
                cell_trajectories_times.append(times)
            self.cells_trajectories_times.append(cell_trajectories_times)
            self.cells_trajectories_MSDs.append(cell_trajectories_MSDs)
        
    def get_trcs(self):
        """
        Create a trc file as np arrays for each cell. Do I even need it? Wrong unit.
        """
        for h5 in self.hdf5:
            h5_index = self.hdf5.index(h5)
            trc_group = h5["trc"]
            trc_group_data = trc_group["trcFile"].value
            max_index = np.shape(trc_group_data)[0]
            trc = self.create_np_array(np.shape(trc_group_data)[0], 6)
            for i in range(0, max_index):
                trc[i,0] = trc_group_data[i][0]  # trajectory id
                trc[i,1] = trc_group_data[i][1]  # frame
                trc[i,2] = trc_group_data[i][2]  # x position
                trc[i,3] = trc_group_data[i][3]  # y position
                trc[i,4] = trc_group_data[i][4]  # place holder
                trc[i,5] = trc_group_data[i][5]  # intensity
            self.trc_files.append(trc)
        #print(self.trc_files)
        
    def get_rossier_plots(self):
        for h5 in self.hdf5:
            h5_index = self.hdf5.index(h5)
            max_trajectory_index = self.trajectory_numbers[h5_index]
            rossier_group = h5["rossier"]
            rossier_plots_group = rossier_group["rossierPlots"]
            cell_trajectories = []
            for trajectory_index in range(0, max_trajectory_index):
                rossier_plot_key = "rossierPlot" + self.trajectory_number_set_digits(trajectory_index)
                rossier_plot_data = rossier_plots_group[rossier_plot_key].value
                MSD_fit = self.create_np_array(len(rossier_plot_data), 4)
                for duration in range(0, len(rossier_plot_data)):
                    MSD_fit[duration,0] = rossier_plot_data[duration][0]  # dt
                    MSD_fit[duration,1] = rossier_plot_data[duration][1]  # MSD
                    MSD_fit[duration,2] = rossier_plot_data[duration][2]  # fit
                    MSD_fit[duration,3] = rossier_plot_data[duration][3]  # residues
                cell_trajectories.append(MSD_fit)
            self.cells_trajectories_MSD_fit.append(cell_trajectories)
        #print(self.cells_trajectories_MSD_fit[0][0][:,1])
                    
    def get_diffusion_plots(self):
        for h5 in self.hdf5:
            h5_index = self.hdf5.index(h5)
            max_trajectory_index = self.trajectory_numbers[h5_index]
            diffusion_group = h5["diffusion"]
            diffusion_plots_group = diffusion_group["diffusionPlots"]
            cell_trajectories = []
            for trajectory_index in range(0, max_trajectory_index):
                diffusion_plot_key = "diffusionPlot" + self.trajectory_number_set_digits(trajectory_index)
                diffusion_plot_data = diffusion_plots_group[diffusion_plot_key].value
                MSD_D = self.create_np_array(len(diffusion_plot_data), 4) 
                for duration in range(0, len(diffusion_plot_data)):
                    MSD_D[duration,0] = diffusion_plot_data[duration][0]  # dt
                    MSD_D[duration,1] = diffusion_plot_data[duration][1]  # MSD
                    MSD_D[duration,2] = diffusion_plot_data[duration][2]  # fit
                    MSD_D[duration,3] = diffusion_plot_data[duration][3]  # residues
                cell_trajectories.append(MSD_D)
            self.cells_trajectories_MSD_D.append(cell_trajectories)
                    
    def trajectory_number_set_digits(self, trajectory_index, number_of_digits=4):
        """
        :param trajectory_index: Index will be +1 and turned to str
        :param number_of_digits: Default 4, trajectory number will be presented with 4 digits -> 0001.
        :return: trajectory number a str.
        """
        trajectory_number = str(trajectory_index+1)
        while len(trajectory_number) < number_of_digits:
            trajectory_number = "0" + trajectory_number 
        return trajectory_number  
    
    def get_locs(self):
        """
        For each trajectory locs will be created (np.array with col0 = molecule, col1 = frames, col2 = x, col3 = y, col4 = -1, col5 = intensity)
        Each cell equals a list. 
        """
        for trc_file in self.trc_files:
            one_cell = []
            for trajectory_number in range(int(trc_file[:,0].min()), int(trc_file[:,0].max())+1):
                idx = trc_file[:,0] == trajectory_number
                localizations = trc_file[idx,:]
                if not (localizations.size == 0):
                    one_cell.append(localizations)
            self.locs.append(one_cell)
                
    def run_load_hdf5(self):
        self.read_h5()
        self.get_cell_name()
        self.count_trajectory_numbers()
        self.count_cells()
        self.settings()
        self.get_diffusion_infos()
        self.get_diffusion_plots()
        self.get_rossier_statistics()
        self.get_rossier_plots()
        self.get_MSDs()
        self.get_trcs()
        self.get_locs()
        
#file = h5py.File(self.file_names[0], "r")
#print(file.keys())
#keys = [key for key in file.keys()]
#print(keys)
#group = file["rossier"]
#print(group)
#for key in group.keys():
#print(key)
        
#print(h5.get("/size/size"))
#print(type(h5.get("/size/size")))
#df = h5.get("/size/size")
#print(df.columns)         
#df = h5.get("/diffusion/diffusion plots/diffusion plot 0001")
#print(df)
#print(df.keys())
#print(type(df.values))            
#data_frame_size = h5.get("size/size")         
#df.frame["size [\u03BCm\u00b2]"]
#print(self.hdf5[0].keys())
        

def main():
    load_h5 = LoadHdf5()
    load_h5.test_create_file_names()
    load_h5.read_h5()
    load_h5.get_cell_name()
    load_h5.count_trajectory_numbers()
    load_h5.count_cells()
    load_h5.get_cell_size()
    load_h5.settings()
    #load_h5.create_np_array(10)
    load_h5.get_diffusion_infos2()
    load_h5.get_rossier_statistics()
    load_h5.rossier_plots()
    load_h5.get_MSDs()
    load_h5.get_trcs()


if __name__ == "__main__":
    main()
    