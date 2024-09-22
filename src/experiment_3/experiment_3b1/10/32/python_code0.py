import pulp

# Data from the provided JSON
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Sets
K = range(data['NumProducts'])  # Products
S = range(data['NumMachines'])   # Stages

# Parameters
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
q = pulp.LpVariable.dicts("q", K, lowBound=0)  # q[k] >= 0

# Objective Function
problem += pulp.lpSum(profit[k] * q[k] for k in K), "Total_Profit"

# Constraints
for s in S:
    problem += pulp.lpSum(produce_time[k][s] * q[k] for k in K) <= available_time[s], f"Time_Constraint_{s}"

# Solve the problem
problem.solve()

# Print the results
production_quantities = {f'quantity_{k}': q[k].varValue for k in K}
print(f'Production Quantities: {production_quantities}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')