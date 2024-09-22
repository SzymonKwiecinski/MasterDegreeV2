import pulp

# Data extracted from the JSON provided
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

# Problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['P'])]
y = pulp.LpVariable('y', cat='Binary')

# Objective Function
profit_terms = [(data['Price'][i] - data['Cost'][i] - data['InvestPercentage'][i] * data['Price'][i]) * x[i] for i in range(data['P'])]
problem += pulp.lpSum(profit_terms) - y * data['UpgradeCost']

# Cash availability constraint
cash_constraint = [
    data['Cost'][i] * x[i] for i in range(data['P'])
]
invest_revenue = [
    data['InvestPercentage'][i] * data['Price'][i] * x[i] for i in range(data['P'])
]
problem += pulp.lpSum(cash_constraint) <= data['Cash'] + pulp.lpSum(invest_revenue)

# Machine capacity constraint
machine_hours = [
    data['Hour'][i] * x[i] for i in range(data['P'])
]
problem += pulp.lpSum(machine_hours) <= data['AvailableHours'] + y * data['UpgradeHours']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')