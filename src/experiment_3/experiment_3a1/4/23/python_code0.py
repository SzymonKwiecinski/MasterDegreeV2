import pulp
import json

# Load data from the provided JSON
data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

# Extracting data for easier reference
requirements = data['requirement']
strengths = data['strength']
less_one_waste = data['lessonewaste']
more_one_waste = data['moreonewaste']
recruits = data['recruit']
cost_redundancy = data['costredundancy']
num_overman = data['num_overman']
cost_overman = data['costoverman']
num_short_work = data['num_shortwork']
cost_short = data['costshort']

K = len(requirements)  # Number of manpower categories
I = len(requirements[0])  # Number of years

# Create the LP problem
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), 
                                      lowBound=0, upBound=None, cat='Integer')
overmanning_vars = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), 
                                             lowBound=0, upBound=None, cat='Integer')
short_vars = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), 
                                      lowBound=0, upBound=None, cat='Integer')

# Objective Function
problem += pulp.lpSum(cost_redundancy[k] * (recruit_vars[k, i] - strengths[k] * more_one_waste[k] if i > 0 else 0) +
                      cost_overman[k] * overmanning_vars[k, i] +
                      cost_short[k] * short_vars[k, i]
                      for k in range(K) for i in range(I))

# Constraints
for i in range(I):
    for k in range(K):
        problem += (strengths[k] * (1 - more_one_waste[k]) + recruit_vars[k, i] + overmanning_vars[k, i] -
                     short_vars[k, i] == requirements[k][i])

        problem += (recruit_vars[k, i] <= recruits[k])
        
        if i == 0:  # Only for the first year, apply redundancy constraint
            problem += (recruit_vars[k, i] <= strengths[k])
        problem += (short_vars[k, i] <= num_short_work)

for i in range(I):
    problem += pulp.lpSum(overmanning_vars[k, i] for k in range(K)) <= num_overman

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')