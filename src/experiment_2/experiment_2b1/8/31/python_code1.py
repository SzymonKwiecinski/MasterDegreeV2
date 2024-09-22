import pulp
import json

# Input data
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

# Problem parameters
T = len(data['demand'])  # number of time periods
K = len(data['num'])      # number of generator types

# Create the LP problem
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), 0, None, pulp.LpInteger)  # number of generators on
power_output = pulp.LpVariable.dicts("power_output", (range(K), range(T)), 0, None)      # power output from each generator type

# Objective function
total_cost = pulp.lpSum(data['runcost'][k] * numon[k][t] + 
                         data['startcost'][k] * (pulp.lpSum(numon[k][t] for k in range(K) if t == 0)) + 
                         data['extracost'][k] * (power_output[k][t] - data['minlevel'][k]) * numon[k][t] 
                         for k in range(K) for t in range(T))
problem += total_cost

# Constraints
for t in range(T):
    problem += pulp.lpSum(numon[k][t] * data['minlevel'][k] for k in range(K)) <= data['demand'][t]
    problem += pulp.lpSum(numon[k][t] * data['maxlevel'][k] for k in range(K)) >= data['demand'][t]
    for k in range(K):
        problem += power_output[k][t] <= numon[k][t] * data['maxlevel'][k]
        problem += power_output[k][t] >= numon[k][t] * data['minlevel'][k] * (numon[k][t] > 0)

# Solve the problem
problem.solve()

# Output results
numon_result = [[pulp.value(numon[k][t]) for t in range(T)] for k in range(K)]

output = {
    "numon": numon_result
}

print(json.dumps(output))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')