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
ds = MPSDataset.from_c4da_file(filename)

# get data from dataset object
data = ds.data          # complex spectrum data 
real = ds.real          # real part
imag = ds.imaginary     # imaginary part
mag = ds.magnitude      # magnitude
phase = ds.phase        # phase

x_hdc = ds.h_dc_values      # offset field strength vector
y_hac = ds.h_ac_values      # alternating field strength vector

## Examples
# get a single point
single_point = data[h_dc, h_ac, harmonic_index, f_ac]

# get full spectrum
spectrum = data[h_dc, h_ac, :, f_ac]

# get magnitude "fingerprint"
z_data = mag[:, :, harmonic_index, f_ac]
```