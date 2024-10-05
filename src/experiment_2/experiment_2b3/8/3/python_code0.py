import pulp

# Input data
data = {'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 
        'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 
        'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}

# Parameters
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100  # Convert percentage to a fraction
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create a LP problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision variables
coal_cap_added = [pulp.LpVariable(f"CoalCapAdded_{t}", lowBound=0, cat='Continuous') for t in range(T)]
nuke_cap_added = [pulp.LpVariable(f"NukeCapAdded_{t}", lowBound=0, cat='Continuous') for t in range(T)]

# Objective function - Minimize the total cost
problem += pulp.lpSum(coal_cost * coal_cap_added[t] + nuke_cost * nuke_cap_added[t] for t in range(T))

# Constraints
for t in range(T):
    # Calculate available coal and nuclear capacity in year t
    coal_capacity = sum(coal_cap_added[max(0, t - coal_life + 1):t + 1])
    nuke_capacity = sum(nuke_cap_added[max(0, t - nuke_life + 1):t + 1])
    
    # Total capacity must meet demand
    problem += oil_cap[t] + coal_capacity + nuke_capacity >= demand[t]
    
    # Max nuclear capacity constraint
    problem += nuke_capacity <= max_nuke * (oil_cap[t] + coal_capacity + nuke_capacity)

# Solve the problem
problem.solve()

# Prepare the output
coal_solution = [coal_cap_added[t].varValue for t in range(T)]
nuke_solution = [nuke_cap_added[t].varValue for t in range(T)]
total_cost = pulp.value(problem.objective)

result = {
    "coal_cap_added": coal_solution,
    "nuke_cap_added": nuke_solution,
    "total_cost": total_cost
}

# Print the result
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')