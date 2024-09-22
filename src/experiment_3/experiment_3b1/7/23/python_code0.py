import pulp
import json

# Given JSON data
data = json.loads("{'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 'strength': [2000, 1500, 1000], 'lessonewaste': [0.25, 0.2, 0.1], 'moreonewaste': [0.1, 0.05, 0.05], 'recruit': [500, 800, 500], 'costredundancy': [200, 500, 500], 'num_overman': 150, 'costoverman': [1500, 2000, 3000], 'num_shortwork': 50, 'costshort': [500, 400, 400]}".replace("'", "\""))

# Extract data
requirement = data['requirement']
strength = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit = data['recruit']
costredundancy = data['costredundancy']
num_overman = data['num_overman']
costoverman = data['costoverman']
num_shortwork = data['num_shortwork']
costshort = data['costshort']

# Create the problem
K = len(requirement)  # number of manpower categories
I = len(requirement[0])  # number of years
problem = pulp.LpProblem("Manpower_Optimization", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("Recruit", (range(K), range(I)), lowBound=0, cat='Continuous')
overmanning_vars = pulp.LpVariable.dicts("Overmanning", (range(K), range(I)), lowBound=0, cat='Continuous')
short_vars = pulp.LpVariable.dicts("Short", (range(K), range(I)), lowBound=0, cat='Continuous')
redundancy_vars = pulp.LpVariable.dicts("Redundancy", (range(K), range(I)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(costredundancy[k] * redundancy_vars[k][i] +
                      costoverman[k] * overmanning_vars[k][i] +
                      costshort[k] * short_vars[k][i]
                      for k in range(K) for i in range(I))

# Constraints

# Manpower requirement
for k in range(K):
    for i in range(I):
        problem += (strength[k] + recruit_vars[k][i] - redundancy_vars[k][i] - 
                    moreonewaste[k] * (strength[k] + recruit_vars[k][i]) - 
                    short_vars[k][i] >= requirement[k][i])

# Recruitment limits
for k in range(K):
    for i in range(I):
        problem += recruit_vars[k][i] <= recruit[k]

# Overman constraints
problem += pulp.lpSum(overmanning_vars[k][i] for k in range(K) for i in range(I)) <= num_overman

# Short-time working constraints
for k in range(K):
    for i in range(I):
        problem += short_vars[k][i] <= num_shortwork

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')