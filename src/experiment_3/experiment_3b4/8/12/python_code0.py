import pulp

# Extracted data
data = {
    'N': 3, 
    'Start': [100.0, 50.0, 200.0], 
    'Limit': [1000.0, 200.0, 3000.0], 
    'Rate': [
        [0.99, 0.9, 1.02], 
        [0.95, 0.99, 0.92], 
        [0.9, 0.91, 0.99]
    ]
}

# Initialize the problem
problem = pulp.LpProblem("Currency_Exchange", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(data['N']) for j in range(data['N'])), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['Rate'][i][data['N'] - 1] * x[i, data['N'] - 1] for i in range(data['N'])), "Maximize_Final_Amount"

# Constraints
# Exchange Limits
for i in range(data['N']):
    problem += pulp.lpSum(x[i, j] for j in range(data['N'])) <= data['Limit'][i], f"Exchange_Limit_{i}"

# Initial Availability
for i in range(data['N']):
    problem += pulp.lpSum(x[j, i] for j in range(data['N'])) <= data['Start'][i], f"Initial_Availability_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')