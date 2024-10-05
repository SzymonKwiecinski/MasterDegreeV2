import pulp
import json

# Input data
data = {
    "N": 3,
    "Start": [100.0, 50.0, 200.0],
    "Limit": [1000.0, 200.0, 3000.0],
    "Rate": [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]
}

N = data["N"]
start = data["Start"]
limit = data["Limit"]
rate = data["Rate"]

# Problem
problem = pulp.LpProblem("Maximize_Currency_N", pulp.LpMaximize)

# Decision variables
amounts = pulp.LpVariable.dicts("amount",
                                ((i, j) for i in range(N) for j in range(N)),
                                lowBound=0)

# Objective function: Maximize the number of units of currency N (currency index N-1)
problem += (start[N-1] + 
            pulp.lpSum(amounts[i, N-1] * rate[i][N-1] for i in range(N)) -
            pulp.lpSum(amounts[N-1, j] for j in range(N)))

# Constraints
for i in range(N):
    problem += pulp.lpSum(amounts[i, j] for j in range(N) if j != i) <= start[i], f"LimitStart_{i}"
    problem += pulp.lpSum(amounts[j, i] * rate[j][i] for j in range(N) if j != i) <= limit[i], f"LimitExchange_{i}"

# Solve the problem
problem.solve()

# Prepare output
transactions = [
    {
        "from": i,
        "to": j,
        "amount": amounts[i, j].varValue
    }
    for i in range(N)
    for j in range(N)
    if i != j and amounts[i, j].varValue > 0
]

final_amount_of_currency_N = start[N-1] + sum(amounts[i, N-1].varValue * rate[i][N-1] for i in range(N)) - sum(amounts[N-1, j].varValue for j in range(N))

output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

# Print output in required JSON format
output_json = json.dumps(output, indent=4)
print(output_json)

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')