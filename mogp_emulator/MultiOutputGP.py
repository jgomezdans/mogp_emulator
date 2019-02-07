# Class implementing a multi-output Gaussian Process for emulating the output of
# a series of computer simulations. Since each emulator is independent of the
# others, the emulators can be fit in parallel, significantly speeding up
# the fitting procedure.

# The class relies on an underlying implementation of a gp_emulator which you must
# have installed on your system. I used Jose Gomez-Dans' original implementation,
# but the interface for Sinan's code should be idential. However, I note that Sinan's
# code did not use the most efficient method for forming the covariance matrix, which
# takes up the bulk of the time for fitting each emulator. Therefore, I suggest
# using Jose's code for the time being, as it should give satisfactory performance
# for the tsunami problem with 210 simulations and 14 parameters.

from multiprocessing import Pool
import numpy as np
from gp_emulator.GaussianProcess import GaussianProcess

class MultiOutputGP(object):
    """
    Implementation of a multiple-output Gaussian Process Emulator.
    """
    def __init__(self, inputs, targets):
        """
        Create a new multi-output GP Emulator
        """
        
        # check input types and shapes, reshape as appropriate for the case of a single emulator
        inputs = np.array(inputs)
        targets = np.array(targets)
        if len(inputs.shape) == 2 and len(targets.shape) == 1:
            inputs = np.reshape(inputs, (1, inputs.shape[0], inputs.shape[1]))
            targets = np.reshape(targets, (1, len(targets)))
        elif not (len(inputs.shape) == 3 and len(targets.shape) == 2):
            raise ValueError("inputs/targets must be 3D/2D or 2D/1D, respectively")
        if not (inputs.shape[0:2] == targets.shape[0:2]):
            raise ValueError("inputs and targets must have the same first two dimentions")

        self.emulators = [ GaussianProcess(single_input, single_target)
                            for single_input, single_target in zip(inputs, targets)]
        
        self.n_emulators = inputs.shape[0]
        self.n = inputs.shape[1]
        self.D = inputs.shape[2]
        
    def get_n_emulators(self):
        """
        Returns the number of emulators
        """
        return self.n_emulators
        
    def get_n(self):
        """
        Returns number of training examples in each emulator
        """
        return self.n
        
    def get_D(self):
        """
        Returns number of inputs for each emulator
        """
        return self.D
        
    def learn_hyperparameters(self, n_tries=15, verbose=False, x0=None, processes=None):
        """
        Fit hyperparameters for each model
        """
        pass
        
    def predict(self, testing, do_deriv=True, do_unc=True, processes=None):
        """
        Make a prediction for a set of input vectors
        """
        pass
        
    def __str__(self):
        """
        Returns a string representation of the model
        """
        return ("Multi-Output Gaussian Process with:\n"+
                 str(self.get_n_emulators())+" emulators\n"+
                 str(self.get_n())+" training examples\n"+
                 str(self.get_D())+" input variables")
        