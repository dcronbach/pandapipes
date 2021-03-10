import os

import numpy as np
import pandapipes
import pandas as pd
import pytest
from pandapipes.component_models import Pipe, Junction
from pandapipes.idx_node import PINIT, TINIT
from pandapipes.pipeflow_setup import get_lookup
from pandapipes.test.pipeflow_internals import internals_data_path
from pandapipes.properties.fluids import _add_fluid_to_net
from pandapipes.pipeflow_setup import get_net_option

def test_temperature_internal_nodes_single_pipe():

    net = pandapipes.create_empty_network("net", add_stdtypes=False)
    d = 75e-3
    pandapipes.create_junction(net, pn_bar=5, tfluid_k=283)
    pandapipes.create_junction(net, pn_bar=5, tfluid_k=283)
    pandapipes.create_pipe_from_parameters(net, 0, 1, 6, d, k_mm=.1, sections=6, alpha_w_per_m2k=5)
    pandapipes.create_ext_grid(net, 0, p_bar=5, t_k=330, type="pt")
    pandapipes.create_sink(net, 1, mdot_kg_per_s=1)

    pandapipes.create_fluid_from_lib(net, "water", overwrite=True)

    pandapipes.pipeflow(net, stop_condition="tol", iter=3, friction_model="nikuradse",
                        mode="seg", transient=False, nonlinear_method="automatic", tol_p=1e-4,
                        tol_v=1e-4)

    assert get_net_option(net, "seg_converged") == True


def test_temperature_internal_nodes_tee_2ab_1zu():
    """

    :return:
    :rtype:
    """

    net = pandapipes.create_empty_network("net", add_stdtypes=False)
    d = 75e-3
    j0 = pandapipes.create_junction(net, pn_bar=5, tfluid_k=283)
    j1 = pandapipes.create_junction(net, pn_bar=5, tfluid_k=283)
    j2 = pandapipes.create_junction(net, pn_bar=5, tfluid_k=283)
    j3 = pandapipes.create_junction(net, pn_bar=5, tfluid_k=283)
    pandapipes.create_ext_grid(net, j0, p_bar=5, t_k=350, type="pt")
    pandapipes.create_sink(net, j2, mdot_kg_per_s=1)
    pandapipes.create_sink(net, j3, mdot_kg_per_s=1)

    pandapipes.create_pipe_from_parameters(net, j0, j1, 2.5, d, k_mm=.1, alpha_w_per_m2k=5)
    pandapipes.create_pipe_from_parameters(net, j1, j2, 2.5, d, k_mm=.1, alpha_w_per_m2k=5)
    pandapipes.create_pipe_from_parameters(net, j1, j3, 2.5, d, k_mm=.1, alpha_w_per_m2k=5)

    pandapipes.create_fluid_from_lib(net, "water", overwrite=True)

    pandapipes.pipeflow(net, stop_condition="tol", iter=70, friction_model="nikuradse",
                        mode='seg', transient=False, nonlinear_method="automatic", tol_p=1e-4,
                        tol_v=1e-4)

    assert  get_net_option(net, "seg_converged") == True



def test_temperature_internal_nodes_tee_2zu_1ab_direction_changed():
    """

    :return:
    :rtype:
    """
    net = pandapipes.create_empty_network("net", add_stdtypes=False)
    d = 75e-3
    j0 = pandapipes.create_junction(net, pn_bar=5, tfluid_k=283)
    j1 = pandapipes.create_junction(net, pn_bar=5, tfluid_k=283)
    j2 = pandapipes.create_junction(net, pn_bar=5, tfluid_k=283)
    j3 = pandapipes.create_junction(net, pn_bar=5, tfluid_k=283)
    pandapipes.create_ext_grid(net, j0, p_bar=5, t_k=350, type="pt")
    pandapipes.create_ext_grid(net, j1, p_bar=5, t_k=350, type="pt")
    pandapipes.create_sink(net, j3, mdot_kg_per_s=1)

    pandapipes.create_pipe_from_parameters(net, j0, j2, 2.5, d, k_mm=.1, sections=5,
                                           alpha_w_per_m2k=5)
    pandapipes.create_pipe_from_parameters(net, j2, j1, 2.5, d, k_mm=.1, sections=5,
                                           alpha_w_per_m2k=5)
    pandapipes.create_pipe_from_parameters(net, j2, j3, 2.5, d, k_mm=.1, sections=5,
                                           alpha_w_per_m2k=5)

    pandapipes.create_fluid_from_lib(net, "water", overwrite=True)

    pandapipes.pipeflow(net, stop_condition="tol", iter=70, friction_model="nikuradse",
                        mode='seg', transient=False, nonlinear_method="automatic", tol_p=1e-4,
                        tol_v=1e-4)



    assert  get_net_option(net, "seg_converged") == True


def test_temperature_internal_nodes_masche_1load():
    """

    :return:
    :rtype:
    """
    net = pandapipes.create_empty_network("net", add_stdtypes=False)
    d = 75e-3
    j0 = pandapipes.create_junction(net, pn_bar=5, tfluid_k=283)
    j1 = pandapipes.create_junction(net, pn_bar=5, tfluid_k=283)
    j2 = pandapipes.create_junction(net, pn_bar=5, tfluid_k=283)
    j3 = pandapipes.create_junction(net, pn_bar=5, tfluid_k=283)

    pandapipes.create_pipe_from_parameters(net, j0, j1, 2.5, d, k_mm=.1, sections=6,
                                           alpha_w_per_m2k=5)
    pandapipes.create_pipe_from_parameters(net, j1, j2, 2.5, d, k_mm=.1, sections=6,
                                           alpha_w_per_m2k=5)
    pandapipes.create_pipe_from_parameters(net, j1, j3, 2.5, d, k_mm=.1, sections=6,
                                           alpha_w_per_m2k=5)
    pandapipes.create_pipe_from_parameters(net, j3, j2, 2.5, d, k_mm=.1, sections=6,
                                           alpha_w_per_m2k=5)

    pandapipes.create_ext_grid(net, j0, p_bar=5, t_k=350, type="pt")
    pandapipes.create_sink(net, j2, mdot_kg_per_s=1)

    pandapipes.create_fluid_from_lib(net, "water", overwrite=True)

    pandapipes.pipeflow(net, stop_condition="tol", iter=70, friction_model="nikuradse",
                        mode='seg', transient=False, nonlinear_method="automatic", tol_p=1e-4,
                        tol_v=1e-4)


    assert  get_net_option(net, "seg_converged") == True



