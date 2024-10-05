import pulp

# Data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 
        'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Problem
problem = pulp.LpProblem("Currency_Exchange", pulp.LpMaximize)

# Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), lowBound=0, cat='Continuous')

# Objective Function
final_currency_N = start[N-1] + pulp.lpSum(x[i, N-1] for i in range(N)) - pulp.lpSum(x[N-1, j] for j in range(N))
problem += final_currency_N

# Constraints
# Exchange Limits
for i in range(N):
    problem += pulp.lpSum(x[i, j] for j in range(N)) <= limit[i]

# Initial Amounts
for i in range(N):
    problem += start[i] - pulp.lpSum(x[i, j] for j in range(N)) + pulp.lpSum(x[j, i] for j in range(N)) >= 0

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')