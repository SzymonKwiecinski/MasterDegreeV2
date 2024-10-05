import pulp
import json

# Load data from JSON
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

# Define the LP problem
problem = pulp.LpProblem("Maximize_Currency_N", pulp.LpMaximize)

# Decision variables
transactions = pulp.LpVariable.dicts(
    "x", ((i, j) for i in range(N) for j in range(N)), 
    lowBound=0, cat='Continuous'
)

# Objective: Maximize the units of currency N
problem += pulp.lpSum(transactions[i, N-1] * rate[i][N-1] for i in range(N)), "Maximize_Currency_N"

# Balance constraints for each currency
for i in range(N):
    problem += (
        start[i] + pulp.lpSum(transactions[j, i] * rate[j][i] for j in range(N)) 
        - pulp.lpSum(transactions[i, j] for j in range(N)) == 0,
        f"Balance_Constraint_for_Currency_{i}"
    )

# Exchange limits constraints
for i in range(N):
    problem += (
        pulp.lpSum(transactions[i, j] for j in range(N)) <= limit[i],
        f"Limit_Constraint_for_Currency_{i}"
    )

# Solve the problem
problem.solve()

# Prepare the output
transactions_result = [{
    "from": i,
    "to": j,
    "amount": transactions[i, j].varValue
} for i in range(N) for j in range(N) if transactions[i, j].varValue > 0]

output = {
    "transactions": transactions_result,
    "final_amount_of_currency_N": pulp.value(problem.objective)
}

# Print the results
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')