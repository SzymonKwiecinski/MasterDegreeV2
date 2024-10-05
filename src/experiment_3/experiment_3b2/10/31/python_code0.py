import pulp
import json

# Data in JSON format
data = {'demand': [15000, 30000, 25000, 40000, 27000], 'num': [12, 10, 5], 'minlevel': [850, 1250, 1500], 'maxlevel': [2000, 1750, 4000], 'runcost': [1000, 2600, 3000], 'extracost': [2.0, 1.3, 3.0], 'startcost': [2000, 1000, 500]}

# Define the model
T = len(data['demand'])  # Number of time periods
K = len(data['num'])      # Number of generators

problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts('x', (range(K), range(1, T + 1)), lowBound=0, cat='Integer')  # Non-negative integers
p = pulp.LpVariable.dicts('p', (range(K), range(1, T + 1)), lowBound=0)  # Non-negative
y = pulp.LpVariable.dicts('y', (range(K), range(1, T + 1)), cat='Binary')  # Binary

# Objective Function
problem += pulp.lpSum(data['runcost'][k] * x[k][t] + data['extracost'][k] * p[k][t] + data['startcost'][k] * y[k][t] 
                       for k in range(K) for t in range(1, T + 1)), "Total_Cost"

# Constraints

# Meet demand for each period
for t in range(1, T + 1):
    problem += pulp.lpSum(x[k][t] * data['minlevel'][k] + p[k][t] for k in range(K)) >= data['demand'][t - 1], f"Demand_Constraint_{t}"

# Respect operational limits of generators
for k in range(K):
    for t in range(1, T + 1):
        problem += p[k][t] <= (x[k][t] * data['maxlevel'][k] - x[k][t] * data['minlevel'][k]), f"Operational_Limit_{k}_{t}"

# Generator availability
for k in range(K):
    for t in range(1, T + 1):
        problem += x[k][t] <= data['num'][k], f"Availability_{k}_{t}"

# Binary start-up constraint
for k in range(K):
    for t in range(2, T + 1):  # Start from t=2 because we need t-1
        problem += x[k][t] - x[k][t - 1] <= y[k][t], f"Startup_Constraint_{k}_{t}"

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')