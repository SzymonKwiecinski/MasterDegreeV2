import pulp
import json

# Input data in the provided JSON format
data = {'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}

# Setting up the problem
K = data['NumParts']  # Number of parts
S = data['NumMachines']  # Number of shops
time = data['Time']  # Time taken for each part in each shop
profit = data['Profit']  # Profit for each part
capacity = data['Capacity']  # Capacity of each shop

# Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables for quantity of each part
quantity = pulp.LpVariable.dicts("Quantity", range(K), lowBound=0, cat='Integer')

# Objective function: Maximize total profit
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

# Constraints: capacities for each shop
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_Shop_{s}"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "quantity": [pulp.value(quantity[k]) for k in range(K)]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')