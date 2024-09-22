import pulp
import json

# Input data (replace with the given data)
data = {'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}

# Extract data from the input
K = data['NumProducts']  # Number of products
S = data['NumMachines']   # Number of stages
produce_time = data['ProduceTime']  # Time to produce each product at each stage
available_time = data['AvailableTime']  # Available time for each stage
profit = data['Profit']  # Profit for each product

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: quantity of each product to produce
quantity = pulp.LpVariable.dicts("Quantity", range(K), lowBound=0, cat='Continuous')

# Objective function: maximize total profit
problem += pulp.lpSum([profit[k] * quantity[k] for k in range(K)]), "Total_Profit"

# Constraints for each stage
for s in range(S):
    problem += pulp.lpSum([produce_time[k][s] * quantity[k] for k in range(K)]) <= available_time[s], f"Available_Time_Stage_{s+1}"

# Solve the problem
problem.solve()

# Output results
quantities = [quantity[k].varValue for k in range(K)]
output = {"quantity": quantities}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')