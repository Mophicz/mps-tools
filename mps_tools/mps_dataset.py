import os
from functools import cached_property

import numpy as np


def _load_c4da_array(file_path):
    """
    Loads measurement data from a c4da file using numpy's fromfile method.
    The file is expected to have a 16-byte header (4 int32 values) followed by
    complex128 data points. The data is reshaped into a 4D array based on the 
    header information.
    
    return shape: (H_DC, H_AC, harmonics, f_AC)
    """
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not find the file: {file_path}")

    with open(file_path, 'rb') as f:
        # Read the header: The first 16 bytes are four 32-bit integers
        shape = tuple(np.fromfile(f, dtype=np.int32, count=4))
        
        # Read the measurement data: The rest of the file is complex128
        # (64-bit real + 64-bit imaginary = 16 bytes per data point)
        raw_data = np.fromfile(f, dtype=np.complex128)

    # Validate the data size to catch corrupted or incomplete files
    expected_points = np.prod(shape)
    actual_points = raw_data.size
    
    if actual_points != expected_points:
        raise ValueError(
            f"Data size mismatch in {file_path}. "
            f"Header claims shape {shape} ({expected_points} points), "
            f"but file contains {actual_points} points."
        )

    # Reshape the 1D array into the 4D measurement matrix
    data_4d = raw_data.reshape(shape, order='F')

    return data_4d


def _parse_metadata(txt_path):
    """Parses the text file into a dictionary."""
    if not os.path.exists(txt_path):
        print(f"Warning: No metadata file found at {txt_path}")
        return {}
            
    meta = {}
    with open(txt_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip headers like [experiment-info] or empty lines
            if not line or line.startswith('[') or '=' not in line:
                continue
                
            key, val = line.split('=', 1)
            
            # Handle European decimal separators safely
            if ',' in val and not any(c.isalpha() for c in val):
                val = val.replace(',', '.')
            
            # Attempt to convert to int or float, otherwise keep as string
            try:
                if '.' in val:
                    meta[key] = float(val)
                else:
                    meta[key] = int(val)
            except ValueError:
                meta[key] = val
                
    return meta


class MPSDataset:
    """
    A container for Magnetic Particle Spectrometry (MPS) measurement data 
    loaded from c4da files. Expected data shape: (H_DC, H_AC, harmonics, f_AC).
    """
    def __init__(self, data, metadata=None, filename=None):
        self._data = data
        self.metadata = metadata or {}
        self.filename = filename
        
    @classmethod
    def from_c4da_file(cls, file_path):
        """Factory method to instantiate an MPSDataset from a .c4da file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Cannot find dataset at: {file_path}")
            
        # Load data
        data_array = _load_c4da_array(file_path)
        
        # Load metadata
        txt_path = os.path.splitext(file_path)[0] + ".txt"
        metadata = _parse_metadata(txt_path)
        
        filename = os.path.basename(file_path)
        
        # Return an instance of the class
        return cls(data=data_array, metadata=metadata, filename=filename)
    
    @property
    def h_dc_values(self):
        """Extracts the physical H_DC step values as a numpy array."""
        if not self.metadata:
            return np.arange(self.num_dc_steps)
        n_steps = int(self.metadata.get('nStepsDC', self.num_dc_steps))
        return np.array([self.metadata.get(f'DCsteps{i:05d}', 0.0) for i in range(n_steps)])

    @property
    def h_ac_values(self):
        """Extracts the physical H_AC step values as a numpy array."""
        if not self.metadata:
            return np.arange(self.num_ac_steps)
        n_steps = int(self.metadata.get('nStepsAC', self.num_ac_steps))
        return np.array([self.metadata.get(f'ACsteps{i:05d}', 0.0) for i in range(n_steps)])
        
    @property
    def f_ac_values(self):
        """Extracts the physical AC frequencies."""
        if not self.metadata:
            return np.arange(self.num_ac_frequencies)
        n_steps = int(self.metadata.get('ACFrequencySteps', self.num_ac_frequencies))
        return np.array([self.metadata.get(f'ACFrequencies{i:05d}', 0.0) for i in range(n_steps)])

    @property
    def harmonic_values(self):
        """Returns an array of harmonic numbers."""
        return np.arange(1, self.num_harmonics + 1)
        
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, new_data):
        if not isinstance(new_data, np.ndarray):
            raise TypeError("Data must be a numpy array.")
            
        self._data = new_data
    
    @property
    def shape(self):
        return self._data.shape
       
    @property
    def num_dc_steps(self):
        return self._data.shape[0] if self._data.ndim >= 1 else 0
    
    @property
    def num_ac_steps(self):
        return self._data.shape[1] if self._data.ndim >= 2 else 0
        
    @property
    def num_harmonics(self):
        return self._data.shape[2] if self._data.ndim >= 3 else 0
    
    @property
    def num_ac_frequencies(self):
        return self._data.shape[3] if self._data.ndim >= 4 else 0

    @property
    def real(self):
        return np.real(self.data)
        
    @property
    def imaginary(self):
        return np.imag(self.data)

    @cached_property
    def magnitude(self):
        """Computes and caches the magnitude of the 4D complex dataset."""
        return np.abs(self.data)
        
    @cached_property
    def phase(self):
        """Computes and caches the phase (angle) of the 4D complex dataset."""
        return np.angle(self.data)