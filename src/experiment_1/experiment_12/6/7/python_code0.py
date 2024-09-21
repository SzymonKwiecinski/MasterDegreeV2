import pulp

# Data extracted from the JSON
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

# Correcting the rates from percentage to decimal
TransactionRate = data['TransactionRate'] / 100
TaxRate = data['TaxRate'] / 100

# Extracting the rest of the data
N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
K = data['K']

# Define the problem
problem = pulp.LpProblem("Maximize_Expected_Portfolio_Value", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, upBound=Bought[i], cat='Continuous') for i in range(N)]

# Objective function
objective = pulp.lpSum((Bought[i] - x[i]) * FuturePrice[i] for i in range(N))
problem += objective

# Constraints
# Amount raised constraint
problem += pulp.lpSum([
    x[i] * CurrentPrice[i] - 
    x[i] * (CurrentPrice[i] - BuyPrice[i]) * TaxRate -
    x[i] * CurrentPrice[i] * TransactionRate 
    for i in range(N)
]) >= K

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')