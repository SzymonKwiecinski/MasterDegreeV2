import pulp

# Data from the JSON format
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Number of products and machines
K = data['NumProducts']
S = data['NumMachines']

# Unpack data
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

# Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: Quantity produced of each product
q = [pulp.LpVariable(f'q_{k+1}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function: Maximize total profit
problem += pulp.lpSum(profit[k] * q[k] for k in range(K)), "Total_Profit"

# Constraints: Time constraints for each machine
for s in range(S):
    problem += pulp.lpSum(produce_time[k][s] * q[k] for k in range(K)) <= available_time[s], f"Time_constraint_s{s+1}"

# Solve the problem
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')