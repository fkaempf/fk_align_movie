# create a stimulus triggered movie
import os
import numpy as np
from tifffile import imread, imsave
from scipy.interpolate import interp1d
import tkinter as tk
from tkinter import filedialog
import os
import h5py





def askforhdf5():
    global dir_path
    root = tk.Tk()
    root.title("Select hdf5 file")


    dir_path = filedialog.askopenfilename(title="Select hdf5 file")

    root.destroy()
    root.mainloop()
    return dir_path
file = askforhdf5()

with h5py.File(file, 'r') as file:
    imaging_data = np.array(file['0']['fp_imaging_data_green_channel'])#.astype(np.uint16)
    imaging_information = np.array(file['0']['imaging_information'])#.astype(np.uint16)
    visual_stimulus_data = np.array(file['0']['stimulus_information'])#.astype(np.uint16)

imaging_time = imaging_information[:, 0]

f_imaging_interpolation_function_F = interp1d(imaging_time, imaging_data, axis=0, bounds_error=False)

trials_stimulus_aligned_F = dict()

stimulus_start_times = np.transpose(visual_stimulus_data)[0]
stimulus_types = np.transpose(visual_stimulus_data)[2]


for stimulus_start_time, stim in zip(stimulus_start_times, stimulus_types):

    print(stimulus_start_time, stim)

    ts = np.arange(stimulus_start_time - 10, stimulus_start_time + 60 + 10 - 0.25, 0.5)
    stimulus_aligned_F = f_imaging_interpolation_function_F(ts).astype(np.uint16)

    if stim in trials_stimulus_aligned_F:
        trials_stimulus_aligned_F[stim].append(stimulus_aligned_F)
    else:
        trials_stimulus_aligned_F[stim] = [stimulus_aligned_F]

del f_imaging_interpolation_function_F
del imaging_data

print('extacted stimulus data')

avg_response0 = np.nanmean(trials_stimulus_aligned_F[0], axis=0)
avg_response1 = np.nanmean(trials_stimulus_aligned_F[1], axis=0)
avg_response_diff = avg_response0 - avg_response1 + 10000

imsave(dir_path.split('/')[-1].split('.')[0] + "_avg0.tif", avg_response0.astype(np.uint16))
imsave(dir_path.split('/')[-1].split('.')[0] + "_avg1.tif", avg_response1.astype(np.uint16))
imsave(dir_path.split('/')[-1].split('.')[0] + "_diff.tif", avg_response_diff.astype(np.uint16))


