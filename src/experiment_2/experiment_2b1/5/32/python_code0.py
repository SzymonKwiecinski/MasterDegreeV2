import pulp
import json

# Input data in JSON format
data = {'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}

# Extracting data from the input
K = data['NumProducts']  # Number of products
S = data['NumMachines']   # Number of stages
produce_time = data['ProduceTime']  # Production time matrix
available_time = data['AvailableTime']  # Available time for stages
profit = data['Profit']  # Profit per product

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: quantity to produce for each product
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0, cat='Continuous')

# Objective function: Maximize total profit
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += (pulp.lpSum(produce_time[k][s] * quantity[k] for k in range(K)) <= available_time[s]), f"Available_Time_Stage_{s+1}"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "quantity": [quantity[k].varValue for k in range(K)]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')