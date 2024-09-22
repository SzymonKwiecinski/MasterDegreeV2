import json
import pulp

# Given data in JSON format
data_json = '{"time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], "profit": [30, 20, 40, 25, 10], "capacity": [700, 1000]}'
data = json.loads(data_json)

# Extract data from the loaded JSON
time = data['time']
profit = data['profit']
capacity = data['capacity']

# Number of parts and shops
K = len(profit)
S = len(capacity)

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_{s}"

# Solve the problem
problem.solve()

# Extracting the results
result_quantity = [quantity[k].varValue for k in range(K)]

# Print the objective value and the quantities
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
output = {"quantity": result_quantity}
print(output)