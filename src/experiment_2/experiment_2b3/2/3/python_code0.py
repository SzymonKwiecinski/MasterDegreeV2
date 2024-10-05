import pulp

# Input data
data = {
    'T': 12,
    'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35],
    'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5],
    'CoalCost': 10,
    'NukeCost': 5,
    'MaxNuke': 20,
    'CoalLife': 5,
    'NukeLife': 10
}

# Unpack data
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create the LP problem
problem = pulp.LpProblem("Minimize_Capacity_Expansion_Cost", pulp.LpMinimize)

# Decision variables
coal_cap_added = pulp.LpVariable.dicts("Coal_Cap_Added", range(1, T + 1), lowBound=0, cat='Continuous')
nuke_cap_added = pulp.LpVariable.dicts("Nuke_Cap_Added", range(1, T + 1), lowBound=0, cat='Continuous')

# Objective function
problem += (
    pulp.lpSum(coal_cap_added[t] * coal_cost for t in range(1, T + 1)) +
    pulp.lpSum(nuke_cap_added[t] * nuke_cost for t in range(1, T + 1))
)

# Constraints
for t in range(1, T + 1):
    # Calculate existing coal and nuclear capacities
    total_coal = pulp.lpSum(coal_cap_added[tau] for tau in range(max(1, t - coal_life + 1), t + 1))
    total_nuke = pulp.lpSum(nuke_cap_added[tau] for tau in range(max(1, t - nuke_life + 1), t + 1))

    # Total capacity should meet demand
    problem += oil_cap[t - 1] + total_coal + total_nuke >= demand[t - 1]

    # Nuclear capacity constraint
    problem += total_nuke <= max_nuke * (oil_cap[t - 1] + total_coal + total_nuke)

# Solve the problem
problem.solve()

# Extract results
coal_solution = [coal_cap_added[t].varValue for t in range(1, T + 1)]
nuke_solution = [nuke_cap_added[t].varValue for t in range(1, T + 1)]
total_cost = pulp.value(problem.objective)

# Output format
output = {
    "coal_cap_added": coal_solution,
    "nuke_cap_added": nuke_solution,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')