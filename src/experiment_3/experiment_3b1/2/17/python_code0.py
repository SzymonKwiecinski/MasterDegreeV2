import pulp
import json

# Input data
data = json.loads("""{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}""")

# Parameters
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate']
taxRate = data['TaxRate']
K = data['K']

# Problem definition
problem = pulp.LpProblem("Maximize_Expected_Portfolio_Value", pulp.LpMaximize)

# Decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i]) for i in range(N)]

# Objective function
problem += pulp.lpSum(futurePrice[i] * (bought[i] - sell[i]) for i in range(N)), "Total_Expected_Value"

# Constraint
problem += (pulp.lpSum(currentPrice[i] * sell[i] * (1 - transactionRate / 100) 
                         - (currentPrice[i] - buyPrice[i]) * sell[i] * (taxRate / 100) 
                         for i in range(N)) >= K), "Minimum_Amount_Raised")

# Solve the problem
problem.solve()

# Output
sell_shares = [pulp.value(sell[i]) for i in range(N)]
print(f'Output: {{"sell": {sell_shares}}}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')