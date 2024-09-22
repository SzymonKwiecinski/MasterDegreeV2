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

# Problem definition
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

# Variables
N = data['N']
bought = data['Bought']
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0, upBound=None, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['FuturePrice'][i] * (bought[i] - sell[i]) for i in range(N)), "Expected_Portfolio_Value"

# Constraints
# Constraint 1: Amount received from selling shares must be at least K
problem += pulp.lpSum(((data['CurrentPrice'][i] * sell[i] * (1 - data['TransactionRate'] / 100)) - 
                        ((data['CurrentPrice'][i] - data['BuyPrice'][i]) * sell[i] * (data['TaxRate'] / 100))) 
                       for i in range(N)) >= data['K'], "Capital_Gains_Constraint"

# Constraint 2: Cannot sell more than bought
for i in range(N):
    problem += sell[i] <= bought[i], f"Max_Sell_Constraint_{i}"

# Solve the problem
problem.solve()

# Output
sell_results = [sell[i].varValue for i in range(N)]
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Output: {{ "sell": {sell_results} }}')