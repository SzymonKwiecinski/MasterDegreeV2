import pulp
import json

# Data from the input
data = {'demand': [15000, 30000, 25000, 40000, 27000], 
        'num': [12, 10, 5], 
        'minlevel': [850, 1250, 1500], 
        'maxlevel': [2000, 1750, 4000], 
        'runcost': [1000, 2600, 3000], 
        'extracost': [2.0, 1.3, 3.0], 
        'startcost': [2000, 1000, 500]}

# Parameters
T = len(data['demand'])
K = len(data['num'])

# Create the LP problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, upBound=max(data['num']), cat='Integer')
power = pulp.LpVariable.dicts("power", (range(K), range(T)), lowBound=0)

# Objective function
total_cost = pulp.lpSum([data['runcost'][k] * numon[k][t] + 
                          data['extracost'][k] * (power[k][t] - data['minlevel'][k]) * numon[k][t] +
                          (data['startcost'][k] if numon[k][t] > 0 else 0) 
                          for k in range(K) for t in range(T)])
problem += total_cost

# Constraints
for t in range(T):
    problem += pulp.lpSum([power[k][t] for k in range(K)]) >= data['demand'][t], f"Demand_Constraint_{t}"

for k in range(K):
    for t in range(T):
        problem += power[k][t] >= data['minlevel'][k] * numon[k][t], f"Min_Level_Constraint_k{K}_t{t}"
        problem += power[k][t] <= data['maxlevel'][k] * numon[k][t], f"Max_Level_Constraint_k{K}_t{t}"
        
# Solve the problem
problem.solve()

# Prepare output
numon_result = [[int(numon[k][t].varValue) for t in range(T)] for k in range(K)]

# Printing the result
result = {
    "numon": numon_result
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')