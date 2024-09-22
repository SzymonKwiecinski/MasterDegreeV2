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

# Extract data
N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
TransactionRate = data['TransactionRate'] / 100
TaxRate = data['TaxRate'] / 100
K = data['K']

# Problem
problem = pulp.LpProblem("Portfolio_Optimization", pulp.LpMaximize)

# Decision Variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=Bought[i], cat='Continuous') for i in range(N)]

# Objective
problem += pulp.lpSum((Bought[i] - sell[i]) * FuturePrice[i] for i in range(N)), "Expected_Future_Value"

# Constraints
# Constraint 1: Non-negativity and selling constraints are handled in variable bounds
# Constraint 2: Raise the required money K
problem += pulp.lpSum(
    ((1 - TransactionRate) * CurrentPrice[i] * sell[i] -
     TaxRate * pulp.lpSum(pulp.lpMax(0, (CurrentPrice[i] - BuyPrice[i]) * sell[i]) for i in range(N)))
    ) for i in range(N)
) >= K, "Raise_Required_Money"

# Solve
problem.solve()

# Print results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')