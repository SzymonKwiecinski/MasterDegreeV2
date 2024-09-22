import pulp
import json

# Input data in JSON format
data = {'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}

# Extracting parameters from data
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100.0
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create the LP problem
problem = pulp.LpProblem("Capacity_Expansion_Problem", pulp.LpMinimize)

# Decision variables
coal_cap_added = pulp.LpVariable.dicts("CoalAdded", range(T), lowBound=0, cat='Continuous')
nuke_cap_added = pulp.LpVariable.dicts("NukeAdded", range(T), lowBound=0, cat='Continuous')

# Objective function: minimize total cost
problem += pulp.lpSum([coal_cost * coal_cap_added[t] for t in range(T)]) + pulp.lpSum([nuke_cost * nuke_cap_added[t] for t in range(T)])

# Constraints for meeting demand
for t in range(T):
    total_capacity = oil_cap[t] + pulp.lpSum([coal_cap_added[tt] for tt in range(max(0, t - coal_life + 1), t + 1)]) + pulp.lpSum([nuke_cap_added[tt] for tt in range(max(0, t - nuke_life + 1), t + 1)])
    problem += total_capacity >= demand[t], f"DemandConstraint_{t}"

# Constraints for nuclear capacity percentage
for t in range(T):
    total_capacity = oil_cap[t] + pulp.lpSum([coal_cap_added[tt] for tt in range(max(0, t - coal_life + 1), t + 1)]) + pulp.lpSum([nuke_cap_added[tt] for tt in range(max(0, t - nuke_life + 1), t + 1)])
    problem += pulp.lpSum([nuke_cap_added[tt] for tt in range(max(0, t - nuke_life + 1), t + 1)]) <= max_nuke * total_capacity, f"NuclearCapacityLimit_{t}"

# Solve the problem
problem.solve()

# Prepare output
coal_cap_added_values = [pulp.value(coal_cap_added[t]) for t in range(T)]
nuke_cap_added_values = [pulp.value(nuke_cap_added[t]) for t in range(T)]
total_cost = pulp.value(problem.objective)

output = {
    "coal_cap_added": coal_cap_added_values,
    "nuke_cap_added": nuke_cap_added_values,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')