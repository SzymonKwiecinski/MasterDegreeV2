import pulp
import json

# Data provided in JSON format
data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

# Parameters
K = len(data['strength'])  # Number of manpower categories
I = len(data['requirement'][0])  # Number of years

requirement = data['requirement']
strength = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit = data['recruit']
costredundancy = data['costredundancy']
num_overman = data['num_overman']
num_shortwork = data['num_shortwork']
costshort = data['costshort']

# Initialize the problem
problem = pulp.LpProblem("Manpower_Management_Optimization", pulp.LpMinimize)

# Decision Variables
recruits = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(costredundancy[k] * (strength[k] - pulp.lpSum(lessonewaste[k] * strength[k]) - 
                pulp.lpSum(moreonewaste[k] * (strength[k] - pulp.lpSum(recruits[(k, j)] for j in range(I)))) + 
                recruits[(k, i)] + short[(k, i)] + overmanning[(k, i)] 
                for i in range(I) for k in range(K))), "Total_Cost"

# Constraints

# Manpower Requirements
for k in range(K):
    for i in range(I):
        problem += (strength[k] - 
                     lessonewaste[k] * strength[k] * (i + 1) - 
                     moreonewaste[k] * (strength[k] - pulp.lpSum(recruits[(k, j)] for j in range(i + 1))) * (i + 1) + 
                     recruits[(k, i)] + short[(k, i)] + overmanning[(k, i)] >= 
                     requirement[k][i], f"Manpower_Requirement_{k}_{i}")

# Recruitment Limits
for k in range(K):
    for i in range(I):
        problem += recruits[(k, i)] <= recruit[k], f"Recruitment_Limit_{k}_{i}"

# Overmanning Limits
problem += pulp.lpSum(overmanning[(k, i)] for k in range(K) for i in range(I)) <= num_overman, "Overmanning_Limit"

# Short-time Working Limits
for k in range(K):
    for i in range(I):
        problem += short[(k, i)] <= num_shortwork, f"Short_Work_Limit_{k}_{i}"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')