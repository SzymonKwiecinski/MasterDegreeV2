import pulp

# Data from the JSON format
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Sets and parameters
K = data['NumProducts']
S = data['NumMachines']
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

# Create the problem variable
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(produce_time[k][s] * x[k] for k in range(K)) <= available_time[s], f"Time_Constraint_{s+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')