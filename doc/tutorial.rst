..
  SPDX-FileCopyrightText: 2019-2024 The PyPSA-Eur Authors

  SPDX-License-Identifier: CC-BY-4.0

.. _tutorial:

###############################
Tutorial: Electricity-Only
###############################

.. raw:: html

    <iframe width="832" height="468" src="https://www.youtube.com/embed/mAwhQnNRIvs" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

.. note::
    If you have not done it yet, follow the :ref:`installation` steps first.

In this tutorial, we will build a heavily simplified power system model for
Belgium. But before getting started with **PyPSA-Eur** it makes sense to be familiar
with its general modelling framework `PyPSA <https://pypsa.readthedocs.io>`__.

Running the tutorial requires limited computational resources compared to the
full model, which allows the user to explore most of its functionalities on a
local machine. The tutorial will cover examples on how to configure and
customise the PyPSA-Eur model and run the ``snakemake`` workflow step by step
from network creation to the solved network. The configuration for the tutorial
is located at ``config/test/config.electricity.yaml``. It includes parts deviating from
the default config file ``config/config.default.yaml``. To run the tutorial with this
configuration, execute

.. code:: bash
    :class: full-width

    snakemake -call results/test-elec/networks/elec_s_6_ec_lcopt_.nc --configfile config/test/config.electricity.yaml

This configuration is set to download a reduced cutout via the rule :mod:`retrieve_cutout`.
For more information on the data dependencies of PyPSA-Eur, continue reading :ref:`data`.

How to configure runs?
===========================

The model can be adapted to only include selected countries (e.g. Belgium) instead of all European countries to limit the spatial scope.

.. literalinclude:: ../config/test/config.electricity.yaml
   :language: yaml
   :start-at: countries:
   :end-before: snapshots:

Likewise, the example's temporal scope can be restricted (e.g. to a single week).

.. literalinclude:: ../config/test/config.electricity.yaml
   :language: yaml
   :start-at: snapshots:
   :end-before: electricity:

It is also possible to allow less or more carbon-dioxide emissions. Here, we limit the emissions of Belgium to 100 Mt per year.

.. literalinclude:: ../config/test/config.electricity.yaml
   :language: yaml
   :start-at: electricity:
   :end-before: extendable_carriers:

PyPSA-Eur also includes a database of existing conventional powerplants.
We can select which types of existing powerplants we like to be extendable:

.. literalinclude:: ../config/test/config.electricity.yaml
   :language: yaml
   :start-at: extendable_carriers:
   :end-before: renewable_carriers:

To accurately model the temporal and spatial availability of renewables such as
wind and solar energy, we rely on historical weather data. It is advisable to
adapt the required range of coordinates to the selection of countries.

.. literalinclude:: ../config/test/config.electricity.yaml
   :language: yaml
   :start-at: atlite:
   :end-before: renewable:

We can also decide which weather data source should be used to calculate
potentials and capacity factor time-series for each carrier. For example, we may
want to use the ERA-5 dataset for solar and not the default SARAH-3 dataset.

.. literalinclude:: ../config/test/config.electricity.yaml
   :language: yaml
   :start-at: solar:
   :end-at: cutout:

Finally, it is possible to pick a solver. For instance, this tutorial uses the
open-source solver GLPK.

.. literalinclude:: ../config/test/config.electricity.yaml
   :language: yaml
   :start-at: solver:
   :end-before: plotting:

Note, that ``config/test/config.electricity.yaml`` only includes changes relative to
the default configuration. There are many more configuration options, which are
documented at :ref:`config`.


How to use ``snakemake`` rules?
===================================

Open a terminal, go into the PyPSA-Eur directory, and activate the ``pypsa-eur`` environment with

.. code:: bash

    mamba activate pypsa-eur

Let's say based on the modifications above we would like to solve a very simplified model
clustered down to 6 buses and every 24 hours aggregated to one snapshot. The command

.. code:: bash

    snakemake -call results/test-elec/networks/elec_s_6_ec_lcopt_.nc --configfile config/test/config.electricity.yaml

orders ``snakemake`` to run the rule :mod:`solve_network` that produces the solved network and stores it in ``results/networks`` with the name ``elec_s_6_ec_lcopt_.nc``:

