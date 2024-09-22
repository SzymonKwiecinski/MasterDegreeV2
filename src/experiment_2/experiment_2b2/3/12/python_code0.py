import pulp

# Data
data = {
    'N': 3, 
    'Start': [100.0, 50.0, 200.0], 
    'Limit': [1000.0, 200.0, 3000.0], 
    'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]
}

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Create LP problem
problem = pulp.LpProblem("Currency_Exchange_Maximization", pulp.LpMaximize)

# Decision variables
exchange = pulp.LpVariable.dicts("exchange", (
    (i, j) for i in range(N) for j in range(N) if i != j), lowBound=0)

# Objective: Maximize the end amount of currency N
problem += pulp.lpSum(exchange[i, N-1] * rate[i][N-1] for i in range(N) if i != N-1)

# Constraints
for i in range(N):
    # Sum of currency exchanges from currency i should not exceed limit[i]
    problem += pulp.lpSum(exchange[i, j] for j in range(N) if i != j) <= limit[i]
    
    # Balance equation for each currency i
    problem += start[i] + pulp.lpSum(exchange[j, i] * rate[j][i] for j in range(N) if i != j) - pulp.lpSum(exchange[i, j] for j in range(N) if i != j) >= 0

# Solve the problem
problem.solve()

# Extract results
transactions = [
    {"from": i, "to": j, "amount": pulp.value(exchange[i, j])}
    for i in range(N) for j in range(N) if i != j and pulp.value(exchange[i, j]) > 0
]

final_amount_of_currency_N = start[N-1] + pulp.lpSum(
    pulp.value(exchange[i, N-1]) * rate[i][N-1] for i in range(N) if i != N-1)

output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')