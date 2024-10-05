import pulp

# Extracting and defining the data from the JSON format
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

K = data['NumProducts']  # Number of products
S = data['NumMachines']  # Number of stages

produce_time = data['ProduceTime']  # Time required to produce one unit of product at each stage
time_available = data['AvailableTime']  # Available production time at each stage
profit = data['Profit']  # Profit for producing one unit of each product

# Creating a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Defining decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Defining the objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

# Defining constraints for each production stage
for s in range(S):
    problem += pulp.lpSum(produce_time[k][s] * quantity[k] for k in range(K)) <= time_available[s], f"Time_Constraint_Stage_{s}"

# Solving the problem
problem.solve()

# Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')