import pulp
import json

data = {'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 
        'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 
        'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 
        'CoalLife': 5, 'NukeLife': 10}

T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create the linear programming problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision variables
coal_cap_added = pulp.LpVariable.dicts("coal_cap", range(T), lowBound=0, cat='Continuous')
nuke_cap_added = pulp.LpVariable.dicts("nuke_cap", range(T), lowBound=0, cat='Continuous')

# Objective function: Minimize total cost
problem += pulp.lpSum(coal_cost * coal_cap_added[t] for t in range(T)) + pulp.lpSum(nuke_cost * nuke_cap_added[t] for t in range(T))

# Constraints
for t in range(T):
    total_capacity = oil_cap[t] + pulp.lpSum(coal_cap_added[i] for i in range(max(0, t-coal_life+1), t+1)) + \
                   pulp.lpSum(nuke_cap_added[j] for j in range(max(0, t-nuke_life+1), t+1))
    problem += total_capacity >= demand[t], f"DemandConstraint_{t}"

    # Max nuclear capacity constraint
    if t >= nuke_life - 1:
        problem += pulp.lpSum(nuke_cap_added[j] for j in range(max(0, t-nuke_life+1), t+1)) <= max_nuke * total_capacity, f"NukeCapacityConstraint_{t}"

# Solve the problem
problem.solve()

# Gather results
coal_cap_added_results = [coal_cap_added[t].varValue for t in range(T)]
nuke_cap_added_results = [nuke_cap_added[t].varValue for t in range(T)]
total_cost = pulp.value(problem.objective)

# Formulate output
output = {
    "coal_cap_added": coal_cap_added_results,
    "nuke_cap_added": nuke_cap_added_results,
    "total_cost": total_cost,
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')