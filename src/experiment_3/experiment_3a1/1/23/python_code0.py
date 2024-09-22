import pulp
import json

# Sample data in json format
data = json.loads('''
{
    "requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 
    "strength": [2000, 1500, 1000], 
    "lessonewaste": [0.25, 0.2, 0.1], 
    "moreonewaste": [0.1, 0.05, 0.05], 
    "recruit": [500, 800, 500], 
    "costredundancy": [200, 500, 500], 
    "num_overman": 150, 
    "costoverman": [1500, 2000, 3000], 
    "num_shortwork": 50, 
    "costshort": [500, 400, 400]
}
''')

# Extracting data
K = len(data['strength'])  # Number of manpower categories
I = len(data['requirement'])  # Number of years
requirement = data['requirement']
strength = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit_limit = data['recruit']
costredundancy = data['costredundancy']
num_overman = data['num_overman']
costoverman = data['costoverman']
num_shortwork = data['num_shortwork']
costshort = data['costshort']

# Create the linear programming problem
problem = pulp.LpProblem("Workforce_Management", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(
    [costredundancy[k] * max(0, strength[k] - requirement[i][k]) + 
     costoverman[k] * overmanning[k][i] + 
     costshort[k] * short[k][i]
     for k in range(K) for i in range(I)]
)

# Constraints
# Manpower requirement constraint
for i in range(I):
    for k in range(K):
        problem += (strength[k] - (1 - lessonewaste[k]) * (strength[k] - pulp.lpSum(recruit[k][j] for j in range(I))) +
                     overmanning[k][i] + short[k][i] / 2 >= requirement[i][k])

# Recruitment constraint
for i in range(I):
    for k in range(K):
        problem += (recruit[k][i] <= recruit_limit[k])

# Overmanning constraint
for i in range(I):
    problem += (pulp.lpSum(overmanning[k][i] for k in range(K)) <= num_overman)

# Short-time working constraint
for i in range(I):
    for k in range(K):
        problem += (short[k][i] <= num_shortwork)

# Solve the problem
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')