"""
Objects representing models which implement some form of supervised learning.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import numpy as np

from .params import Parameterized
from ..learning import optimize

__all__ = ['Model']


class Model(Parameterized):
    def __new__(cls, *args, **kwargs):
        self = super(Model, cls).__new__(cls, *args, **kwargs)
        self._X = None
        self._Y = None
        return self

    @property
    def ndata(self):
        """
        The number of independent observations added to the model.
        """
        return 0 if self._X is None else self._X.shape[0]

    @property
    def data(self):
        return (self._X, self._Y)

    def reset(self):
        self._X = None
        self._Y = None
        self._update()

    def __deepcopy__(self, memo):
        # don't make a copy of the data.
        memo[id(self._X)] = self._X
        memo[id(self._Y)] = self._Y
        return super(Model, self).__deepcopy__(memo)

    def copy(self, theta=None, transform=False, reset=False):
        obj = super(Model, self).copy(theta, transform)
        if reset:
            obj.reset()
        return obj

    def add_data(self, X, Y):
        """
        Add a new set of input/output data to the model.
        """
        if self._X is None:
            self._X = X.copy()
            self._Y = Y.copy()
            self._update()

        elif hasattr(self, '_updateinc'):
            self._updateinc(X, Y)
            self._X = np.r_[self._X, X]
            self._Y = np.r_[self._Y, Y]

        else:
            self._X = np.r_[self._X, X]
            self._Y = np.r_[self._Y, Y]
            self._update()

    def get_loglike(self, grad=False):
        """
        Get the log-likelihood of the model (and its gradient if requested).
        """
        raise NotImplementedError

    def optimize(self):
        self.set_params(optimize(self, True), True)


class PosteriorModel(Model):
    def get_posterior(self, X, grad=False, predictive=False):
        """
        Compute the first two moments of the marginal posterior, evaluated at
        input points X.
        """
        raise NotImplementedError
