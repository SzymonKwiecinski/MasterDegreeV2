import pulp

# Reading data
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

# Assign data to variables
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100.0  # convert percentage to fraction
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create the LP problem
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

# Decision variables
coal_cap_added = [pulp.LpVariable(f"coal_cap_added_{t}", lowBound=0) for t in range(T)]
nuke_cap_added = [pulp.LpVariable(f"nuke_cap_added_{t}", lowBound=0) for t in range(T)]

# Objective function: Minimize the total cost
total_cost = pulp.lpSum([coal_cost * coal_cap_added[t] + nuke_cost * nuke_cap_added[t] for t in range(T)])
problem += total_cost

# Constraints
for t in range(T):
    # Capacity needs to meet demand for each year
    coal_capacity = pulp.lpSum(coal_cap_added[max(0, t - coal_life + 1):t + 1])
    nuke_capacity = pulp.lpSum(nuke_cap_added[max(0, t - nuke_life + 1):t + 1])
    total_capacity = oil_cap[t] + coal_capacity + nuke_capacity
    problem += (total_capacity >= demand[t], f"Capacity_Constraint_{t}")

    # Nuclear capacity must not exceed max_nuke percentage of the total capacity
    problem += (nuke_capacity <= max_nuke * total_capacity, f"Nuke_Percentage_Constraint_{t}")

# Solve the problem
problem.solve()

# Extract the results
coal_cap_added_solution = [pulp.value(coal_cap_added[t]) for t in range(T)]
nuke_cap_added_solution = [pulp.value(nuke_cap_added[t]) for t in range(T)]
total_cost_solution = pulp.value(problem.objective)

# Output
solution = {
    "coal_cap_added": coal_cap_added_solution,
    "nuke_cap_added": nuke_cap_added_solution,
    "total_cost": total_cost_solution
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')