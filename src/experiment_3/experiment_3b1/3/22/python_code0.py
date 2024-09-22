import pulp
import json

# Data provided
data = {
    'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]],
    'strength': [2000, 1500, 1000],
    'lessonewaste': [0.25, 0.2, 0.1],
    'moreonewaste': [0.1, 0.05, 0.05],
    'recruit': [500, 800, 500],
    'costredundancy': [200, 500, 500],
    'num_overman': 150,
    'costoverman': [1500, 2000, 3000],
    'num_shortwork': 50,
    'costshort': [500, 400, 400]
}

K = len(data['strength'])  # Number of categories
I = len(data['requirement'])  # Number of years

# Create the problem
problem = pulp.LpProblem("Manpower_Requirement", pulp.LpMinimize)

# Decision Variables
r = pulp.LpVariable.dicts("r", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
o = pulp.LpVariable.dicts("o", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
s = pulp.LpVariable.dicts("s", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * (r[k, i] + o[k, i]) for k in range(K) for i in range(I)) \
                     + pulp.lpSum(data['costoverman'][k] * o[k, i] for k in range(K) for i in range(I)) \
                     + pulp.lpSum(data['costshort'][k] * s[k, i] for k in range(K) for i in range(I))

# Constraints
# Manpower requirements
for k in range(K):
    for i in range(I):
        problem += (data['strength'][k] + r[k, i] - 
                     data['lessonewaste'][k] * r[k, i] - 
                     data['moreonewaste'][k] * data['strength'][k] + 
                     o[k, i] + 
                     0.5 * s[k, i] >= data['requirement'][i][k])

# Recruitment limits
for k in range(K):
    for i in range(I):
        problem += r[k, i] <= data['recruit'][k]

# Overmanning limits
for k in range(K):
    for i in range(I):
        problem += o[k, i] <= data['num_overman']

# Short-time working limits
for k in range(K):
    for i in range(I):
        problem += s[k, i] <= data['num_shortwork']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')