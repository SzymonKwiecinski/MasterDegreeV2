import pulp

# Data based on the given JSON
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Number of different spare parts (K) and shops (S)
K = len(data['profit'])
S = len(data['capacity'])

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
quantity = [pulp.LpVariable(f"quantity_{k}", lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
total_profit = pulp.lpSum(data['profit'][k] * quantity[k] for k in range(K))
problem += total_profit, "Total_Profit"

# Constraints
for s in range(S):
    problem += (pulp.lpSum(data['time'][k][s] * quantity[k] for k in range(K)) <= data['capacity'][s]), f"Capacity_Constraint_Shop_{s}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')