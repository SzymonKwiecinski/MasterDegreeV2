import pulp
import numpy as np

# Input data
data = {
    'N': 3,
    'Start': [100.0, 50.0, 200.0],
    'Limit': [1000.0, 200.0, 3000.0],
    'Rate': [
        [0.99, 0.9, 1.02],
        [0.95, 0.99, 0.92],
        [0.9, 0.91, 0.99]
    ]
}

N = data['N']
start = data['Start']
limit = data['Limit']
rate = np.array(data['Rate'])

# Define the problem
problem = pulp.LpProblem("Currency_Exchange_Problem", pulp.LpMaximize)

# Define decision variables
x = pulp.LpVariable.dicts("exchange", (range(N), range(N)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("final_amount", range(N), lowBound=0, cat='Continuous')

# Objective function: Maximize final amount of currency N
problem += y[N-1]

# Constraints for final amount of currency
for i in range(N):
    problem += y[i] == start[i] + pulp.lpSum(x[j][i] for j in range(N)) - pulp.lpSum(x[i][j] for j in range(N))

# Exchange limits
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N)) <= limit[i]
    problem += pulp.lpSum(x[j][i] for j in range(N)) <= limit[i]

# Transaction rates constraints
for i in range(N):
    for j in range(N):
        problem += x[i][j] <= start[i] * rate[i][j]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')