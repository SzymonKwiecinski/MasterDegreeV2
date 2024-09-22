import pulp
import json

# Input data
data = {'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}

# Extracting parameters from the data
K = data['NumProducts']  # Number of products
S = data['NumMachines']   # Number of stages
produce_time = data['ProduceTime']  # Time required to produce each product at each stage
available_time = data['AvailableTime']  # Available time for each stage
profit = data['Profit']  # Profit for each product

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
quantity = pulp.LpVariable.dicts("Quantity", range(K), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += (pulp.lpSum(produce_time[k][s] * quantity[k] for k in range(K)) <= available_time[s]), f"Time_Constraint_{s+1}"

# Solve the problem
problem.solve()

# Output the results
result_quantity = [quantity[k].varValue for k in range(K)]
output = {"quantity": result_quantity}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')