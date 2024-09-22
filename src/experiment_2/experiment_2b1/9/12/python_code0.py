import json
import pulp

# Input data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Define the problem
problem = pulp.LpProblem("Currency_Exchange", pulp.LpMaximize)

# Define decision variables for the amount of currency exchanged
amounts = pulp.LpVariable.dicts("Amount", (range(N), range(N)), lowBound=0)

# Objective function: maximize the final amount of currency N
final_currency_N = start[2] + pulp.lpSum((amounts[i][2] * rate[i][2]) for i in range(N))
problem += final_currency_N, "Maximize_Amount_Currency_N"

# Constraints
for i in range(N):
    # Starting amounts
    problem += pulp.lpSum(amounts[i][j] for j in range(N)) <= start[i], f"Start_Amount_Constraint_{i}"
    
    # Limits on each currency exchange
    problem += pulp.lpSum(amounts[i][j] for j in range(N)) <= limit[i], f"Limit_Amount_Constraint_{i}"
    
    # Currency exchange limits
    for j in range(N):
        if i != j:
            problem += amounts[i][j] <= limit[i], f"Exchange_Limit_Constraint_{i}_{j}"

# Solve the problem
problem.solve()

# Prepare output
transactions = []
for i in range(N):
    for j in range(N):
        if i != j and amounts[i][j].value() > 0:
            transactions.append({
                "from": i,
                "to": j,
                "amount": amounts[i][j].value()
            })

final_amount_of_currency_N = start[2] + sum(amounts[i][2].value() * rate[i][2] for i in range(N))

# Printing output
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')