import pulp

# Data from JSON
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Problem
problem = pulp.LpProblem("Currency_Exchange", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N) if i != j), lowBound=0)

# Objective Function
problem += pulp.lpSum(rate[i][N-1] * x[i, N-1] for i in range(N-1)), "Objective"

# Constraints
for i in range(N):
    # Supply constraints
    for j in range(N):
        if i != j:
            problem += x[i, j] <= start[i], f"Supply_Constraint_{i}_{j}"
    
    # Exchange limits
    problem += (
        pulp.lpSum(x[i, j] for j in range(N) if i != j) +
        pulp.lpSum(x[j, i] / rate[j][i] for j in range(N) if i != j)
        <= limit[i], f"Exchange_Limit_{i}"
    )
    
    # Initial and Balance Constraints
    problem += (
        pulp.lpSum(x[j, i] * rate[j][i] for j in range(N) if i != j) -
        pulp.lpSum(x[i, j] for j in range(N) if i != j)
        == start[i], f"Balance_Constraint_{i}"
    )

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')