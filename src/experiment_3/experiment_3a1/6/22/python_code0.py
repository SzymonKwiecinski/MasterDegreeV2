import pulp
import json

data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

requirements = data['requirement']
strength = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit_limit = data['recruit']
costredundancy = data['costredundancy']
num_overman = data['num_overman']
num_shortwork = data['num_shortwork']
costshort = data['costshort']

K = len(strength)  # number of manpower categories
I = len(requirements[0])  # number of years

# Create the linear programming problem
problem = pulp.LpProblem("ManpowerOptimization", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
overmanning_vars = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
short_vars = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(costredundancy[k] * (strength[k] - pulp.lpSum(recruit_vars[k, j] for j in range(I)) - overmanning_vars[k, i] - short_vars[k, i]) for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(I):
        problem += (
            strength[k] +
            pulp.lpSum(recruit_vars[k, j] for j in range(i + 1)) -
            (lessonewaste[k] * strength[k] + moreonewaste[k] * (strength[k] - pulp.lpSum(recruit_vars[k, j] for j in range(i + 1)))) -
            overmanning_vars[k, i] -
            short_vars[k, i] >= requirements[k][i]
        )
        
        # Recruitment limit
        problem += recruit_vars[k, i] <= recruit_limit[k]

        # Short-time working limit
        problem += short_vars[k, i] <= num_shortwork

# Overmanning limit
for i in range(I):
    problem += pulp.lpSum(overmanning_vars[k, i] for k in range(K)) <= num_overman

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')