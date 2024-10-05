import pulp
import json

# Data from the provided JSON format
data = json.loads('{"T": 12, "Demand": [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], "OilCap": [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], "CoalCost": 10, "NukeCost": 5, "MaxNuke": 20, "CoalLife": 5, "NukeLife": 10}')

# Define the problem
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

# Variables for coal and nuclear capacity additions
coal_cap_added = pulp.LpVariable.dicts("coal_cap_added", range(1, data['T'] + 1), lowBound=0)
nuke_cap_added = pulp.LpVariable.dicts("nuke_cap_added", range(1, data['T'] + 1), lowBound=0)

# Objective function
problem += pulp.lpSum(data['CoalCost'] * coal_cap_added[t] + data['NukeCost'] * nuke_cap_added[t] for t in range(1, data['T'] + 1))

# Constraints
for t in range(1, data['T'] + 1):
    # Coal and Nuclear Capacity Balance
    coal_capacity = pulp.lpSum(coal_cap_added[i] for i in range(max(1, t - data['CoalLife'] + 1), t + 1))
    nuke_capacity = pulp.lpSum(nuke_cap_added[j] for j in range(max(1, t - data['NukeLife'] + 1), t + 1))
    problem += (coal_capacity + nuke_capacity + data['OilCap'][t - 1] >= data['Demand'][t - 1]), f"Capacity_Balance_{t}"
    
    # Nuclear Capacity Constraint
    problem += (nuke_capacity <= (data['MaxNuke'] / 100) * (coal_capacity + nuke_capacity + data['OilCap'][t - 1])), f"Nuclear_Capacity_Constraint_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')