import pulp

# Problem data
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

# Create the problem
problem = pulp.LpProblem("Maximize_Investor_Portfolio", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]

# Objective function
problem += pulp.lpSum((data['Bought'][i] - x[i]) * data['FuturePrice'][i] for i in range(data['N'])), "Total_Expected_Value"

# Constraints
for i in range(data['N']):
    problem += x[i] <= data['Bought'][i], f"Max_Sell_{i}"

# Amount raised constraint
problem += (
    pulp.lpSum(
        x[i] * (data['CurrentPrice'][i] - (data['CurrentPrice'][i] - data['BuyPrice'][i]) * (data['TaxRate'] / 100) - data['CurrentPrice'][i] * (data['TransactionRate'] / 100))
        for i in range(data['N'])
    ) >= data['K'], "Amount_Raised"
)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')