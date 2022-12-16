
from rl.policy import Policy
import numpy as np
import random

class CustomAnnealedPolicy(Policy):
    """Implement the linear annealing policy
    Linear Annealing Policy computes a current threshold value and
    transfers it to an inner policy which chooses the action. The threshold
    value is following a linear function decreasing over time."""
    def __init__(self, inner_policy, attr, value_max, value_min, value_decay, value_test):
        if not hasattr(inner_policy, attr):
            raise ValueError('Policy does not have attribute "{}".'.format(attr))

        super(CustomAnnealedPolicy, self).__init__()

        self.inner_policy = inner_policy
        self.attr = attr
        self.value_max = value_max
        self.value_min = value_min
        self.value_decay = value_decay
        self.value_test = value_test

    def get_current_value(self):
        """Return current annealing value
        # Returns
            Value to use in annealing
        """
        if self.agent.training:
            # Linear annealed: f(x) = ax + b.
            value = max(self.value_min, self.value_min + (self.value_max - self.value_min) * np.exp( - float(self.agent.step)  / self.value_decay))
        else:
            value = self.value_test
        return value

    def select_action(self, **kwargs):
        """Choose an action to perform
        # Returns
            Action to take (int)
        """
        setattr(self.inner_policy, self.attr, self.get_current_value())
        return self.inner_policy.select_action(**kwargs)

    @property
    def metrics_names(self):
        """Return names of metrics
        # Returns
            List of metric names
        """
        return ['mean_{}'.format(self.attr)]

    @property
    def metrics(self):
        """Return metrics values
        # Returns
            List of metric values
        """

        return [getattr(self.inner_policy, self.attr)]

    def get_config(self):
        """Return configurations of LinearAnnealedPolicy
        # Returns
            Dict of config
        """
        config = super(CustomAnnealedPolicy, self).get_config()
        config['attr'] = self.attr
        config['value_max'] = self.value_max
        config['value_min'] = self.value_min
        config['value_decay'] = self.value_decay
        config['value_test'] = self.value_test
        config['inner_policy'] = get_object_config(self.inner_policy)
        return config