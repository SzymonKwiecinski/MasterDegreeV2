import pulp

# Data
data = {
    'T': 12,
    'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35],
    'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5],
    'CoalCost': 10,
    'NukeCost': 5,
    'MaxNuke': 20,  # percentage
    'CoalLife': 5,
    'NukeLife': 10
}

# Variables
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100.0
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision Variables
coal_cap_added = pulp.LpVariable.dicts("CoalAdded", range(T), 0)
nuke_cap_added = pulp.LpVariable.dicts("NukeAdded", range(T), 0)

# Objective Function
total_cost = (pulp.lpSum(coal_cap_added[t] * coal_cost for t in range(T))
              + pulp.lpSum(nuke_cap_added[t] * nuke_cost for t in range(T)))

problem += total_cost

# Constraints
for t in range(T):
    # Capacity constraints: Oil + Coal + Nuke >= Demand
    existing_coal_cap = pulp.lpSum(coal_cap_added[max(0, t - l)] for l in range(coal_life) if t - l >= 0)
    existing_nuke_cap = pulp.lpSum(nuke_cap_added[max(0, t - l)] for l in range(nuke_life) if t - l >= 0)
    problem += (
        oil_cap[t] + existing_coal_cap + existing_nuke_cap >= demand[t],
        f"Capacity_Meet_Demand_{t}"
    )
    # Max nuclear capacity constraint
    problem += (
        existing_nuke_cap <= max_nuke * (oil_cap[t] + existing_coal_cap + existing_nuke_cap),
        f"Max_Nuke_Perc_{t}"
    )

# Solve the problem
problem.solve()

# Results
coal_cap_plan = [coal_cap_added[t].varValue for t in range(T)]
nuke_cap_plan = [nuke_cap_added[t].varValue for t in range(T)]
total_cost_value = pulp.value(problem.objective)

output = {
    "coal_cap_added": coal_cap_plan,
    "nuke_cap_added": nuke_cap_plan,
    "total_cost": total_cost_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')