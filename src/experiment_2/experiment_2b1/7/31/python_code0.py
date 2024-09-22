import pulp
import json

# Given data
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

# Extract data
T = len(data['demand'])  # Number of time periods
K = len(data['num'])     # Number of generator types

# Create the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), 0, None, pulp.LpInteger)
output_power = pulp.LpVariable.dicts("output_power", (range(K), range(T)), 0, None)

# Objective function
total_cost = pulp.lpSum(data['startcost'][k] * (numon[k][t] > 0) +
                         data['runcost'][k] * numon[k][t] +
                         data['extracost'][k] * (output_power[k][t] - data['minlevel'][k]) * numon[k][t]
                         for k in range(K) for t in range(T))

problem += total_cost

# Constraints
for t in range(T):
    # Demand satisfaction
    problem += (pulp.lpSum(output_power[k][t] for k in range(K)) == data['demand'][t], f"DemandConstraint_{t}")

    # Capacity constraints for each type of generator
    for k in range(K):
        problem += (output_power[k][t] >= data['minlevel'][k] * numon[k][t], f"MinLevelConstraint_{k}_{t}")
        problem += (output_power[k][t] <= data['maxlevel'][k] * numon[k][t], f"MaxLevelConstraint_{k}_{t}")
        
        # Total units constraint
        problem += (numon[k][t] <= data['num'][k], f"MaxUnitsConstraint_{k}")

# Solve the problem
problem.solve()

# Prepare output
numon_output = [[int(numon[k][t].varValue) for t in range(T)] for k in range(K)]

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output result
result = {
    "numon": numon_output
}

print(result)