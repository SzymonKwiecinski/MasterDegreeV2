import pulp
import json

# Data from the provided JSON
data = {'large_roll_width': 70, 
        'demands': [40, 65, 80, 75], 
        'roll_width_options': [17, 14, 11, 8.5], 
        'patterns': [[4, 0, 0, 0], [3, 1, 0, 0], [3, 0, 1, 0], [2, 2, 0, 0], 
                     [3, 0, 0, 2], [2, 1, 2, 0], [2, 1, 1, 1], [2, 1, 0, 2], 
                     [2, 0, 3, 0], [2, 0, 2, 1], [2, 0, 1, 2], [1, 3, 1, 0], 
                     [1, 3, 0, 1], [1, 2, 2, 0], [1, 2, 1, 1], [1, 2, 0, 2], 
                     [1, 1, 3, 0], [0, 5, 0, 0], [0, 4, 1, 0], [0, 4, 0, 1], 
                     [0, 3, 2, 0], [2, 0, 0, 4], [1, 1, 2, 2], [1, 1, 1, 3], 
                     [1, 1, 0, 4], [1, 0, 4, 1], [1, 0, 3, 2], [1, 0, 2, 3], 
                     [1, 0, 1, 4], [0, 3, 1, 2], [0, 3, 0, 3], [0, 2, 3, 1], 
                     [0, 2, 2, 2], [0, 2, 1, 3], [0, 2, 0, 4], [0, 1, 5, 0], 
                     [0, 1, 4, 1], [0, 1, 3, 2], [0, 0, 6, 0], [0, 0, 5, 1], 
                     [1, 0, 0, 6], [0, 1, 2, 4], [0, 1, 1, 5], [0, 1, 0, 6], 
                     [0, 0, 4, 3], [0, 0, 3, 4], [0, 0, 2, 5], [0, 0, 1, 6], 
                     [0, 0, 0, 8]]}

# Define problem
problem = pulp.LpProblem("Paper_Cutting_Problem", pulp.LpMinimize)

# Decision Variables
N = len(data['patterns'])
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat='Integer')
z = pulp.LpVariable("z", lowBound=0, cat='Integer')

# Objective Function
problem += z

# Constraints
# Demand Satisfaction
for j, demand in enumerate(data['demands']):
    problem += pulp.lpSum(x[i] * data['patterns'][i][j] for i in range(N)) >= demand

# Large Roll Width
for i in range(N):
    problem += pulp.lpSum(data['patterns'][i][j] * x[i] for j in range(len(data['roll_width_options']))) <= data['large_roll_width']

# Solving the problem
problem.solve()

# Output
patterns_used = {f'pattern_{i}': pulp.value(x[i]) for i in range(N)}
total_large_rolls_used = pulp.value(z)

print(f'Patterns used: {patterns_used}')
print(f'Total large rolls used: {total_large_rolls_used}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')