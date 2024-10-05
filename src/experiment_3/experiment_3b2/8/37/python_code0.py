import pulp
import json

# Load data from the provided JSON format
data = json.loads('{"time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], "profit": [30, 20, 40, 25, 10], "capacity": [700, 1000]}')

# Set up the problem
K = len(data['profit'])   # Number of spare parts
S = len(data['capacity'])  # Number of shops

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(data['profit'][k] * quantity[k] for k in range(K))

# Constraints for each shop
for s in range(S):
    problem += pulp.lpSum(data['time'][k][s] * quantity[k] for k in range(K)) <= data['capacity'][s]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')