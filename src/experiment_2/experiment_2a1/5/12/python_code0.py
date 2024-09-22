import json
import pulp

# Input data
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

# Define the problem
problem = pulp.LpProblem("Currency_Exchange_Problem", pulp.LpMaximize)

# Create variables for the amount exchanged from currency i to currency j
exchange_vars = pulp.LpVariable.dicts("exchange", 
                                        [(i, j) for i in range(N) for j in range(N) if i != j], 
                                        lowBound=0)

# Objective function: Maximize the total amount of currency N we can have at the end of the day
problem += pulp.lpSum(exchange_vars[(i, N-1)] * rate[i][N-1] for i in range(N)), "Total_Amount_Currency_N"

# Constraints for the exchanges
for i in range(N):
    # The total amount exchanged from currency i
    outgoing = pulp.lpSum(exchange_vars[(i, j)] for j in range(N) if j != i)
    # The total amount exchanged to currency i
    incoming = pulp.lpSum(exchange_vars[(j, i)] for j in range(N) if j != i)
    
    # Ensure the outgoing doesn't exceed the starting amount and the limit
    problem += outgoing <= start[i] + limit[i], f"Outgoing_Limit_{i}"
    
    # Mirror the incoming for limit constraints
    problem += incoming <= limit[i], f"Incoming_Limit_{i}"

# Solve the problem
problem.solve()

# Prepare the output
transactions = []
for (i, j) in exchange_vars:
    amount = exchange_vars[(i, j)].varValue
    if amount > 0:
        transactions.append({
            "from": i,
            "to": j,
            "amount": amount
        })

final_amount_of_currency_N = sum(exchange_vars[(i, N-1)].varValue * rate[i][N-1] for i in range(N))

# Output the result
result = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')