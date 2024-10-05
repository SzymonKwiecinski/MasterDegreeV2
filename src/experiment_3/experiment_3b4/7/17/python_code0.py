import pulp

# Data
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
TransactionRate = data['TransactionRate']
TaxRate = data['TaxRate']
K = data['K']

# Problem
problem = pulp.LpProblem("Maximize_Future_Value", pulp.LpMaximize)

# Variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=Bought[i], cat='Continuous') for i in range(N)]

# Objective Function
problem += pulp.lpSum((Bought[i] - sell[i]) * FuturePrice[i] for i in range(N))

# Constraints
# Net amount raised constraint
problem += pulp.lpSum(
    sell[i] * CurrentPrice[i] * (1 - TransactionRate / 100) - 
    max(0, (CurrentPrice[i] - BuyPrice[i]) * sell[i] * TaxRate / 100) 
    for i in range(N)
) >= K

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')