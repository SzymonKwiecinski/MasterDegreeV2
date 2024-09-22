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

N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate']
taxRate = data['TaxRate']
K = data['K']

# Define the problem
problem = pulp.LpProblem("Stock_Selling_Problem", pulp.LpMaximize)

# Variables
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0)

# Objective function
problem += pulp.lpSum(futurePrice[i] * (bought[i] - sell[i]) for i in range(N)), "Total_Value"

# Constraints
problem += pulp.lpSum(
    currentPrice[i] * sell[i] * (1 - transactionRate / 100) - 
    (sell[i] * bought[i] * (currentPrice[i] - buyPrice[i]) * taxRate / 100) 
    for i in range(N)) >= K, "Raise_Amount"

# Constraints for the maximum number of shares that can be sold
for i in range(N):
    problem += sell[i] <= bought[i], f"Max_Sell_{i+1}"
    
# Solve the problem
problem.solve()

# Retrieve results
sell_values = [sell[i].varValue for i in range(N)]

# Output the results
print(f'sell = {sell_values}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')