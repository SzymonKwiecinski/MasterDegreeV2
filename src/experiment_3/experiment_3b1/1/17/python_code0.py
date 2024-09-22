import pulp
import json

# Data in JSON format
data = json.loads('{"N": 3, "Bought": [100, 150, 80], "BuyPrice": [50, 40, 30], "CurrentPrice": [60, 35, 32], "FuturePrice": [65, 44, 34], "TransactionRate": 1.0, "TaxRate": 15.0, "K": 5000}')

# Extracting data
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate'] / 100  # Convert percentage to fraction
taxRate = data['TaxRate'] / 100  # Convert percentage to fraction
K = data['K']

# Create a linear programming problem
problem = pulp.LpProblem("Stock_Selling_Problem", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0)

# Objective function
problem += pulp.lpSum(futurePrice[i] * (bought[i] - sell[i]) for i in range(N)), "Objective"

# Constraints
# Constraint 1: The amount raised from selling stocks must cover the desired amount K
problem += (
    pulp.lpSum(currentPrice[i] * sell[i] * (1 - transactionRate) - 
                taxRate * (currentPrice[i] * sell[i] - buyPrice[i] * sell[i]) for i in range(N)) >= K,
    "AmountRaisedConstraint"
)

# Constraint 2: The number of shares sold must not exceed the number of shares bought
for i in range(N):
    problem += sell[i] <= bought[i], f"MaxSellConstraint_{i}"

# Solve the problem
problem.solve()

# Output results
sell_values = [sell[i].varValue for i in range(N)]
print(f'Output: {{"sell": {sell_values}}}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')