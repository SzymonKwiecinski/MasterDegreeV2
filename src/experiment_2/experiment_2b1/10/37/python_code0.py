import pulp
import json

# Input data
data = {'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}

# Extracting data from the input JSON
time = data['time']
profit = data['profit']
capacity = data['capacity']

# Constants
K = len(profit)  # Number of parts
S = len(capacity)  # Number of shops

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: quantity of each spare part to be made
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Maximize total profit
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

# Constraints: Capacity constraints for each shop
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s], f"Capacity_Shop_{s+1}"

# Solve the problem
problem.solve()

# Extract the results
result_quantity = [quantity[k].varValue for k in range(K)]

# Output the result in the required format
output = {
    "quantity": result_quantity
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')