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

# Parameters
N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
TransactionRate = data['TransactionRate']
TaxRate = data['TaxRate']
K = data['K']

# Initialize the problem
problem = pulp.LpProblem("MaximizeFutureValue", pulp.LpMaximize)

# Decision variables
sell_vars = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=Bought[i]) for i in range(N)]

# Objective function
problem += pulp.lpSum((Bought[i] - sell_vars[i]) * FuturePrice[i] for i in range(N))

# Constraint: amount of money to be raised
problem += (
    pulp.lpSum(
        sell_vars[i] * CurrentPrice[i] * (1 - TransactionRate / 100) -
        max(0, sell_vars[i] * (CurrentPrice[i] - BuyPrice[i])) * TaxRate / 100
        for i in range(N)
    ) >= K
)

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')