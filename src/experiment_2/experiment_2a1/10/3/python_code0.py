import pulp
import json

data = {'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}

T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create the LP problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision variables for coal and nuclear capacity added each year
coal_capacity = pulp.LpVariable.dicts("CoalCapacity", range(T), lowBound=0, cat='Continuous')
nuke_capacity = pulp.LpVariable.dicts("NukeCapacity", range(T), lowBound=0, cat='Continuous')

# Objective function: minimize the total cost
problem += pulp.lpSum([coal_capacity[t] * coal_cost for t in range(T)]) + pulp.lpSum([nuke_capacity[t] * nuke_cost for t in range(T)])

# Constraints
for t in range(T):
    total_capacity = oil_cap[t] + pulp.lpSum([coal_capacity[j] for j in range(max(0, t-coal_life+1), t+1)]) + pulp.lpSum([nuke_capacity[j] for j in range(max(0, t-nuke_life+1), t+1)])
    
    # Demand constraint
    problem += total_capacity >= demand[t], f"DemandConstraint_{t}"
    
    # Nuclear capacity constraint
    if t >= nuke_life-1:
        problem += pulp.lpSum([nuke_capacity[j] for j in range(max(0, t-nuke_life+1), t+1)]) <= max_nuke * total_capacity, f"NuclearConstraint_{t}"

# Solve the problem
problem.solve()

# Collecting results
coal_cap_added = [coal_capacity[t].varValue for t in range(T)]
nuke_cap_added = [nuke_capacity[t].varValue for t in range(T)]
total_cost = pulp.value(problem.objective)

# Output the results
results = {
    "coal_cap_added": coal_cap_added,
    "nuke_cap_added": nuke_cap_added,
    "total_cost": total_cost,
}

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')
results