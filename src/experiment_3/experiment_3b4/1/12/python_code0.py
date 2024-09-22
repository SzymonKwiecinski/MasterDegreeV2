import pulp

# Data
data = {
    'N': 3,
    'Start': [100.0, 50.0, 200.0],
    'Limit': [1000.0, 200.0, 3000.0],
    'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]
}

N = data['N']
Start = data['Start']
Limit = data['Limit']
Rate = data['Rate']

# Problem
problem = pulp.LpProblem("Maximize_Exchange", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), lowBound=0, cat='Continuous')

# Objective Function
objective = (
    pulp.lpSum(x[i, N-1] * Rate[i][N-1] for i in range(N-1)) 
    + Start[N-1] 
    - pulp.lpSum(x[N-1, j] for j in range(N-1))
)
problem += objective

# Constraints

# Currency Balance Constraints
for i in range(N):
    problem += (
        pulp.lpSum(x[i, j] for j in range(N)) 
        <= Start[i] + pulp.lpSum(x[k, i] * Rate[k][i] for k in range(N))
    )

# Limit Constraints
for i in range(N):
    problem += (
        pulp.lpSum(x[i, j] for j in range(N)) 
        <= Limit[i]
    )

# Solve
problem.solve()

# Output Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')