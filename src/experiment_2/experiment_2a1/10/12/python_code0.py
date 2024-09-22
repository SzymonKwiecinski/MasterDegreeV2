import json
import pulp

# Input data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Currency", pulp.LpMaximize)

# Create variables for amounts exchanged
amounts = pulp.LpVariable.dicts("amount", (range(N), range(N)), lowBound=0)

# Objective function: Maximize the total amount of currency N
problem += pulp.lpSum(amounts[i][2] for i in range(N)), "Total_Amount_of_Currency_N"

# Constraints for starting amounts
for i in range(N):
    problem += pulp.lpSum(amounts[i][j] for j in range(N)) <= start[i], f"Start_Constraint_{i}"
    problem += pulp.lpSum(amounts[j][i] for j in range(N)) <= start[i], f"Start_Constraint_In_{i}"

# Constraints for limits
for i in range(N):
    problem += pulp.lpSum(amounts[i][j] for j in range(N)) <= limit[i], f"Limit_Constraint_{i}"
    problem += pulp.lpSum(amounts[j][i] for j in range(N)) <= limit[i], f"Limit_Constraint_In_{i}"

# Rate constraints
for i in range(N):
    for j in range(N):
        if i != j:
            problem += amounts[i][j] <= start[i] * rate[i][j], f"Rate_Constraint_{i}_{j}"

# Solve the problem
problem.solve()

# Prepare transactions and final amount
transactions = []
for i in range(N):
    for j in range(N):
        if i != j and amounts[i][j].varValue:
            transactions.append({
                "from": i,
                "to": j,
                "amount": amounts[i][j].varValue
            })

final_amount_of_currency_N = sum(amounts[i][2].varValue for i in range(N))

# Output
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')