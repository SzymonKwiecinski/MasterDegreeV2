import json
import pulp

# Input data
data = {'demand': [15000, 30000, 25000, 40000, 27000], 
        'num': [12, 10, 5], 
        'minlevel': [850, 1250, 1500], 
        'maxlevel': [2000, 1750, 4000], 
        'runcost': [1000, 2600, 3000], 
        'extracost': [2.0, 1.3, 3.0], 
        'startcost': [2000, 1000, 500]}

# Parameters
T = len(data['demand'])  # Number of time periods
K = len(data['num'])      # Number of generator types

# Create the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, upBound=None, cat='Integer')
output = pulp.LpVariable.dicts("output", (range(K), range(T)), lowBound=0, upBound=None, cat='Continuous')

# Objective function
total_cost = pulp.lpSum([data['startcost'][k] * (numon[k][t] > 0) + 
                           data['runcost'][k] * numon[k][t] + 
                           data['extracost'][k] * (output[k][t] - data['minlevel'][k]) 
                           for k in range(K) for t in range(T)])
problem += total_cost

# Constraints
for t in range(T):
    problem += pulp.lpSum([numon[k][t] * data['maxlevel'][k] for k in range(K)]) >= data['demand'][t], f"Demand_Constraint_{t}"

    for k in range(K):
        problem += output[k][t] == numon[k][t] * data['maxlevel'][k], f"Output_Definition_{k}_{t}"
        problem += output[k][t] >= data['minlevel'][k] * numon[k][t], f"Min_Level_Constraint_{k}_{t}"
        problem += output[k][t] <= data['maxlevel'][k] * numon[k][t], f"Max_Level_Constraint_{k}_{t}"
        problem += numon[k][t] <= data['num'][k], f"Availability_Constraint_{k}_{t}"

# Solve the problem
problem.solve()

# Prepare the output
numon_solution = [[int(numon[k][t].value()) for t in range(T)] for k in range(K)]

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the result
result = {
    "numon": numon_solution
}

print(result)