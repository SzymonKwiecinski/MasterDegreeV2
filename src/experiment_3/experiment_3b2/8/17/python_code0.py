import pulp

# Data from the JSON format
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

# Number of assets
N = data['N']

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

# Define decision variables
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0, cat='Continuous')
bought = data['Bought']

# Objective function
problem += pulp.lpSum((bought[i] - sell[i]) * data['FuturePrice'][i] for i in range(N)), "Total Expected Value"

# Constraints
# Constraint 1: raise amount K
problem += (pulp.lpSum(sell[i] * data['CurrentPrice'][i] for i in range(N)) - 
             pulp.lpSum(sell[i] * data['BuyPrice'][i] for i in range(N)) * (data['TaxRate'] / 100) - 
             pulp.lpSum(sell[i] * data['CurrentPrice'][i] for i in range(N)) * (data['TransactionRate'] / 100) >= data['K']), "Capital Gains Constraint"

# Constraint 2: limit on maximum shares sold
for i in range(N):
    problem += (sell[i] <= bought[i]), f"Max_Sold_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')