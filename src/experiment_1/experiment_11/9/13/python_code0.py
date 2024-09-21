import pulp

# Data from JSON
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Number of spare parts and machines
K = len(data['profit'])
S = len(data['capacity'])

# Create the problem variable
problem = pulp.LpProblem("Optimal_Production_of_Spare_Parts", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['profit'][k] * x[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(data['time'][k][s] * x[k] for k in range(K)) <= data['capacity'][s], f"Capacity_Constraint_{s+1}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')