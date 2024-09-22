import pulp
import json

# Load data from JSON format
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

# Create the problem variable
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision Variables
coal = pulp.LpVariable.dicts("coal", range(T), lowBound=0, cat='Continuous')
nuke = pulp.LpVariable.dicts("nuke", range(T), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(coal_cost * coal[t] + nuke_cost * nuke[t] for t in range(T))

# Capacity demand constraints
for t in range(T):
    problem += (oil_capacity[t] +
                 pulp.lpSum(coal[t-j] for j in range(1, min(t, coal_life) + 1)) +
                 pulp.lpSum(nuke[t-j] for j in range(1, min(t, nuke_life) + 1)) >= demand[t])

# Maximum nuclear capacity constraint
for t in range(T):
    problem += (pulp.lpSum(coal[t-j] for j in range(1, min(t, coal_life) + 1)) +
                 pulp.lpSum(nuke[t-j] for j in range(1, min(t, nuke_life) + 1)) * (nuke_cost / coal_cost) <= 
                 (max_nuke / 100) * (oil_capacity[t] +
                 pulp.lpSum(coal[t-j] for j in range(1, min(t, coal_life) + 1)) +
                 pulp.lpSum(nuke[t-j] for j in range(1, min(t, nuke_life) + 1))))

# Solve the problem
problem.solve()

# Prepare output
coal_capacity_added = [coal[t].varValue for t in range(T)]
nuke_capacity_added = [nuke[t].varValue for t in range(T)]
total_cost = pulp.value(problem.objective)

# Print results
print(f'Coal capacity added each year: {coal_capacity_added}')
print(f'Nuclear capacity added each year: {nuke_capacity_added}')
print(f'Total cost of capacity expansion: <OBJ>{total_cost}</OBJ>')