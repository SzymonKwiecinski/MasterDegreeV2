import pulp
import json

# Data from JSON format
data = json.loads("""{'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 
                     'strength': [2000, 1500, 1000], 
                     'lessonewaste': [0.25, 0.2, 0.1], 
                     'moreonewaste': [0.1, 0.05, 0.05], 
                     'recruit': [500, 800, 500], 
                     'costredundancy': [200, 500, 500], 
                     'num_overman': 150, 
                     'costoverman': [1500, 2000, 3000], 
                     'num_shortwork': 50, 
                     'costshort': [500, 400, 400]}""")

# Indices
K = len(data['strength'])          # Number of manpower categories
I = len(data['requirement'])       # Number of years

# Create the problem variable
problem = pulp.LpProblem("Manpower_Management", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] - data['requirement'][k][i] + overmanning[k][i]) 
                       for k in range(K) for i in range(I)) + \
           pulp.lpSum(data['costoverman'][k] * overmanning[k][i] 
                       for k in range(K) for i in range(I)) + \
           pulp.lpSum(data['costshort'][k] * short[k][i] 
                       for k in range(K) for i in range(I))

# Constraints
# Employee availability in year i
for i in range(I):
    for k in range(K):
        problem += (data['strength'][k] - data['moreonewaste'][k] * (data['strength'][k] - recruit[k][i]) - short[k][i] >= 
                     data['requirement'][k][i] - overmanning[k][i]), f"availability_{k}_{i}"

# Recruitment limit
for i in range(I):
    for k in range(K):
        problem += recruit[k][i] <= data['recruit'][k], f"recruit_limit_{k}_{i}"

# Wastage rates
for i in range(I):
    for k in range(K):
        problem += (data['strength'][k] * data['lessonewaste'][k] + short[k][i] <= 
                     data['strength'][k] - recruit[k][i]), f"wastage_rate_{k}_{i}"

# Overmanning limit
for i in range(I):
    problem += (pulp.lpSum(overmanning[k][i] for k in range(K)) <= data['num_overman']), f"overmanning_limit_{i}"

# Short-time working limit
for k in range(K):
    for i in range(I):
        problem += short[k][i] <= data['num_shortwork'], f"short_time_limit_{k}_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')