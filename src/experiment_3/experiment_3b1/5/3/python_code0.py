import pulp
import json

# Data input
data = json.loads('{"T": 12, "Demand": [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], "OilCap": [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], "CoalCost": 10, "NukeCost": 5, "MaxNuke": 20, "CoalLife": 5, "NukeLife": 10}')

# Parameters
T = data['T']
demand = data['Demand']
oil_capacity = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create the problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision Variables
coal_vars = pulp.LpVariable.dicts("coal", range(1, T + 1), lowBound=0, cat='Continuous')
nuke_vars = pulp.LpVariable.dicts("nuke", range(1, T + 1), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(coal_cost * coal_vars[t] + nuke_cost * nuke_vars[t] for t in range(1, T + 1))

# Constraints
for t in range(1, T + 1):
    # Capacity Constraint
    problem += (oil_capacity[t-1] + 
                 pulp.lpSum(coal_vars[j] for j in range(max(1, t - coal_life + 1), t + 1)) + 
                 pulp.lpSum(nuke_vars[j] for j in range(max(1, t - nuke_life + 1), t + 1)) >= demand[t - 1], 
                 f"Capacity_Constraint_{t}")

    # Nuclear Capacity Constraint
    problem += (pulp.lpSum(coal_vars[j] for j in range(max(1, t - coal_life + 1), t + 1)) + 
                 pulp.lpSum(nuke_vars[j] for j in range(max(1, t - nuke_life + 1), t + 1)) * (max_nuke / 100) >= 
                 pulp.lpSum(coal_vars[j] for j in range(max(1, t - coal_life + 1), t + 1)), 
                 f"Nuclear_Capacity_Constraint_{t}")

# Solve the problem
problem.solve()

# Output results
coal_cap_added = [pulp.value(coal_vars[t]) for t in range(1, T + 1)]
nuke_cap_added = [pulp.value(nuke_vars[t]) for t in range(1, T + 1)]
total_cost = pulp.value(problem.objective)

result = {
    "coal_cap_added": coal_cap_added,
    "nuke_cap_added": nuke_cap_added,
    "total_cost": total_cost
}

print(result)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')