import pulp

# Extracting data from the JSON format
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
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate']
taxRate = data['TaxRate']
K = data['K']

# Define the problem
problem = pulp.LpProblem("Stock_Selling", pulp.LpMaximize)

# Define the decision variables
s = [pulp.LpVariable(f's_{i}', lowBound=0, upBound=bought[i], cat='Continuous') for i in range(N)]

# Define the objective function
objective = pulp.lpSum(
    (futurePrice[i] - buyPrice[i]) * bought[i] - 
    (transactionRate / 100 * currentPrice[i] * s[i] + 
     taxRate / 100 * (currentPrice[i] * s[i] - buyPrice[i] * s[i])) 
    for i in range(N)
)
problem += objective

# Define the constraints
# Constraint 1: Amount raised must be at least K
problem += pulp.lpSum(
    (currentPrice[i] * s[i] - (
        transactionRate / 100 * currentPrice[i] * s[i] +
        taxRate / 100 * (currentPrice[i] * s[i] - buyPrice[i] * s[i])
    )) for i in range(N)
) >= K

# Constraint 2 and 3: Each s_i must be non-negative and can not exceed bought_i (handled by LpVariable definition)

# Solve the problem
problem.solve()

# Print the results
print("Status:", pulp.LpStatus[problem.status])
for i in range(N):
    print(f's_{i} (Shares to sell for stock {i+1}): {s[i].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')