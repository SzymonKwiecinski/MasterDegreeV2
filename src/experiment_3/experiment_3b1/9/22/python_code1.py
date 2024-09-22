import pulp
import json

# Load data from JSON format
data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

K = len(data['requirement'])  # Number of manpower categories
I = len(data['requirement'][0])  # Number of years

# Create the problem
problem = pulp.LpProblem("Manpower_Optimization", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=None, cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=data['num_shortwork'], cat='Integer')

# Objective function
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] * data['moreonewaste'][k]) + 
                      data['costoverman'][k] * overmanning[(k, i)] +
                      data['costshort'][k] * short[(k, i)] 
                      for k in range(K) for i in range(I)), "Total_Cost"

# Constraints
# Manpower requirements
for k in range(K):
    for i in range(I):
        problem += (data['strength'][k] * (1 - data['moreonewaste'][k]) + 
                     recruit[(k, i)] * (1 - data['lessonewaste'][k]) + 
                     overmanning[(k, i)] + 
                     0.5 * short[(k, i)] == 
                     data['requirement'][k][i], 
                     f"Manpower_Requirement_{k}_{i}")

# Recruitment limits
for k in range(K):
    for i in range(I):
        problem += (recruit[(k, i)] >= 0, f"Recruit_NonNegativity_{k}_{i}")

# Overmanning limits
problem += (pulp.lpSum(overmanning[(k, i)] for k in range(K) for i in range(I)) <= data['num_overman'], "Max_Overman")

# Short-time working limits
for k in range(K):
    for i in range(I):
        problem += (short[(k, i)] >= 0, f"Short_NonNegativity_{k}_{i}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')