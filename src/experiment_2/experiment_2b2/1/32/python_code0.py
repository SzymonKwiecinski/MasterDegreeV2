import pulp

# Input data
data = {
    'NumProducts': 2, 
    'NumMachines': 2, 
    'ProduceTime': [[1, 3], [2, 1]], 
    'AvailableTime': [200, 100], 
    'Profit': [20, 10]
}

# Extracting parameters from data
K = data['NumProducts']
S = data['NumMachines']
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

# Define the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: Quantity of each product to produce
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Maximize total profit
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K))

# Constraints: Time available for each machine should not be exceeded
for s in range(S):
    problem += pulp.lpSum(produce_time[k][s] * quantity[k] for k in range(K)) <= available_time[s], f"Time_Constraint_{s}"

# Solve the problem
problem.solve()

# Output quantities to produce for each product
quantity_output = [quantity[k].varValue for k in range(K)]

output = {
    "quantity": quantity_output
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')