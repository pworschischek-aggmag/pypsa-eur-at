# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: : 2023-2024 The PyPSA-Eur Authors
#
# SPDX-License-Identifier: MIT

# This script helps to generate a scenarios.yaml file for PyPSA-Eur.
# You can modify the template to your needs and define all possible combinations of config values that should be considered.

if "snakemake" in globals():
    filename = snakemake.output[0]
else:
    filename = "../config/scenarios.yaml"

import itertools

# Insert your config values that should be altered in the template.
# Change `config_section` and `config_section2` to the actual config sections.
template = """
{scenario_name}:
    foresight: {foresight}
    clustering: 
      temporal:
        resolution_elec: {timesteps}
        resolution_sector: {timesteps}
    solving:
      solver:
        name: {solver_name}
        options: {solver_name}-default
"""

# Define all possible combinations of config values.
# This must define all config values that are used in the template.
config_values = dict(
    solver_name=["gurobi", "highs", "copt"],
    timesteps=[120, 3, 1],  # h
    foresight=["myopic", "perfect"],
)

combinations = [
    dict(zip(config_values.keys(), values))
    for values in itertools.product(*config_values.values())
]

with open(filename, "w") as f:
    for config in combinations:
        scenario_name = (
            f"{config['foresight']}_{config['solver_name']}_{config['timesteps']}h"
        )
        f.write(template.format(scenario_name=scenario_name, **config))
