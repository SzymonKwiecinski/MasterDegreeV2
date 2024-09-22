import pulp
import json

# Load data from JSON format
data = {'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 
        'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 
        'CoalCost': 10, 'NukeCost': 5, 
        'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}

# Parameters
T = data['T']
demand = data['Demand']
oil_capacity = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Define the problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision Variables
coal = pulp.LpVariable.dicts("Coal", range(T), lowBound=0)
nuke = pulp.LpVariable.dicts("Nuke", range(T), lowBound=0)

# Objective Function
problem += pulp.lpSum(coal_cost * coal[t] + nuke_cost * nuke[t] for t in range(T)), "Total_Cost"

# Constraints
for t in range(T):
    # Total capacity must meet or exceed demand
    problem += (oil_capacity[t] + 
                 pulp.lpSum(coal[t-j] for j in range(min(t, coal_life))) + 
                 pulp.lpSum(nuke[t-j] for j in range(min(t, nuke_life))) >= demand[t], 
                 f"Demand_Constraint_{t}")
    
    # Proportion of nuclear capacity must not exceed max_nuke percentage
    total_capacity = (oil_capacity[t] + 
                      pulp.lpSum(coal[t-j] for j in range(min(t, coal_life))) + 
                      pulp.lpSum(nuke[t-j] for j in range(min(t, nuke_life))))
    
    # Solve the comparison by using a constraint directly instead of an if statement
    problem += (total_capacity > 0) >> (pulp.lpSum(nuke[t-j] for j in range(min(t, nuke_life))) / total_capacity <= max_nuke / 100), f"Nuclear_Capacity_Constraint_{t}")

# Solve the problem
problem.solve()

# Outputs
coal_cap_added = [coal[t].varValue for t in range(T)]
nuke_cap_added = [nuke[t].varValue for t in range(T)]
total_cost = pulp.value(problem.objective)

# Print the results
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')
print(f'Coal Capacity Added: {coal_cap_added}')
print(f'Nuclear Capacity Added: {nuke_cap_added}')