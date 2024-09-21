import pulp

# Data
data = {
    'N': 3,
    'Bought': [100, 150, 80],
    'BuyPrice': [50, 40, 30],
    'CurrentPrice': [60, 35, 32],
    'FuturePrice': [65, 44, 34],
    'TransactionRate': 1.0,  # Transaction cost rate per share sold
    'TaxRate': 15.0,  # Capital gains tax rate
    'K': 5000  # Amount of money the investor needs to raise
}

# Parameters
N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
TransactionRate = data['TransactionRate'] / 100.0
TaxRate = data['TaxRate'] / 100.0
K = data['K']

# Problem
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, upBound=Bought[i], cat='Continuous') for i in range(N)]

# Objective Function
problem += pulp.lpSum([(Bought[i] - x[i]) * FuturePrice[i] for i in range(N)])

# Constraints
# Amount raised constraint
problem += pulp.lpSum([
    x[i] * (CurrentPrice[i] - (CurrentPrice[i] - BuyPrice[i]) * TaxRate - CurrentPrice[i] * TransactionRate)
    for i in range(N)
]) >= K

# Solve
problem.solve()

# Output the Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')