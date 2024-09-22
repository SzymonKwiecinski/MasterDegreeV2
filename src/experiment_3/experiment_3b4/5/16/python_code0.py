import pulp

# Data
data = {
    'O': 2, 
    'P': 2, 
    'L': 3, 
    'Allocated': [8000, 5000], 
    'Price': [38, 33], 
    'Input': [[3, 5], [1, 1], [5, 3]], 
    'Output': [[4, 3], [1, 1], [3, 4]], 
    'Cost': [51, 11, 40]
}

O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_matrix = data['Input']
output_matrix = data['Output']
cost = data['Cost']

# Problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision Variables
execute = pulp.LpVariable.dicts("execute", range(L), lowBound=0, cat='Continuous')

# Objective Function
revenue = pulp.lpSum(
    [price[p] * 
     pulp.lpSum([output_matrix[l][p] * execute[l] for l in range(L)]) 
     for p in range(P)]
) - pulp.lpSum(
    [cost[l] * 
     pulp.lpSum([output_matrix[l][p] * execute[l] for p in range(P)]) 
     for l in range(L)]
)

problem += revenue

# Constraints
# Crude Oil Availability
for i in range(O):
    problem += (pulp.lpSum([input_matrix[l][i] * execute[l] for l in range(L)]) <= allocated[i], f"Crude_Oil_Availability_{i}")

# Solve Problem
problem.solve()

# Output
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')