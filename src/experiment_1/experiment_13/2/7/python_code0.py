import pulp
import json

# Load data from JSON format
data = json.loads('{"N": 3, "Bought": [100, 150, 80], "BuyPrice": [50, 40, 30], "CurrentPrice": [60, 35, 32], "FuturePrice": [65, 44, 34], "TransactionRate": 1.0, "TaxRate": 15.0, "K": 5000}')

# Parameters
N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
TransactionRate = data['TransactionRate']
TaxRate = data['TaxRate']
K = data['K']

# Create the 'prob' variable to contain the problem data
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum((Bought[i] - x[i]) * FuturePrice[i] for i in range(N)), "Total_Value"

# Constraints
# Cannot sell more than bought
for i in range(N):
    problem += x[i] <= Bought[i], f"Sell_Limit_{i}"
    
# Amount raised constraint
problem += pulp.lpSum(
    x[i] * (CurrentPrice[i] - (CurrentPrice[i] - BuyPrice[i]) * TaxRate / 100 - CurrentPrice[i] * TransactionRate) for i in range(N)
) >= K, "Amount_Raised"

# Solve the problem
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')