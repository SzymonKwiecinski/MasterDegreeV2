import pulp
import json

# Data provided in JSON format
data = {
    'NumParts': 5, 
    'NumMachines': 2, 
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 
    'Profit': [30, 20, 40, 25, 10], 
    'Capacity': [700, 1000]
}

# Extracting data from JSON
NumParts = data['NumParts']
NumMachines = data['NumMachines']
Time = data['Time']
Profit = data['Profit']
Capacity = data['Capacity']

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(NumParts), lowBound=0)  # Quantity of parts to produce

# Objective function
problem += pulp.lpSum([Profit[k] * x[k] for k in range(NumParts)])

# Constraints
for s in range(NumMachines):
    problem += pulp.lpSum([Time[k][s] * x[k] for k in range(NumParts)]) <= Capacity[s]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')