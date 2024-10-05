import pulp

# Extract data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Initialize the problem
problem = pulp.LpProblem('Currency_Exchange', pulp.LpMaximize)

# Define the variables
x = pulp.LpVariable.dicts('exchange', ((i, j) for i in range(N) for j in range(N)), lowBound=0, cat='Continuous')

# Objective function: Maximize the final amount of currency N
problem += pulp.lpSum(x[i][N-1] for i in range(N)), "Maximize_Currency_N"

# Constraints

# 1. Amount of each currency exchanged cannot exceed the start amount + amount received
for i in range(N):
    problem += (
        pulp.lpSum(x[j][i] * rate[j][i] for j in range(N) if j != i) + start[i] >= 
        pulp.lpSum(x[i][j] for j in range(N)), 
        f"Conservation_of_Currency_{i+1}"
    )

# 2. Limit on total amount of currency exchanged for each i
for i in range(N):
    problem += (
        pulp.lpSum(x[i][j] for j in range(N)) <= limit[i],
        f"Limit_on_Currency_{i+1}"
    )

# Solve the problem
problem.solve()

# Prepare the output
transactions = [{'from': i+1, 'to': j+1, 'amount': x[i][j].varValue} for i in range(N) for j in range(N) if x[i][j].varValue > 0]

final_amount_of_currency_N = sum(start[N-1] + pulp.lpSum(x[i][N-1].varValue for i in range(N)))

output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')