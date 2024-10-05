import pulp

# Parse the data
data = {'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 
        'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 
        'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}

T = data['T']
Demand = data['Demand']
OilCap = data['OilCap']
CoalCost = data['CoalCost']
NukeCost = data['NukeCost']
MaxNuke = data['MaxNuke'] / 100.0
CoalLife = data['CoalLife']
NukeLife = data['NukeLife']

# Initialization of LP problem
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

# Decision variables
CoalAdded = [pulp.LpVariable(f'coal_{t}', lowBound=0, cat='Continuous') for t in range(T)]
NukeAdded = [pulp.LpVariable(f'nuke_{t}', lowBound=0, cat='Continuous') for t in range(T)]

# Objective: Minimize capital cost
problem += pulp.lpSum([CoalAdded[t] * CoalCost + NukeAdded[t] * NukeCost for t in range(T)])

# Constraints
for t in range(T):
    # Capacity constraints
    coal_cap = pulp.lpSum([CoalAdded[i] for i in range(max(0, t - CoalLife + 1), t + 1)])
    nuke_cap = pulp.lpSum([NukeAdded[i] for i in range(max(0, t - NukeLife + 1), t + 1)])
    
    problem += (OilCap[t] + coal_cap + nuke_cap >= Demand[t], f"demand_constraint_year_{t}")

    # Nuclear capacity constraint
    problem += (nuke_cap <= MaxNuke * (OilCap[t] + coal_cap + nuke_cap), f"nuclear_cap_constraint_year_{t}")

# Solve the problem
problem.solve()

# Retrieve the results
coal_cap_added = [CoalAdded[t].varValue for t in range(T)]
nuke_cap_added = [NukeAdded[t].varValue for t in range(T)]
total_cost = pulp.value(problem.objective)

# Prepare the output
output = {
    "coal_cap_added": coal_cap_added,
    "nuke_cap_added": nuke_cap_added,
    "total_cost": total_cost,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')