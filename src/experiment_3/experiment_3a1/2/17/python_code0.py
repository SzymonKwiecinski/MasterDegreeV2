import pulp
import json

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

# Problem definition
problem = pulp.LpProblem("InvestorPortfolio", pulp.LpMaximize)

# Variables
sell = pulp.LpVariable.dicts("sell", range(data['N']), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(data['FuturePrice'][i] * (data['Bought'][i] - sell[i]) for i in range(data['N'])), "Total Future Value"

# Constraints
net_amount_raised = pulp.lpSum(
    ((1 - data['TransactionRate'] / 100 - data['TaxRate'] / 100) * (data['CurrentPrice'][i] * sell[i]) +
      (data['TaxRate'] / 100 * data['BuyPrice'][i] * sell[i])) for i in range(data['N'])
)

problem += net_amount_raised >= data['K'], "NetAmountRaisedConstraint"

# Constraints for sold shares not exceeding bought shares
for i in range(data['N']):
    problem += sell[i] <= data['Bought'][i], f"SellLimit_{i}"

# Solving the problem
problem.solve()

# Output the result
results = {f'sell_{i+1}': sell[i].varValue for i in range(data['N'])}
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(results)