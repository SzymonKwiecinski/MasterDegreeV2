import pulp
import json

# Data provided in JSON format
data = {'N': 3, 
        'Bought': [100, 150, 80], 
        'BuyPrice': [50, 40, 30], 
        'CurrentPrice': [60, 35, 32], 
        'FuturePrice': [65, 44, 34], 
        'TransactionRate': 1.0, 
        'TaxRate': 15.0, 
        'K': 5000}

# Parameters
N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
TransactionRate = data['TransactionRate']
TaxRate = data['TaxRate']
K = data['K']

# Create the problem
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0)  # Number of shares sold

# Objective Function
problem += pulp.lpSum([(Bought[i] - x[i]) * FuturePrice[i] for i in range(N)])

# Constraints
# Non-negativity constraints are handled by the lowBound in LpVariable
for i in range(N):
    problem += x[i] <= Bought[i]  # Cannot sell more than bought

# Amount raised constraint
problem += (pulp.lpSum([x[i] * CurrentPrice[i] - 
                        x[i] * (CurrentPrice[i] - BuyPrice[i]) * (TaxRate / 100) - 
                        x[i] * CurrentPrice[i] * (TransactionRate / 100) for i in range(N)]) 
                     >= K)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')