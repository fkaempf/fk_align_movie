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

    root = tk.Tk()
    root.title("Select hdf5 file")


    dir_path = filedialog.askopenfilename(title="Select hdf5 file")

    root.destroy()
    root.mainloop()
    return dir_path


file = h5py.File(askforhdf5(), 'r')




imaging_data = np.array(file['z_plane0000']['imaging_green_channel']).astype(np.uint16)
imaging_information = np.array(file['z_plane0000']['imaging_information'])
visual_stimulus_data = np.array(file['z_plane0000']['stimulus_information'])

print(imaging_data.shape)


imaging_time = imaging_information[:, 0]

f_imaging_interpolation_function_F = interp1d(imaging_time, imaging_data, axis=0, bounds_error=False)

trials_stimulus_aligned_F = dict()

for stimulus_start_time, stim in zip(visual_stimulus_data["stimulus_start_times"],
                                     visual_stimulus_data["stimulus_start_indices"]):

    print(stimulus_start_time, stim)

    ts = np.arange(stimulus_start_time - 10, stimulus_start_time + 60 + 10 - 0.25, 0.5)
    stimulus_aligned_F = f_imaging_interpolation_function_F(ts)


    if stim in trials_stimulus_aligned_F:
        trials_stimulus_aligned_F[stim].append(stimulus_aligned_F)
    else:
        trials_stimulus_aligned_F[stim] = [stimulus_aligned_F]

print('extacted stimulus data')

avg_response0 = np.nanmean(trials_stimulus_aligned_F[0], axis=0)
avg_response1 = np.nanmean(trials_stimulus_aligned_F[1], axis=0)
avg_response_diff = avg_response0 - avg_response1 + 10000

imsave("z_plane0000_trial000_imaging_roi00_green_channel_motion_corrected_avg0.tif", avg_response0)
imsave("z_plane0000_trial000_imaging_roi00_green_channel_motion_corrected_avg1.tif", avg_response1)
imsave("z_plane0000_trial000_imaging_roi00_green_channel_motion_corrected_diff.tif", avg_response_diff)


