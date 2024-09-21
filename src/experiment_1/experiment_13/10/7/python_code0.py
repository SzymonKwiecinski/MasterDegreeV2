import pulp
import json

# Data provided in JSON format
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

# Extracting parameters from data
N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
TransactionRate = data['TransactionRate']
TaxRate = data['TaxRate']
K = data['K']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("Shares_Sold", range(N), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum((Bought[i] - x[i]) * FuturePrice[i] for i in range(N)), "Total_Portfolio_Value"

# Constraints
# Non-negativity constraint and Cannot sell more than bought
for i in range(N):
    problem += x[i] >= 0, f"Non_Negativity_Constraint_{i}"
    problem += x[i] <= Bought[i], f"Max_Sell_Constraint_{i}"

# Amount raised constraint
problem += pulp.lpSum(
    x[i] * CurrentPrice[i] - 
    x[i] * (CurrentPrice[i] - BuyPrice[i]) * (TaxRate / 100) - 
    x[i] * CurrentPrice[i] * (TransactionRate / 100) 
    for i in range(N)
) >= K, "Amount_Raised_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')