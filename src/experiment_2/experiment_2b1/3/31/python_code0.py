import pulp
import json

# Input data
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

# Create the problem
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Decision Variables
num_on = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), 
                                     lowBound=0, upBound=None, cat='Integer')

# Objective Function
total_cost = pulp.lpSum((data['runcost'][k] + data['extracost'][k] * (num_on[k, t] * data['minlevel'][k] - data['minlevel'][k])) * (num_on[k, t] > 0) +
                         data['startcost'][k] * (num_on[k, t] > 0) for k in range(K) for t in range(T))
problem += total_cost

# Constraints
for t in range(T):
    problem += pulp.lpSum(num_on[k, t] * data['minlevel'][k] for k in range(K)) >= data['demand'][t], f"Demand_Constraint_{t}"

for k in range(K):
    for t in range(T):
        problem += num_on[k, t] <= data['num'][k], f"Capacity_Constraint_k{K}_t{T}"

# Solve the problem
problem.solve()

# Prepare result
result = {
    "numon": [[int(num_on[k, t].varValue) for t in range(T)] for k in range(K)]
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')