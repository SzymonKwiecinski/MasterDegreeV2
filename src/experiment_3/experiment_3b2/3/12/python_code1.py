import pulp
import json

# Data input
data = {
    'N': 3,
    'Start': [100.0, 50.0, 200.0],
    'Limit': [1000.0, 200.0, 3000.0],
    'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]
}

# Parameters
N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Create the problem
problem = pulp.LpProblem("CurrencyExchange", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("exchange", (range(N), range(N)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(x[i][N-1] * rate[i][N-1] for i in range(N-1)) + start[N-1] - pulp.lpSum(x[N-1][j] for j in range(N-1)), "Total_Exchange"

# Constraints
# Initial amount constraints
for i in range(N):
    problem += (pulp.lpSum(x[i][j] for j in range(N) if j != i) - 
                 pulp.lpSum(x[k][i] / rate[k][i] for k in range(N) if k != i) <= start[i]), f"Initial_Amount_Constraint_{i}")

# Exchange limit constraints
for i in range(N):
    problem += (pulp.lpSum(x[i][j] for j in range(N) if j != i) + 
                 pulp.lpSum(x[k][i] / rate[k][i] for k in range(N) if k != i) <= limit[i]), f"Exchange_Limit_Constraint_{i}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')