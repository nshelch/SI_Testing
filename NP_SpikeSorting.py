"""
This should become a template script for running SpikeInterface once you've 
played with parameters in the notebooks and are happy with them
"""

import spikeinterface.full as si
import matplotlib.pyplot as plt
import numpy as np
import os
import warnings
warnings.simplefilter("ignore")


## Global arguments for parallel processing
# Arguments include: 
# n_jobs: number of cores used (-1 uses all the cores)
# chunk_duration: Chunk duration in s if float or with units if str (e.g. “1s”, “500ms”)
# progress_bar: If True, a progress bar is printed

global_job_kwargs = dict(n_jobs=4, chunk_duration="1s", progress_bar=True)
si.set_global_job_kwargs(**global_job_kwargs)

# Set the base folder and where the binary data are located
base_folder = r'C:/Users/nshelch/Desktop/Neuropixel Spike Interface/'
binary_folder = base_folder + '/Binary Data/quiet_AP_continuous.bin'
assert os.path.exists(base_folder)

## Reading the data

# Dataset params
sampling_frequency = 30_000.0
num_channels = 384 
dtype_int = 'int16' 
gain_to_uV = 0.195  
offset_to_uV = 0   

raw_rec = si.read_binary(file_paths=binary_folder, sampling_frequency=sampling_frequency,
                           num_channels=num_channels, dtype=dtype_int,
                           gain_to_uV=gain_to_uV, offset_to_uV=offset_to_uV)

# Importing probe information #TODO: Make this into a function where it loads a probe file instead
import probeinterface as pi

linear_probe = pi.generate_linear_probe(num_elec=384, ypitch=20, contact_shapes='square', contact_shape_params={'width': 12})

# Map the channel ids to device ids
channel_indices = np.arange(384)
linear_probe.set_device_channel_indices(channel_indices)

# Assign the probe information to the recording
raw_rec_probe = raw_rec.set_probe(linear_probe)

## Preprocessing #TODO: How much of this should be moved to params closer to the top (or its own section?)

# Bandpass filter
recording_f = si.bandpass_filter(raw_rec_probe, freq_min=300, freq_max=9000)

# Detect bad channels
bad_channel_ids, channel_labels = si.detect_bad_channels(recording_f)

# Remove bad channels
recording_good_channels_f = recording_f.remove_channels(bad_channel_ids)

# Common Median Reference (CMR)
recording_good_channels_cmr = si.common_reference(recording_good_channels_f, reference='global', operator='median')

## Spike Sorting

# # Specify kilosort location (Needs to be done each time)
# kilosort_25_path = 'C://GitHub/Kilosort-2.5/'
# si.Kilosort2_5Sorter.set_kilosort2_5_path(kilosort_25_path)
# si.get_default_sorter_params('kilosort2_5')

# # Specify specific sorter params
# sorter_params = {'do_correction': False}

# # run spike sorting on entire recording
# sorting_KS25 = si.run_sorter(sorter_name='kilosort2_5', recording=recording_good_channels_cmr, remove_existing_folder=True,
#                              output_folder=path_extra + '/results_KS25',
#                              verbose=True, **sorter_params, **global_job_kwargs)

# print(f'Spike train of a unit: {sorting_KS25.get_unit_spike_train(unit_id=1)}')
# print(f'Spike train of a unit (in s): {sorting_KS25.get_unit_spike_train(unit_id=1, return_times=True)}')

# # Saving/loading spike sorting outputs
# #sorting_saved_KS25 = sorting_KS25.save(folder=base_folder / "sorting_KS25")
# sorting_KS25 = si.load_extractor(base_folder / "sorting_KS25")


# Docker attempts
sorting = si.run_sorter(sorter_name='kilosort2_5',recording=recording_good_channels_cmr, remove_existing_folder=True,
                        output_folder=base_folder + '/results_KS25',
                        singularity_image=True,
                        **global_job_kwargs)











