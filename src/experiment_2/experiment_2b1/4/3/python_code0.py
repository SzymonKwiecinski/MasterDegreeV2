import pulp
import json

data = {'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 
        'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 
        'CoalCost': 10, 
        'NukeCost': 5, 
        'MaxNuke': 20, 
        'CoalLife': 5, 
        'NukeLife': 10}

T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Define the problem
problem = pulp.LpProblem("ElectricityCapacityExpansion", pulp.LpMinimize)

# Define variables
coal_capacity_added = pulp.LpVariable.dicts("CoalCapacityAdded", range(T), lowBound=0, cat='Continuous')
nuclear_capacity_added = pulp.LpVariable.dicts("NuclearCapacityAdded", range(T), lowBound=0, cat='Continuous')

# Define the objective function
problem += pulp.lpSum(coal_cost * coal_capacity_added[t] + nuke_cost * nuclear_capacity_added[t] for t in range(T))

# Constraints for each year
for t in range(T):
    total_capacity = oil_cap[t] + pulp.lpSum(coal_capacity_added[i] for i in range(max(0, t - coal_life + 1), t + 1)) + \
                  pulp.lpSum(nuclear_capacity_added[j] for j in range(max(0, t - nuke_life + 1), t + 1))
    
    problem += total_capacity >= demand[t], f"DemandConstraint_{t}"

# Nuclear capacity percentage constraint
for t in range(T):
    total_capacity = oil_cap[t] + pulp.lpSum(coal_capacity_added[i] for i in range(max(0, t - coal_life + 1), t + 1)) + \
                  pulp.lpSum(nuclear_capacity_added[j] for j in range(max(0, t - nuke_life + 1), t + 1))
    
    nuclear_capacity = pulp.lpSum(nuclear_capacity_added[j] for j in range(max(0, t - nuke_life + 1), t + 1))
    
    problem += nuclear_capacity <= max_nuke * total_capacity, f"NuclearCapacityConstraint_{t}"

# Solve the problem
problem.solve()

# Prepare the output
coal_cap_added = [coal_capacity_added[t].varValue for t in range(T)]
nuke_cap_added = [nuclear_capacity_added[t].varValue for t in range(T)]
total_cost = pulp.value(problem.objective)

output = {
    "coal_cap_added": coal_cap_added,
    "nuke_cap_added": nuke_cap_added,
    "total_cost": total_cost,
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')