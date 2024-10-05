import pulp
import json

# Input data
data = {
    'N': 3, 
    'Start': [100.0, 50.0, 200.0], 
    'Limit': [1000.0, 200.0, 3000.0], 
    'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]
}

# Unpack data
N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Define the problem
problem = pulp.LpProblem("Currency_Exchange", pulp.LpMaximize)

# Decision variables: amount of currency i to be exchanged to currency j
amount = pulp.LpVariable.dicts("amount", ((i, j) for i in range(N) for j in range(N)),
                               lowBound=0, cat='Continuous')

# Objective: Maximize the end amount of currency N
problem += start[-1] + pulp.lpSum(amount[i, N-1]*rate[i][N-1] for i in range(N)), "Maximize final currency N amount"

# Constraints for each currency
for i in range(N):
    # Total outflow from currency i cannot exceed available amount
    problem += pulp.lpSum(amount[i, j] for j in range(N)) <= start[i] + pulp.lpSum(amount[j, i]*rate[j][i] for j in range(N)), f"Outflow constraint for currency {i}"

    # Limit constraints for each currency
    problem += pulp.lpSum(amount[i, j] for j in range(N)) <= limit[i], f"Limit constraint for currency {i}"

# Solve the problem
problem.solve()

# Generate the output
transactions = [
    {
        "from": i,
        "to": j,
        "amount": amount[i, j].varValue
    }
    for i in range(N) for j in range(N) if amount[i, j].varValue > 0
]

final_amount_of_currency_N = start[-1] + sum(amount[i, N-1].varValue * rate[i][N-1] for i in range(N))

output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

# Print results
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')