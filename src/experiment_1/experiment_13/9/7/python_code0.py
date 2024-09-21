import pulp

# Data from the provided JSON format
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

# Number of shares
N = data['N']

# Create the problem variable
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum((data['Bought'][i] - x[i]) * data['FuturePrice'][i] for i in range(N)), "Total_Value"

# Constraints
# Non-negativity constraint is handled by the lowBound in the variable definition

# Cannot sell more than bought constraint
for i in range(N):
    problem += x[i] <= data['Bought'][i], f"Cannot_Sell_More_Than_Bought_{i}"

# Amount raised constraint
problem += pulp.lpSum(
    x[i] * (data['CurrentPrice'][i] - (data['CurrentPrice'][i] - data['BuyPrice'][i]) * data['TaxRate'] / 100 - data['CurrentPrice'][i] * data['TransactionRate']) for i in range(N)
) >= data['K'], "Amount_Raised_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')