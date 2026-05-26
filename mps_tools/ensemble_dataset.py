import numpy as np
from mps_dataset import MPSDataset


class EnsembleDataset(MPSDataset):
    """
    Represents an averaged collection of Magnetic Particle Spectrometry (MPS)
    measurements. Inherits physical axes and properties from a base MPSDataset.
    """

    def __init__(
        self, data, std_dev, num_samples, metadata=None, filename=None
    ):
        super().__init__(data=data, metadata=metadata, filename=filename)
        self.std_dev = std_dev
        self.num_samples = num_samples
