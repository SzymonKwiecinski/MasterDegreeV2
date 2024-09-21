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

# Constants
N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
TransactionRate = data['TransactionRate'] / 100  # Convert percentage to a decimal
TaxRate = data['TaxRate'] / 100  # Convert percentage to a decimal
K = data['K']

# Problem
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, upBound=Bought[i]) for i in range(N)]

# Objective Function
problem += pulp.lpSum((Bought[i] - x[i]) * FuturePrice[i] for i in range(N))

# Constraints
# Non-negativity and not selling more than bought constraints are handled by variable bounds
# Amount raised constraint
problem += pulp.lpSum([
    x[i] * CurrentPrice[i] - 
    x[i] * (CurrentPrice[i] - BuyPrice[i]) * TaxRate - 
    x[i] * CurrentPrice[i] * TransactionRate 
    for i in range(N)
]) >= K

# Solve the problem
problem.solve()

# Output the results
for i in range(N):
    print(f'Shares of type {i+1} sold: {x[i].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')