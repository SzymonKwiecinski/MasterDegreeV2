import pulp

# Data from JSON
data = {
    'N': 3,
    'Bought': [100, 150, 80],
    'BuyPrice': [50, 40, 30],
    'CurrentPrice': [60, 35, 32],
    'FuturePrice': [65, 44, 34],
    'TransactionRate': 1.0,
    'TaxRate': 15.0,
    'K': 5000
}

N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
TransactionRate = data['TransactionRate'] / 100  # Converting percentage to rate
TaxRate = data['TaxRate'] / 100  # Converting percentage to rate
K = data['K']

# Define the LP problem
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, upBound=Bought[i], cat='Continuous') for i in range(N)]

# Objective function
problem += pulp.lpSum((Bought[i] - x[i]) * FuturePrice[i] for i in range(N)), "Total_Future_Value"

# Constraints
# Amount raised constraint
problem += pulp.lpSum(
    x[i] * CurrentPrice[i] - x[i] * (CurrentPrice[i] - BuyPrice[i]) * TaxRate - x[i] * CurrentPrice[i] * TransactionRate
    for i in range(N)
) >= K, "Amount_Raised"

# Solve the problem
problem.solve()

# Print results
print(f"Status: {pulp.LpStatus[problem.status]}")
for i in range(N):
    print(f"Shares sold of type {i+1}: {x[i].varValue}")
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")