import pulp
import json

# Input data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 
        'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Problem
problem = pulp.LpProblem("Maximize_Currency_N", pulp.LpMaximize)

# Variables
exchange = pulp.LpVariable.dicts("Exchange", (range(N), range(N)), lowBound=0)

# Objective: Maximize currency N
problem += pulp.lpSum(exchange[i][N-1] * rate[i][N-1] for i in range(N))

# Constraints
# Initial balance constraint and transaction limits
for i in range(N):
    # Total outflow and inflow constraints
    outflow = pulp.lpSum(exchange[i][j] for j in range(N))
    inflow = pulp.lpSum(exchange[j][i] * rate[j][i] for j in range(N))
    
    problem += (start[i] + inflow - outflow >= 0, f"Balance_{i}")
    problem += (outflow <= limit[i], f"Limit_{i}")

# Solve
problem.solve()

# Prepare output
transactions = []
for i in range(N):
    for j in range(N):
        amount = exchange[i][j].varValue
        if amount > 0:
            transactions.append({
                "from": i + 1,  # variables are 0-indexed, data might be 1-indexed
                "to": j + 1,
                "amount": amount
            })

final_amount_of_currency_N = pulp.value(start[N-1] + pulp.lpSum(exchange[j][N-1] * rate[j][N-1] for j in range(N)) - pulp.lpSum(exchange[N-1][j] for j in range(N)))

output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

# Printing objective value for clarity
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output result
output_json = json.dumps(output, indent=4)
print(output_json)