.. literalinclude:: ../rules/solve_electricity.smk
   :start-at: rule solve_network:
   :end-before: rule solve_operations_network:

This triggers a workflow of multiple preceding jobs that depend on each rule's inputs and outputs:

.. graphviz::
    :class: full-width
    :align: center

    digraph snakemake_dag {
        graph[bgcolor=white, margin=0];
        node[shape=box, style=rounded, fontname=sans,                 fontsize=10, penwidth=2];
        edge[penwidth=2, color=grey];
            0[label = "solve_network", color = "0.16 0.6 0.85", style="rounded"];
            1[label = "prepare_network\nll: copt\nopts: ", color = "0.40 0.6 0.85", style="rounded"];
            2[label = "add_extra_components", color = "0.03 0.6 0.85", style="rounded"];
            3[label = "cluster_network\nclusters: 6", color = "0.26 0.6 0.85", style="rounded"];
            4[label = "simplify_network\nsimpl: ", color = "0.17 0.6 0.85", style="rounded"];
            5[label = "add_electricity", color = "0.39 0.6 0.85", style="rounded"];
            6[label = "build_renewable_profiles\ntechnology: solar", color = "0.13 0.6 0.85", style="rounded"];
            7[label = "base_network", color = "0.01 0.6 0.85", style="rounded"];
            8[label = "retrieve_osm_prebuilt", color = "0.27 0.6 0.85", style="rounded"];
            9[label = "build_shapes", color = "0.18 0.6 0.85", style="rounded"];
            10[label = "retrieve_naturalearth_countries", color = "0.41 0.6 0.85", style="rounded"];
            11[label = "retrieve_eez", color = "0.14 0.6 0.85", style="rounded"];
            12[label = "retrieve_databundle", color = "0.38 0.6 0.85", style="rounded"];
            13[label = "retrieve_cutout\ncutout: be-03-2013-era5", color = "0.51 0.6 0.85", style="rounded"];
            14[label = "build_renewable_profiles\ntechnology: solar-hsat", color = "0.13 0.6 0.85", style="rounded"];
            15[label = "build_renewable_profiles\ntechnology: onwind", color = "0.13 0.6 0.85", style="rounded"];
            16[label = "build_renewable_profiles\ntechnology: offwind-ac", color = "0.13 0.6 0.85", style="rounded"];
            17[label = "build_ship_raster", color = "0.16 0.6 0.85", style="rounded"];
            18[label = "retrieve_ship_raster", color = "0.53 0.6 0.85", style="rounded"];
            19[label = "build_renewable_profiles\ntechnology: offwind-dc", color = "0.13 0.6 0.85", style="rounded"];
            20[label = "build_renewable_profiles\ntechnology: offwind-float", color = "0.13 0.6 0.85", style="rounded"];
            21[label = "build_line_rating", color = "0.46 0.6 0.85", style="rounded"];
            22[label = "build_transmission_projects", color = "0.29 0.6 0.85", style="rounded"];
            23[label = "retrieve_cost_data\nyear: 2030", color = "0.11 0.6 0.85", style="rounded"];
            24[label = "build_powerplants", color = "0.18 0.6 0.85", style="rounded"];
            25[label = "build_electricity_demand", color = "0.30 0.6 0.85", style="rounded"];
            26[label = "retrieve_electricity_demand", color = "0.13 0.6 0.85", style="rounded"];
            27[label = "retrieve_synthetic_electricity_demand", color = "0.43 0.6 0.85", style="rounded"];
            1 -> 0
            2 -> 1
            23 -> 1
            3 -> 2
            23 -> 2
            4 -> 3
            23 -> 3
            5 -> 4
            23 -> 4
            7 -> 4
            6 -> 5
            14 -> 5
            15 -> 5
            16 -> 5
            19 -> 5
            20 -> 5
            7 -> 5
            21 -> 5
            22 -> 5
            23 -> 5
            24 -> 5
            25 -> 5
            9 -> 5
            7 -> 6
            12 -> 6
            9 -> 6
            13 -> 6
            8 -> 7
            9 -> 7
            10 -> 9
            11 -> 9
            12 -> 9
            7 -> 14
            12 -> 14
            9 -> 14
            13 -> 14
            7 -> 15
            12 -> 15
            9 -> 15
            13 -> 15
            7 -> 16
            12 -> 16
            17 -> 16
            9 -> 16
            13 -> 16
            18 -> 17
            13 -> 17
            7 -> 19
            12 -> 19
            17 -> 19
            9 -> 19
            13 -> 19
            7 -> 20
            12 -> 20
            17 -> 20
            9 -> 20
            13 -> 20
            7 -> 21
            13 -> 21
            7 -> 22
            9 -> 22
            7 -> 24
            26 -> 25
            27 -> 25
    }

