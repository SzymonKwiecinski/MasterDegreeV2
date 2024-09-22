import pulp
import json

# Input data
data = json.loads("{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}")

N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate']
taxRate = data['TaxRate']
K = data['K']

# Define the problem
problem = pulp.LpProblem("Investment_Portfolio", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(futurePrice[i] * (bought[i] - sell[i]) for i in range(N)), "Total_Expected_Value"

# Constraints
# Constraint 1: Total amount raised after selling should cover K
problem += (pulp.lpSum((currentPrice[i] * sell[i] * (1 - transactionRate / 100)) - 
                        ((currentPrice[i] - buyPrice[i]) * sell[i] * (taxRate / 100)) 
                        for i in range(N)) >= K), "Capital_Gains_Constraint")

# Constraint 2: Number of shares sold cannot exceed those bought
for i in range(N):
    problem += (sell[i] <= bought[i]), f"Sell_Constraint_Stock_{i+1}"

# Solve the problem
problem.solve()

# Output the results
sell_values = [sell[i].varValue for i in range(N)]
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Output: {{"sell": {sell_values}}}')