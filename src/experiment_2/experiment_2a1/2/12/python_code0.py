import pulp
import json

# Data parsing
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}
N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Define the problem
problem = pulp.LpProblem("Currency_Exchange", pulp.LpMaximize)

# Decision variables for the amount exchanged from currency i to currency j
amount = pulp.LpVariable.dicts("amount", (range(N), range(N)), lowBound=0)

# Objective function: Maximize the total amount of currency N we have at the end of the day
problem += pulp.lpSum(amount[i][N-1] for i in range(N)), "Total_Amount_of_Currency_N"

# Constraints for the limits on currency exchanges
for i in range(N):
    problem += pulp.lpSum(amount[i][j] for j in range(N)) <= limit[i], f"Limit_Constraint_{i}"

# Constraints for starting currency amounts
for j in range(N):
    problem += pulp.lpSum(amount[i][j] for i in range(N)) <= start[j], f"Start_Amount_Constraint_{j}"

# Constraints for exchange rates
for i in range(N):
    for j in range(N):
        if i != j:
            problem += amount[i][j] <= start[i] * rate[i][j], f"Exchange_Rate_Constraint_{i}_{j}"

# Solve the problem
problem.solve()

# Prepare the output
transactions = []
for i in range(N):
    for j in range(N):
        if i != j and amount[i][j].varValue > 0:
            transactions.append({
                "from": i,
                "to": j,
                "amount": amount[i][j].varValue
            })

final_amount_of_currency_N = sum(amount[i][N-1].varValue for i in range(N))

# Output the result in the required format
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')