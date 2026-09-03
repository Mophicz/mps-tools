Install:
```
pip install git+https://github.com/Mophicz/mps-tools.git
```

Import: 
```python
from mps_tools import MPSDataset
```

Use: 
```python
# load data from .c4da file
ds = MPSDataset.from_c4da_file(filepath)

# get data from dataset object
data = ds.data          # complex spectrum data 
real = ds.real          # real part
imag = ds.imaginary     # imaginary part
mag = ds.magnitude      # magnitude
phase = ds.phase        # phase (rad)
# or
unwrapped_phase = np.unwrap(ds.phase)

# options for x-axis (extracted from measurement metadata txt file)
ds.h_dc_values
ds.h_ac_values
ds.harmonic_values
ds.f_ac_values

## Examples
# get a single point
single_point = data[h_dc, h_ac, harmonic_index, f_ac]

# get full spectrum
spectrum = data[h_dc, h_ac, :, f_ac]

# get magnitude "fingerprint"
z_magnitude = mag[:, :, harmonic_index, f_ac]
x_hdc = ds.h_dc_values      # DC field strength (x-axis of "fingerprint" plot)
y_hac = ds.h_ac_values      # AC field strength (y-axis of "fingerprint" plot)
```

Example: Plot Magnitude Spectrum
```python
# Load dataset
ds = MPSDataset.from_c4da_file(filepath)

# Get odd harmonics
x = ds.harmonic_values[2::2]

# Get magnitudes for odd harmonics
y = ds.magnitude[0, -1, 2::2, 0]

plt.plot(x, y)
plt.show()
```

Example: Plot Magnitude DC Sweep of 3rd harmonic
```python
# Load dataset
ds = MPSDataset.from_c4da_file(filepath)

# Get DC values
x = ds.h_dc_values

# Get magnitudes for 3rd harmonic
y = ds.magnitude[:, -1, 2, 0]

plt.plot(x, y)
plt.show()
```
