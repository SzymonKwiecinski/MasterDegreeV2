import pulp

# Data from the given JSON format
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

# Create a linear programming problem
problem = pulp.LpProblem("InvestmentPortfolioOptimization", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0)

# Objective function
problem += pulp.lpSum((data['Bought'][i] - x[i]) * data['FuturePrice'][i] for i in range(data['N'])), "MaximizeExpectedPortfolioValue"

# Constraints
# Non-negativity and upper bounds constraints
for i in range(data['N']):
    problem += x[i] >= 0, f"NonNegativity_x_{i}"
    problem += x[i] <= data['Bought'][i], f"UpperBound_x_{i}"

# Amount raised constraint
problem += pulp.lpSum(
    (x[i] * data['CurrentPrice'][i] - x[i] * (data['CurrentPrice'][i] - data['BuyPrice'][i]) * (data['TaxRate'] / 100) - x[i] * data['CurrentPrice'][i] * (data['TransactionRate'] / 100))
    for i in range(data['N'])) >= data['K'], "AmountRaisedConstraint"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')