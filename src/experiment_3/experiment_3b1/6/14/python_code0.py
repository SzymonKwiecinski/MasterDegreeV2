import pulp

# Data from the provided JSON
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

# Initializing the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("production", range(data['P']), lowBound=0)  # Production quantities
upgrade = pulp.LpVariable("upgrade", cat='Binary')  # Upgrade machine variable

# Objective function
problem += pulp.lpSum((data['Price'][i] * x[i] - data['Cost'][i] * x[i] - data['InvestPercentage'][i] * (data['Price'][i] * x[i])) for i in range(data['P']))

# Constraints
problem += pulp.lpSum(data['Hour'][i] * x[i] for i in range(data['P'])) <= data['AvailableHours'] + upgrade * data['UpgradeHours'], "Machine_Hour_Constraint"
problem += pulp.lpSum((data['Cost'][i] + data['InvestPercentage'][i] * data['Price'][i]) * x[i] for i in range(data['P'])) <= data['Cash'] + upgrade * data['UpgradeCost'], "Cash_Constraint"

# Solve the problem
problem.solve()

# Print the results
production_quantities = [x[i].varValue for i in range(data['P'])]
net_income = pulp.value(problem.objective)
upgrade_decision = upgrade.varValue == 1

print(f'Net Income: {net_income}, Production Quantities: {production_quantities}, Upgrade Required: {upgrade_decision}')
print(f' (Objective Value): <OBJ>{net_income}</OBJ>')