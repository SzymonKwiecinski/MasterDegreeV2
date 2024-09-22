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
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(data['P']), lowBound=0)  # production quantity of products
u = pulp.LpVariable("u", cat='Binary')  # binary variable for machine upgrade

# Objective Function
problem += pulp.lpSum((data['Price'][i] * x[i] - 
                        data['Cost'][i] * x[i] - 
                        data['InvestPercentage'][i] * data['Price'][i] * x[i]) for i in range(data['P'])) - data['UpgradeCost'] * u, "Total_Profit"

# Constraints
# Cash Constraint
problem += pulp.lpSum(data['Cost'][i] * x[i] for i in range(data['P'])) <= data['Cash'] + \
            pulp.lpSum(data['InvestPercentage'][i] * data['Price'][i] * x[i] for i in range(data['P'])), "Cash_Constraint"

# Machine Hours Constraint
problem += pulp.lpSum(data['Hour'][i] * x[i] for i in range(data['P'])) <= data['AvailableHours'] + data['UpgradeHours'] * u, "Machine_Hours_Constraint"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')