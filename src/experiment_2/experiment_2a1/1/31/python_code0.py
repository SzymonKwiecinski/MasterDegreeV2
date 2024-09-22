import pulp
import json

# Input data
data = {'demand': [15000, 30000, 25000, 40000, 27000], 'num': [12, 10, 5], 'minlevel': [850, 1250, 1500], 'maxlevel': [2000, 1750, 4000], 'runcost': [1000, 2600, 3000], 'extracost': [2.0, 1.3, 3.0], 'startcost': [2000, 1000, 500]}

# Constants
T = len(data['demand'])
K = len(data['num'])

# Create the problem
problem = pulp.LpProblem("Power_Generation_Cost_Minimization", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, cat='Integer')
power_generated = pulp.LpVariable.dicts("power_generated", (range(K), range(T)), lowBound=0, cat='Continuous')
startup = pulp.LpVariable.dicts("startup", range(K), cat='Binary')

# Objective function
total_cost = pulp.lpSum([
    data['runcost'][k] * numon[k][t] + 
    data['extracost'][k] * (power_generated[k][t] - data['minlevel'][k]) * numon[k][t] +
    data['startcost'][k] * startup[k]
    for k in range(K) for t in range(T) if numon[k][t] > 0
])
problem += total_cost

# Constraints
for t in range(T):
    problem += pulp.lpSum([power_generated[k][t] for k in range(K)]) >= data['demand'][t], f"demand_constraint_{t}"
    
for k in range(K):
    for t in range(T):
        problem += power_generated[k][t] >= data['minlevel'][k] * numon[k][t], f"min_level_constraint_{k}_{t}"
        problem += power_generated[k][t] <= data['maxlevel'][k] * numon[k][t], f"max_level_constraint_{k}_{t}"
        problem += numon[k][t] <= data['num'][k], f"num_generators_constraint_{k}_{t}"
        
# Ensure startup only if at least one generator is on
for k in range(K):
    for t in range(T):
        problem += numon[k][t] <= startup[k] * data['num'][k], f"startup_constraint_{k}_{t}"

# Solve the problem
problem.solve()

# Prepare the output
numon_output = [[pulp.value(numon[k][t]) for t in range(T)] for k in range(K)]

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Format the output
output = {
    "numon": numon_output
}
print(json.dumps(output))