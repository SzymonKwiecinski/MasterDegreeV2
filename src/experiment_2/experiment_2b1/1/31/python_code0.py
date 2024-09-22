import pulp
import json

# Data provided in JSON format
data = {'demand': [15000, 30000, 25000, 40000, 27000], 
        'num': [12, 10, 5], 
        'minlevel': [850, 1250, 1500], 
        'maxlevel': [2000, 1750, 4000], 
        'runcost': [1000, 2600, 3000], 
        'extracost': [2.0, 1.3, 3.0], 
        'startcost': [2000, 1000, 500]}

# Constants
T = len(data['demand'])  # number of time periods
K = len(data['num'])      # number of generator types

# Create the problem
problem = pulp.LpProblem("PowerGeneration", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", 
                               ((k, t) for k in range(K) for t in range(T)), 
                               lowBound=0, 
                               upBound=data['num'][k], 
                               cat='Integer')

# Power produced by each generator type
power = pulp.LpVariable.dicts("power", 
                               ((k, t) for k in range(K) for t in range(T)), 
                               lowBound=0, 
                               upBound=data['maxlevel'][k], 
                               cat='Continuous')

# Objective function
total_cost = pulp.lpSum(data['runcost'][k] * numon[k, t] + 
                         pulp.lpSum(data['extracost'][k] * (power[k, t] - data['minlevel'][k]) * numon[k, t] 
                                     for k in range(K) if power[k, t] > data['minlevel'][k]) + 
                         data['startcost'][k] * (1 if numon[k, t] > 0 else 0) 
                         for k in range(K) for t in range(T))

problem += total_cost

# Constraints
for t in range(T):
    problem += pulp.lpSum(power[k, t] for k in range(K)) >= data['demand'][t], f"DemandConstraint_{t}"
    for k in range(K):
        problem += power[k, t] >= data['minlevel'][k] * numon[k, t], f"MinPowerConstraint_{k}_{t}"
        problem += power[k, t] <= data['maxlevel'][k] * numon[k, t], f"MaxPowerConstraint_{k}_{t}"

# Solve the problem
problem.solve()

# Get results
numon_result = [[pulp.value(numon[k, t]) for t in range(T)] for k in range(K)]

# Output the results
output = {
    "numon": numon_result
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')