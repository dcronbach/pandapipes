==============
Heat Exchanger
==============

Create Function
---------------

.. _create_heat_exchanger:


.. autofunction:: pandapipes.create_heat_exchanger

Component Table Data
====================

*net.heat_exchanger*

.. tabularcolumns:: |p{0.10\linewidth}|p{0.10\linewidth}|p{0.25\linewidth}|p{0.40\linewidth}|

.. csv-table::
   :file: heat_exchanger_par.csv
   :delim: ;
   :widths: 10, 10, 25, 40



Result Table Data
=================

*net.res_heat_exchanger*

.. tabularcolumns:: |p{0.15\linewidth}|p{0.10\linewidth}|p{0.55\linewidth}|
.. csv-table::
   :file: heat_exchanger_res.csv
   :delim: ;
   :widths: 15, 10, 55

The heat exchanger is a general component to add heat to or remove heat from the system. Regarding the hydraulic
properties, there is no pressure loss calculated. The heat flux is described with the parameter 'qext_w'.

Please note that a positive value extracts heat from the system, where a negative value corresponds to a heat
flux entering the system.