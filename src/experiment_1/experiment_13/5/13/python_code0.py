import pulp
import json

# Data in JSON format
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 
    'profit': [30, 20, 40, 25, 10], 
    'capacity': [700, 1000]
}

# Parameters
K = len(data['profit'])  # Number of different spare parts
S = len(data['capacity'])  # Number of machines

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("SparePart", range(K), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['profit'][k] * x[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += (pulp.lpSum(data['time'][k][s] * x[k] for k in range(K)) <= data['capacity'][s]), f"Machine_Capacity_{s}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')