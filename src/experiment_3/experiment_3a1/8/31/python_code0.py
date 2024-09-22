import pulp
import json

# Load data from JSON format
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

# Define parameters
T = len(data['demand'])  # Total number of time periods
K = len(data['num'])     # Total number of generator types

# Create the problem variable
problem = pulp.LpProblem("Power_Generation_Optimization", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", ((k, t) for k in range(K) for t in range(T)), cat='Binary')

# Objective function
problem += pulp.lpSum(
    (data['runcost'][k] * numon[k, t] + data['startcost'][k] * y[k, t] +
     pulp.lpSum(data['extracost'][k] * p for p in range(data['minlevel'][k] if numon[k, t] > 0 else 0, 
                                                          data['maxlevel'][k] + 1) if numon[k, t] > 0) 
    )
    for k in range(K) for t in range(T)
), "Total_Cost"

# Constraints
# Demand must be met
for t in range(T):
    problem += pulp.lpSum(numon[k, t] for k in range(K)) >= data['demand'][t], f"Demand_Constraint_{t}"

# Power output relation
for k in range(K):
    for t in range(T):
        problem += numon[k, t] >= data['minlevel'][k] * y[k, t], f"Min_Level_Constraint_{k}_{t}"
        problem += numon[k, t] <= data['maxlevel'][k] * y[k, t], f"Max_Level_Constraint_{k}_{t}"

# Available generators
for k in range(K):
    for t in range(T):
        problem += numon[k, t] <= data['num'][k], f"Available_Generator_Constraint_{k}_{t}"

# Solve the problem
problem.solve()

# Output results
numon_result = [[pulp.value(numon[k, t]) for t in range(T)] for k in range(K)]
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Output: {{"numon": {numon_result}}}')