import pulp

# Data from the problem
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}
N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Define the problem
problem = pulp.LpProblem("Maximize_currency_N", pulp.LpMaximize)

# Decision variables: amount of currency i exchanged to currency j
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), lowBound=0)

# Objective: Maximize the amount of currency N we end up with
problem += pulp.lpSum(x[i, N-1] * rate[i][N-1] for i in range(N))

# Constraints
for i in range(N):
    # The total amount of currency i exchanged (to or from) cannot exceed its limit
    problem += pulp.lpSum(x[i, j] + x[j, i] for j in range(N)) <= limit[i]
    
    # Proceed with exchange, ensuring we start with what we have
    problem += (start[i] + pulp.lpSum(x[j, i] * rate[j][i] for j in range(N) if j != i)
                - pulp.lpSum(x[i, j] for j in range(N) if j != i)) >= 0

# Solve the problem
problem.solve()

# Prepare the output
transactions = []
for i in range(N):
    for j in range(N):
        if i != j and x[i, j].varValue > 0:
            transactions.append({
                "from": i+1,  # converting to 1-based index for output (problem spec)
                "to": j+1,
                "amount": x[i, j].varValue
            })

# Final amount of currency N
final_amount_of_currency_N = start[N-1] + pulp.lpSum(x[i, N-1].varValue * rate[i][N-1] for i in range(N))

# Output format
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')