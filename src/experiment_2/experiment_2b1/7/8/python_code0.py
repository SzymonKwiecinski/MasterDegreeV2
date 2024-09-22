import pulp
import json

data = {'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}

# Extracting relevant data from the input
K = data['NumParts']  # Number of parts
S = data['NumMachines']  # Number of shops
time = data['Time']  # Time required for each part in each shop
profit = data['Profit']  # Profit for each part
capacity = data['Capacity']  # Capacity of each shop

# Creating a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Defining decision variables for the quantity of each part
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0, cat='Continuous')

# Objective function: Maximize total profit
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

# Adding capacity constraints for each shop
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s], f"Shop_Capacity_{s + 1}"

# Solving the problem
problem.solve()

# Preparing the output
output_quantity = [quantity[k].varValue for k in range(K)]
output = {"quantity": output_quantity}

# Print objective value
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')