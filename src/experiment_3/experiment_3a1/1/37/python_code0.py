import pulp
import json

# Load data from a JSON format string
data = json.loads('{"time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], "profit": [30, 20, 40, 25, 10], "capacity": [700, 1000]}')

# Define the sets
K = len(data['profit'])  # Total number of spare parts
S = len(data['capacity'])  # Number of shops

# Create the problem variable
problem = pulp.LpProblem("Spare_Parts_Production", pulp.LpMaximize)

# Define decision variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

# Define the objective function
problem += pulp.lpSum(data['profit'][k] * quantity[k] for k in range(K)), "Total_Profit"

# Add constraints for each shop
for s in range(S):
    problem += (pulp.lpSum(data['time'][k][s] * quantity[k] for k in range(K)) <= data['capacity'][s]), f"Capacity_Constraint_{s}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')