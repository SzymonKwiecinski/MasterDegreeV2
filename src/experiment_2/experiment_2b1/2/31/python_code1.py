import pulp
import json

# Input data in JSON format
data = json.loads("{'demand': [15000, 30000, 25000, 40000, 27000], 'num': [12, 10, 5], 'minlevel': [850, 1250, 1500], 'maxlevel': [2000, 1750, 4000], 'runcost': [1000, 2600, 3000], 'extracost': [2.0, 1.3, 3.0], 'startcost': [2000, 1000, 500]}")

# Extracting data from the input
demand = data['demand']
num_units = data['num']
min_level = data['minlevel']
max_level = data['maxlevel']
run_cost = data['runcost']
extra_cost = data['extracost']
start_cost = data['startcost']

T = len(demand)  # Number of time periods
K = len(num_units)  # Number of generator types

# Create the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
num_on = pulp.LpVariable.dicts("num_on", (range(K), range(T)), lowBound=0, upBound=None, cat='Integer')
power_generated = pulp.LpVariable.dicts("power_generated", (range(K), range(T)), lowBound=0, upBound=None, cat='Continuous')

# Objective function
total_cost = pulp.lpSum(
    start_cost[k] * (num_on[k][t] > 0) + run_cost[k] + extra_cost[k] * (power_generated[k][t] - min_level[k]) * num_on[k][t]
    for k in range(K) for t in range(T)
)
problem += total_cost

# Constraints
for t in range(T):
    problem += pulp.lpSum(num_on[k][t] * min_level[k] for k in range(K)) <= demand[t], f"Demand_Constraint_{t}"
    for k in range(K):
        problem += num_on[k][t] <= num_units[k], f"Max_Unit_Constraint_{k}_{t}"
        problem += power_generated[k][t] <= max_level[k] * num_on[k][t], f"Max_Generation_Constraint_{k}_{t}"
        problem += power_generated[k][t] >= min_level[k] * num_on[k][t], f"Min_Generation_Constraint_{k}_{t}"

# Solve the problem
problem.solve()

# Output result
numon = [[pulp.value(num_on[k][t]) for t in range(T)] for k in range(K)]

result = {
    "numon": numon
}

# Print Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')