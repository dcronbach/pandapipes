# Copyright (c) 2020 by Fraunhofer Institute for Energy Economics
# and Energy System Technology (IEE), Kassel. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be found in the LICENSE file.

import copy

import pandas as pd
import numpy as np
from pandapower import pandapowerNet
from pandapower.auxiliary import ADict

from pandapipes import __version__
from pandapipes import pandapipesNet

try:
    import pplog as logging
except ImportError:
    import logging

logger = logging.getLogger(__name__)


class MultiNet(ADict):
    """
    A 'MultiNet' is a frame for different pandapipes & pandapower nets and coupling controllers.

    Usually, a multinet is a multi energy net which one net per energy carrier. 
    The coupled simulation can be run with
    pandapipes.multinet.control.run_control_multinet.run_control()
    The nets are stored with a unique key in a dictionary in multinet['nets'].
    Controllers that connect to nets are stored in multinet['controller'].
    """

    def __init__(self, name = "multinet", *args, **kwargs):
        """

        :param args: item of the ADict
        :type args: variable
        :param kwargs: item of the ADict with corresponding name
        :type kwargs: dict
        """
        default_multinet_structure = {
            # structure data
            # f8, u4 etc. are probably referencing numba or numpy data types
            "name": "",
            "nets": dict(),
            "version": __version__,
            "controller": [('object', np.dtype(object)),
                           ('in_service', "bool"),
                           ('order', "float64"),
                           ('level', np.dtype(object)),
                           ('initial_run', "bool"),
                           ("recycle", "bool")]}

        super().__init__(default_multinet_structure)
        if isinstance(default_multinet_structure, self.__class__):
            net = default_multinet_structure
            self.clear()
            self.update(**net.deepcopy())

        self['controller'] = pd.DataFrame(np.zeros(0, dtype=self['controller']), index=[])
        self['name'] = name


        self.power_net =[]
        self._bus =[]
        self._line = []

        self.gas_net = []
        self._gas_junction = []
        self._gas_pipe = []

        # Unterscheidungsmöglichkeit zwischen Gas- und Wärmenetzen fehlt
        self._heat_junction = []
        self._heat_pipes = []

    def _set_attributes(self, net):
            if isinstance(net, pandapowerNet):
                self._bus = net["bus"]
                self._line = net["line"]
                self.power_net = net
            elif isinstance(net, pandapipesNet):
                self._gas_junction = net["junction"]
                self._gas_pipe = net["pipe"]
                self.gas_net = net


    def add_net(self, net, net_name='power', overwrite=False):
        """
        Add a pandapipes or pandapower net to the multinet structure.

        :param multinet: multinet to which a pandapipes/pandapower net will be added
        :type multinet: pandapipes.MultiNet
        :param net: pandapipes or pandapower net that will be added to the multinet
        :type net: pandapowerNet or pandapipesNet
        :param net_name: unique name for the added net, e.g. 'power', 'gas', or 'power_net1'
        :type net_name: str
        :param overwrite: whether a net should be overwritten if it has the same net_name
        :type overwrite: bool
        :return: net reference is added inplace to the multinet (in multinet['nets'])
        :rtype: None
        """
        if net_name in self['nets'] and not overwrite:
            logger.warning("A net with the name %s exists already in the multinet. If you want to "
                           "overwrite it, set 'overwrite' to True." % net_name)
        else:
            self['nets'][net_name] = net
            self._set_attributes(net)



    def add_nets(self, overwrite=False, **networks):
        """
        Add multiple nets to a multinet. 'networks' is one or more keyword arguments with nets.

        :param multinet: multinet to which several pandapipes/pandapower nets are added
        :type multinet: pandapipes.MultiNet
        :param overwrite: whether a net should be overwritten if it has the same net_name
        :type overwrite: bool
        :param networks: one or more keyword arguments with pandapipes/pandapower nets as values.
                         The keyword of each net will be set in multinet.nets as the name for the
                         network in the respective argument.
        :type networks: kwarg (name=net)
        :return: nets are added to multinet
        :rtype: None
        """
        for name, net in networks.items():
            self.add_net(net, name, overwrite)


    def deepcopy(self):
        return copy.deepcopy(self)


    def __repr__(self):  # pragma: no cover
        """
        defines the representation of the multinet in the console

        :return: representation
        :rtype: str
        """

        r = "This multi net includes following nets:"
        for cat in self.nets:
            if isinstance(self['nets'][cat], pandapowerNet):
                r += "\n   - %s (%s pandapowerNet)" % (cat, 1)
            elif isinstance(self['nets'][cat], pandapipesNet):
                r += "\n   - %s (%s pandapipesNet)" % (cat, 1)
            else:
                r += "\n   - %s (%s nets)" % (cat, len(self['nets'][cat]))

        par = []
        for tb in list(self.keys()):
            if isinstance(self[tb], pd.DataFrame) and len(self[tb]) > 0:
                par.append(tb)
            elif tb == 'std_type':
                par.append(tb)
        if par:
            r += "\nand the following parameter tables:"
            for tb in par:
                r += "\n   - %s (%s elements)" % (tb, len(self[tb]))
        return r


    def get_gas_junctions(self):
        return self._gas_junction

    def get_gas_pipes(self):
        return self._gas_pipe

    def get_buses(self):
        return self._bus

    def get_lines(self):
        return self._line
