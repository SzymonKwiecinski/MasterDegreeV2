import pulp

# Data from JSON
data = {
    'P': 2,
    'Cash': 3000,
    'Hour': [2, 6],
    'Cost': [3, 2],
    'Price': [6, 5],
    'InvestPercentage': [0.4, 0.3],
    'UpgradeHours': 2000,
    'UpgradeCost': 400,
    'AvailableHours': 2000
}

# Create the Linear Programming problem
problem = pulp.LpProblem("Production_Planning", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Continuous') for i in range(data['P'])]
y = pulp.LpVariable("y", cat='Binary')

# Objective Function
profit_contributions = [
    (data['Price'][i] - data['Cost'][i] - data['Price'][i] * data['InvestPercentage'][i]) * x[i]
    for i in range(data['P'])
]
problem += pulp.lpSum(profit_contributions) - y * data['UpgradeCost'], "Total_Net_Income"

# Constraints
# Machine capacity constraint with upgrade option
problem += (pulp.lpSum(data['Hour'][i] * x[i] for i in range(data['P'])) <= 
            data['AvailableHours'] + y * data['UpgradeHours']), "Machine_Capacity"

# Cash constraint
cash_constraints = [
    data['Cost'][i] * x[i] for i in range(data['P'])
]
investment_return = [
    data['Price'][i] * data['InvestPercentage'][i] * x[i] for i in range(data['P'])
]
problem += pulp.lpSum(cash_constraints) <= data['Cash'] + pulp.lpSum(investment_return), "Cash_Availability"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')