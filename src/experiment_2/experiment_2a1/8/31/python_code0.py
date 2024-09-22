import pulp
import json

# Given data
data = {'demand': [15000, 30000, 25000, 40000, 27000], 
        'num': [12, 10, 5], 
        'minlevel': [850, 1250, 1500], 
        'maxlevel': [2000, 1750, 4000], 
        'runcost': [1000, 2600, 3000], 
        'extracost': [2.0, 1.3, 3.0], 
        'startcost': [2000, 1000, 500]}

# Extract data
demand = data['demand']
num_generators = data['num']
min_level = data['minlevel']
max_level = data['maxlevel']
run_cost = data['runcost']
extra_cost = data['extracost']
start_cost = data['startcost']

# Number of periods (T) and types of generators (K)
T = len(demand)
K = len(num_generators)

# Create the problem
problem = pulp.LpProblem("Generation_Cost_Minimization", pulp.LpMinimize)

# Decision variables
num_on = pulp.LpVariable.dicts("num_on", (range(K), range(T)), lowBound=0, upBound=[num_generators[k] for k in range(K)], cat='Integer')
output_power = pulp.LpVariable.dicts("output_power", (range(K), range(T)), lowBound=0)

# Objective function
total_cost = pulp.lpSum(num_on[k][t] * (start_cost[k] + run_cost[k] + 
                    extra_cost[k] * (output_power[k][t] - min_level[k])) for k in range(K) for t in range(T))
problem += total_cost

# Constraints
for t in range(T):
    problem += pulp.lpSum(output_power[k][t] for k in range(K)) >= demand[t], f"Demand_constraint_{t}"

    for k in range(K):
        problem += output_power[k][t] >= min_level[k] * num_on[k][t], f"Min_level_constraint_{k}_{t}"
        problem += output_power[k][t] <= max_level[k] * num_on[k][t], f"Max_level_constraint_{k}_{t}"

# Solve the problem
problem.solve()

# Prepare output
numon = [[pulp.value(num_on[k][t]) for t in range(T)] for k in range(K)]

output_result = {
    "numon": numon
}

print(json.dumps(output_result, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')