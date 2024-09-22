import pulp
import numpy as np

# Input data
data = {
    'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]],
    'strength': [2000, 1500, 1000],
    'lessonewaste': [0.25, 0.2, 0.1],
    'moreonewaste': [0.1, 0.05, 0.05],
    'recruit': [500, 800, 500],
    'costredundancy': [200, 500, 500],
    'num_overman': 150,
    'num_shortwork': 50
}

K = len(data['strength']) # Number of k
I = len(data['requirement'][0]) # Number of i

# Create the problem instance
problem = pulp.LpProblem("Minimize_Cost_Redundancy", pulp.LpMinimize)

# Decision variables
r = pulp.LpVariable.dicts("r", (range(K), range(I)), lowBound=0, cat='Continuous')
x = pulp.LpVariable.dicts("x", (range(K), range(I)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", (range(K), range(I)), lowBound=0, cat='Continuous')
z = pulp.LpVariable.dicts("z", (range(K), range(I)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['costredundancy'][k] * r[k][i] for k in range(K) for i in range(I))

# Constraints
strength = np.array(data['strength'])
lessonewaste = np.array(data['lessonewaste'])
moreonewaste = np.array(data['moreonewaste'])
requirement = np.array(data['requirement'])

# Strength constraints
for k in range(K):
    for i in range(I - 1):
        problem += (strength[k] - r[k][i] - lessonewaste[k] * x[k][i] - 
                     moreonewaste[k] * (strength[k] - x[k][i]) + x[k][i] + y[k][i] - z[k][i] == 
                     strength[k] - r[k][i] - lessonewaste[k] * x[k][i] - 
                     moreonewaste[k] * (strength[k] - x[k][i]) + x[k][i] + y[k][i] - z[k][i])

# Recruitment constraints
for k in range(K):
    for i in range(I):
        problem += x[k][i] <= data['recruit'][k]

# Overman constraints
for i in range(I):
    problem += pulp.lpSum(y[k][i] for k in range(K)) <= data['num_overman']

# Short work constraints
for k in range(K):
    for i in range(I):
        problem += z[k][i] <= data['num_shortwork']

# Requirement constraints
for k in range(K):
    for i in range(I):
        problem += strength[k] + y[k][i] - (z[k][i] / 2) >= requirement[k][i]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')