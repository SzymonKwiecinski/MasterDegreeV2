import pulp
import json

# Input data in JSON format
data_json = "{'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}"
data = json.loads(data_json.replace("'", "\""))

# Extract data
K = data['NumProducts']  # Number of products
S = data['NumMachines']   # Number of stages (machines)
produce_time = data['ProduceTime']  # Produce time for each product and stage
available_time = data['AvailableTime']  # Available time for each stage
profit = data['Profit']  # Profit for each product

# Problem setup
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(produce_time[k][s] * quantity[k] for k in range(K)) <= available_time[s], f"Available_Time_Constraint_{s}"

# Solve the problem
problem.solve()

# Output the results
result_quantity = [quantity[k].varValue for k in range(K)]
output = {"quantity": result_quantity}

# Printing the output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')