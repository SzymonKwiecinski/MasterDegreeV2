import json
import pulp

# Input data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 
        'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

N = data['N']
start = data['Start']
limit = data['Limit']
rates = data['Rate']

# Create the problem
problem = pulp.LpProblem("Currency_Exchange_Problem", pulp.LpMaximize)

# Define decision variables
amounts = pulp.LpVariable.dicts("amount", (range(N), range(N)), lowBound=0)

# Set the objective function to maximize the final amount of currency N
problem += pulp.lpSum(amounts[i][N-1] for i in range(N)), "Total_Final_Amount_of_Currency_N"

# Constraints for starting amounts and limits
for i in range(N):
    problem += (pulp.lpSum(amounts[i][j] for j in range(N)) - pulp.lpSum(amounts[j][i] for j in range(N)) <= limit[i]), f"Limit_Constraint_{i}"
    problem += (pulp.lpSum(amounts[i][j] for j in range(N)) + start[i] >= sum(amounts[j][i] for j in range(N))), f"Start_Amount_Constraint_{i}"

# Constraints for each currency exchange based on rates
for i in range(N):
    for j in range(N):
        if i != j:
            problem += (amounts[i][j] <= start[i] * rates[i][j]), f"Rate_Constraint_{i}_{j}"

# Solve the problem
problem.solve()

# Prepare output
transactions = []
for i in range(N):
    for j in range(N):
        if i != j and amounts[i][j].varValue > 0:
            transactions.append({
                "from": i,
                "to": j,
                "amount": amounts[i][j].varValue
            })

final_amount_currency_N = pulp.value(problem.objective)

# Output results
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_currency_N
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')