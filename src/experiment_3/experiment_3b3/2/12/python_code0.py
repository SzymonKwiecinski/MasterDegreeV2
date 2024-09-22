import pulp

# Problem data
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
rate = data['Rate']

# Define the problem
problem = pulp.LpProblem("Maximize_Final_Amount_of_Currency", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), lowBound=0)

# Final amount variables
final = pulp.LpVariable.dicts("final", (i for i in range(N)), lowBound=0)

# Objective function: Maximize final amount of currency N
problem += final[N-1], "Maximize_final_currency_N"

# Constraints

# Initial amounts (constraint 1)
for i in range(N):
    problem += final[i] == start[i] + sum(x[j, i] for j in range(N)) - sum(x[i, j] for j in range(N)), f"Initial_Amount_of_currency_{i}"

# Exchange limits (constraint 2)
for i in range(N):
    problem += sum(x[i, j] for j in range(N)) <= limit[i], f"Exchange_Limit_Outgoing_{i}"
    problem += sum(x[j, i] for j in range(N)) <= limit[i], f"Exchange_Limit_Incoming_{i}"

# Rate constraints (constraint 3)
for i in range(N):
    for j in range(N):
        problem += x[i, j] * rate[i][j] <= final[j], f"Rate_Constraint_{i}_{j}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')