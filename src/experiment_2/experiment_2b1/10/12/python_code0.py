import pulp
import json

# Input data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 
        'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

# Extract variables from data
N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Initialize the problem
problem = pulp.LpProblem("Maximize_Currency", pulp.LpMaximize)

# Define decision variables for transactions
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N) if i != j), lowBound=0)

# Define the objective function
problem += pulp.lpSum(x[i, j] * rate[i][j] for i in range(N) for j in range(N) if i != j)

# Constraints for limits and starting amounts
for i in range(N):
    problem += pulp.lpSum(x[i, j] for j in range(N) if i != j) <= limit[i], f"Limit_{i}"
    problem += pulp.lpSum(x[j, i] for j in range(N) if i != j) <= limit[i], f"Limit_From_{i}"

# Constraints for starting amounts
for i in range(N):
    problem += pulp.lpSum(x[i, j] for j in range(N) if i != j) + start[i] >= pulp.lpSum(x[j, i] for j in range(N) if i != j), f"Start_Amount_{i}"

# Solve the problem
problem.solve()

# Prepare output
transactions = []
for (i, j) in x:
    amount = x[i, j].varValue
    if amount > 0:
        transactions.append({"from": i, "to": j, "amount": amount})

# Calculate final amount of currency N
final_amount_of_currency_N = start[2] + pulp.value(problem.objective)

# Create the output structure
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

# Print the final objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(json.dumps(output, indent=4))