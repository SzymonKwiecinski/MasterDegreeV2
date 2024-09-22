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

# Unpacking data
N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
TransactionRate = data['TransactionRate']
TaxRate = data['TaxRate']
K = data['K']

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
sell_vars = [pulp.LpVariable(f'sell_{i}', lowBound=0) for i in range(N)]

# Objective Function
problem += pulp.lpSum((Bought[i] - sell_vars[i]) * FuturePrice[i] for i in range(N))

# Constraints
for i in range(N):
    problem += sell_vars[i] <= Bought[i], f"sell_constraint_{i}"

problem += pulp.lpSum(
    sell_vars[i] * CurrentPrice[i] * (1 - TransactionRate / 100)
    - sell_vars[i] * (CurrentPrice[i] - BuyPrice[i]) * (TaxRate / 100)
    for i in range(N)
) >= K, "revenue_constraint"

# Solve
problem.solve()

# Results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')