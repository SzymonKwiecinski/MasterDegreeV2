import pulp
import json

data = {'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 
        'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 
        'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}

# Extract data
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate'] / 100
taxRate = data['TaxRate'] / 100
K = data['K']

# Create the problem
problem = pulp.LpProblem("Investment_Portfolio_Optimization", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0)

# Objective function
problem += pulp.lpSum((bought[i] - sell[i]) * futurePrice[i] for i in range(N)), "Total_Profit"

# Constraints
# Net Amount Raised Constraint
problem += (pulp.lpSum(((1 - transactionRate) * sell[i] * currentPrice[i]) - 
                        ((1 - transactionRate) * sell[i] * buyPrice[i] * taxRate) 
                        for i in range(N)) >= K, "Net_Amount_Raised")

# Sell constraints
for i in range(N):
    problem += (sell[i] <= bought[i], f"Sell_Constraint_{i}")
    problem += (sell[i] >= 0, f"Non_Negativity_Constraint_{i}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')