|

In the terminal, this will show up as a list of jobs to be run:

.. code:: bash

    Building DAG of jobs...
    Job stats:
    job                                      count
    -------------------------------------  -------
    add_electricity                              1
    add_extra_components                         1
    base_network                                 1
    build_electricity_demand                     1
    build_line_rating                            1
    build_powerplants                            1
    build_renewable_profiles                     6
    build_shapes                                 1
    build_ship_raster                            1
    build_transmission_projects                  1
    cluster_network                              1
    prepare_network                              1
    retrieve_cost_data                           1
    retrieve_cutout                              1
    retrieve_databundle                          1
    retrieve_eez                                 1
    retrieve_electricity_demand                  1
    retrieve_naturalearth_countries              1
    retrieve_osm_prebuilt                        1
    retrieve_ship_raster                         1
    retrieve_synthetic_electricity_demand        1
    simplify_network                             1
    solve_network                                1
    total                                       28


``snakemake`` then runs these jobs in the correct order.

A job (here ``simplify_network``) will display its attributes and normally some logs below this block:

.. code:: bash

    rule simplify_network:
        input: resources/test/networks/elec.nc, resources/test/costs_2030.csv, resources/test/regions_onshore.geojson, resources/test/regions_offshore.geojson
        output: resources/test/networks/elec_s.nc, resources/test/regions_onshore_elec_s.geojson, resources/test/regions_offshore_elec_s.geojson, resources/test/busmap_elec_s.csv
        log: logs/test/simplify_network/elec_s.log
        jobid: 4
        benchmark: benchmarks/test/simplify_network/elec_s
        reason: Forced execution
        wildcards: simpl=
        resources: tmpdir=<TBD>, mem_mb=12000, mem_mib=11445

Once the whole worktree is finished, it should state so in the terminal.

You will notice that many intermediate stages are saved, namely the outputs of each individual ``snakemake`` rule.

You can produce any output file occurring in the ``Snakefile`` by running

.. code:: bash

    snakemake -call <output file>

For example, you can explore the evolution of the PyPSA networks by running

#. ``snakemake resources/networks/base.nc -call --configfile config/test/config.electricity.yaml``
#. ``snakemake resources/networks/elec.nc -call --configfile config/test/config.electricity.yaml``
#. ``snakemake resources/networks/elec_s.nc -call --configfile config/test/config.electricity.yaml``
#. ``snakemake resources/networks/elec_s_6.nc -call --configfile config/test/config.electricity.yaml``
#. ``snakemake resources/networks/elec_s_6_ec_lcopt_.nc -call --configfile config/test/config.electricity.yaml``

To run all combinations of wildcard values provided in the ``config/config.yaml`` under ``scenario:``,
you can use the collection rule ``solve_elec_networks``.

.. code:: bash

    snakemake -call solve_elec_networks --configfile config/test/config.electricity.yaml

If you now feel confident and want to tackle runs with larger temporal and
spatial scope, clean-up the repository and after modifying the ``config/config.yaml`` file
target the collection rule ``solve_elec_networks`` again without providing the test
configuration file.

.. code:: bash

    snakemake -call purge
    snakemake -call solve_elec_networks

.. note::

    It is good practice to perform a dry-run using the option `-n`, before you
    commit to a run:

    .. code:: bash

        snakemake -call solve_elec_networks -n

How to analyse results?
===============================

The solved networks can be analysed just like any other PyPSA network (e.g. in
Jupyter Notebooks).

.. code:: python

    import pypsa

    n = pypsa.Network("results/networks/elec_s_6_ec_lcopt_.nc")

For inspiration, read the `examples section in the PyPSA documentation <https://pypsa.readthedocs.io/en/latest/examples-basic.html>`__.
