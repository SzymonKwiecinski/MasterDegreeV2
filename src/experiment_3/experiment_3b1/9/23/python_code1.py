import pulp
import json

# Load the data
data = json.loads("""{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}""")

# Model parameters
K = len(data['requirement'])  # Number of categories
I = len(data['requirement'][0])  # Number of years

# Create the problem
problem = pulp.LpProblem("Manpower_Optimization", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, cat='Continuous')
overmanning = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, cat='Continuous')
short = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] + pulp.lpSum(recruit[k][i] for i in range(I)) - 
             (data['lessonewaste'][k] * pulp.lpSum(recruit[k][j] for j in range(i + 1)) + 
              data['moreonewaste'][k] * (data['strength'][k] + pulp.lpSum(recruit[k][m] for m in range(i)) )) for k in range(K) for i in range(I))) + \
         pulp.lpSum(data['costoverman'][k] * overmanning[k][i] for k in range(K) for i in range(I)) + \
         pulp.lpSum(data['costshort'][k] * short[k][i] for k in range(K) for i in range(I))

# Constraints
# 1. Meeting manpower requirements
for k in range(K):
    for i in range(I):
        problem += (data['strength'][k] + pulp.lpSum(recruit[k][j] for j in range(I)) - 
                     (data['lessonewaste'][k] * pulp.lpSum(recruit[k][j] for j in range(i+1)) + 
                      data['moreonewaste'][k] * (data['strength'][k] + pulp.lpSum(recruit[k][m] for m in range(i)))) + 
                     pulp.lpSum(overmanning[k][j] for j in range(I)) - 
                     pulp.lpSum(short[k][j] for j in range(I)) >= data['requirement'][k][i])

# 2. Recruitment Limit
for k in range(K):
    problem += pulp.lpSum(recruit[k][i] for i in range(I)) <= data['recruit'][k]

# 3. Overmanning Limit
problem += pulp.lpSum(overmanning[k][i] for k in range(K) for i in range(I)) <= data['num_overman']

# 4. Short-time working Limit
for k in range(K):
    problem += pulp.lpSum(short[k][i] for i in range(I)) <= data['num_shortwork']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')