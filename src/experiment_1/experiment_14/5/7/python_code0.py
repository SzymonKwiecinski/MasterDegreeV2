import pulp

# Data from the JSON
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

# Extracting data
N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
TransactionRate = data['TransactionRate'] / 100.0
TaxRate = data['TaxRate'] / 100.0
K = data['K']

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, upBound=Bought[i]) for i in range(N)]

# Objective Function
problem += pulp.lpSum((Bought[i] - x[i]) * FuturePrice[i] for i in range(N)), "Expected_Future_Portfolio_Value"

# Constraints

# Amount raised constraint
problem += pulp.lpSum([
    x[i] * CurrentPrice[i] - 
    x[i] * (CurrentPrice[i] - BuyPrice[i]) * TaxRate - 
    x[i] * CurrentPrice[i] * TransactionRate 
    for i in range(N)
]) >= K, "Amount_Raised"

# Solve the problem
problem.solve()

# Output the results
print("Solution Status:", pulp.LpStatus[problem.status])
for i in range(N):
    print(f'Number of shares {i+1} sold: {x[i].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')