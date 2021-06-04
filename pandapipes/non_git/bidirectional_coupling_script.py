
import pandas as pd
import numpy as np
from pandapipes.component_models import Pipe
import pandapipes.properties.fluids as fl
pd.set_option('display.max_columns', 15)
pd.set_option('display.width', 300000)
from pandapipes.properties.fluids import get_fluid

import pandapipes



d = 75e-3

net = pandapipes.create_empty_network("net", add_stdtypes=False)
pandapipes.create_fluid_from_lib(net, "water", overwrite=True)

j0 = pandapipes.create_junction(net, pn_bar=5, tfluid_k=283)
j1 = pandapipes.create_junction(net, pn_bar=5, tfluid_k=283)


pandapipes.create_ext_grid(net, j0, p_bar=5, t_k=350, type="pt")

pandapipes.create_sink(net, j1, mdot_kg_per_s=1)


pandapipes.create_pipe_from_parameters(net, j0, j1, 2.5, 0.075, k_mm=.1, alpha_w_per_m2k=5, sections=10)



print(net.pipe)

pandapipes.pipeflow(net, stop_condition="tol", seg_iter=60, friction_model="nikuradse",
                   mode='seg',  nonlinear_method="automatic", tol_p=1e-4,
                   tol_v=1e-4)


print(net.res_pipe)
print(net.res_junction)
pipe_results = Pipe.get_internal_results(net, [0])
print(pipe_results['TINIT'])
Pipe.plot_pipe(net,0, pipe_results)





