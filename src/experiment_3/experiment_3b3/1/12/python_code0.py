import pulp

# Input data
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

# Define the LP problem
problem = pulp.LpProblem("Currency_Exchange_Maximization", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("exchange", [(i, j) for i in range(data['N']) for j in range(data['N'])], lowBound=0, cat='Continuous')

# Objective function: Maximize the final amount of currency N
# Since we are interested in ending up with the maximum amount of currency N (last currency in the list)
problem += data['Start'][-1] - sum(x[i, data['N']-1] for i in range(data['N'])) + sum(data['Rate'][j][data['N']-1] * x[j, data['N']-1] for j in range(data['N']))

# Constraints
# 1. Limit Constraints
for i in range(data['N']):
    problem += sum(x[i, j] for j in range(data['N'])) <= data['Limit'][i]

# 2. Initial Amount Constraints
for i in range(data['N']):
    problem += data['Start'][i] - sum(x[i, j] for j in range(data['N'])) + sum(x[j, i] for j in range(data['N'])) == data['Start'][i]

# 3. Non-Negativity Constraints are already ensured by 'lowBound=0' in the LpVariable

# 4. Wealth Preservation Constraints (Checking simple cycles is a heuristic approach, not implemented here)

# Solve the problem
problem.solve()

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')