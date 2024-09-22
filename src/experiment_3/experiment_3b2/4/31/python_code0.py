import pulp
import json

# Load data from JSON format
data = json.loads('{"demand": [15000, 30000, 25000, 40000, 27000], "num": [12, 10, 5], "minlevel": [850, 1250, 1500], "maxlevel": [2000, 1750, 4000], "runcost": [1000, 2600, 3000], "extracost": [2.0, 1.3, 3.0], "startcost": [2000, 1000, 500]}')

# Define sets and parameters
T = len(data['demand'])
K = len(data['num'])
demand_t = data['demand']
num_k = data['num']
minlevel_k = data['minlevel']
maxlevel_k = data['maxlevel']
runcost_k = data['runcost']
extracost_k = data['extracost']
startcost_k = data['startcost']

# Create the problem
problem = pulp.LpProblem("Electricity_Load_Demand_Optimization", pulp.LpMinimize)

# Decision Variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), 0, None, pulp.LpInteger)
power = pulp.LpVariable.dicts("power", (range(K), range(T)), 0)
start = pulp.LpVariable.dicts("start", (range(K), range(T)), cat='Binary')

# Objective Function
problem += pulp.lpSum(
    runcost_k[k] * numon[k][t] + 
    extracost_k[k] * (power[k][t] - numon[k][t] * minlevel_k[k]) 
    for k in range(K) for t in range(T)
) + pulp.lpSum(startcost_k[k] * start[k][t] for k in range(K) for t in range(T))

# Constraints
for t in range(T):
    problem += pulp.lpSum(power[k][t] for k in range(K)) >= demand_t[t], f"demand_constraint_{t}"

for k in range(K):
    for t in range(T):
        problem += numon[k][t] * minlevel_k[k] <= power[k][t], f"min_power_constraint_{k}_{t}"
        problem += power[k][t] <= numon[k][t] * maxlevel_k[k], f"max_power_constraint_{k}_{t}"

for k in range(K):
    for t in range(1, T):
        problem += start[k][t] >= numon[k][t] - numon[k][t-1], f"start_constraint_{k}_{t}"

for k in range(K):
    for t in range(T):
        problem += numon[k][t] <= num_k[k], f"capacity_constraint_{k}_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')