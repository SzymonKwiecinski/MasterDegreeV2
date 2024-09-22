import pulp

# Data obtained from the JSON
data = {
    'NumProducts': 2, 
    'NumMachines': 2, 
    'ProduceTime': [[1, 3], [2, 1]], 
    'AvailableTime': [200, 100], 
    'Profit': [20, 10]
}

# Number of products
K = data['NumProducts']
# Number of stages
S = data['NumMachines']
# Time required to produce one unit of each product at each stage
produce_time = data['ProduceTime']
# Available time at each stage
available_time = data['AvailableTime']
# Profit for each product
profit = data['Profit']

# Create the problem variable to contain the problem data
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{k}", lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K))

# Constraints
for s in range(S):
    problem += pulp.lpSum(produce_time[k][s] * x[k] for k in range(K)) <= available_time[s]

# Solve the problem
problem.solve()

# Print the results
quantity = [pulp.value(x[k]) for k in range(K)]
print("Quantity produced for each product:", quantity)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')