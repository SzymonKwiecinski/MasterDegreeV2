import pulp
import json

# Problem data
data = {
    'N': 3,
    'Start': [100.0, 50.0, 200.0],
    'Limit': [1000.0, 200.0, 3000.0],
    'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]
}

N = data['N']
Start = data['Start']
Limit = data['Limit']
Rate = data['Rate']

# Create a linear programming problem
problem = pulp.LpProblem("Currency_Exchange_Problem", pulp.LpMaximize)

# Define decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), lowBound=0)

# Objective Function
final_amount_N = Start[2] + pulp.lpSum(x[2][j] for j in range(N)) - pulp.lpSum(x[j][2] for j in range(N))
problem += final_amount_N, "Objective"

# Constraints
for i in range(N):
    # Initial Amount Constraint
    problem += Start[i] + pulp.lpSum(x[i][j] for j in range(N)) - pulp.lpSum(x[j][i] for j in range(N)) >= 0, f"Initial_Amount_Constraint_{i}"
    
    # Limit Constraint
    problem += (pulp.lpSum(x[i][j] for j in range(N)) + pulp.lpSum(x[j][i] for j in range(N))) <= Limit[i], f"Limit_Constraint_{i}"

    for j in range(N):
        # Exchange Rate Constraint
        problem += x[i][j] <= Rate[i][j] * Start[i], f"Exchange_Rate_Constraint_{i}_{j}"

# Solve the problem
problem.solve()

# Prepare the output
transactions = []
for i in range(N):
    for j in range(N):
        if x[i][j].value() > 0:
            transactions.append({"from": i + 1, "to": j + 1, "amount": x[i][j].value()})

output = {
    "transactions": transactions,
    "final_amount_of_currency_N": pulp.value(problem.objective)
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')