import pulp

# Data
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Initialize the problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Create decision variables
x = pulp.LpVariable.dicts("x", range(data['NumProducts']), lowBound=0)

# Objective function
problem += pulp.lpSum(data['Profit'][k] * x[k] for k in range(data['NumProducts'])), "Total_Profit"

# Constraints
for m in range(data['NumMachines']):
    problem += pulp.lpSum(data['ProduceTime'][k][m] * x[k] for k in range(data['NumProducts'])) <= data['AvailableTime'][m], f"Machine_Capacity_{m}"

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')