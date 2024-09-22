import pulp
import json

# Data extracted from the JSON format
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

# Sets and indices
K = range(len(data['strength']))  # manpower categories
I = range(len(data['requirement'][0]))  # years

# Create the problem
problem = pulp.LpProblem("Manpower_Optimization", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", (K, I), 0, None, pulp.LpInteger)
overmanning = pulp.LpVariable.dicts("overmanning", (K, I), 0, None, pulp.LpInteger)
short = pulp.LpVariable.dicts("short", (K, I), 0, None, pulp.LpInteger)
redundancy = pulp.LpVariable.dicts("redundancy", (K, I), 0, None, pulp.LpInteger)
employed = pulp.LpVariable.dicts("employed", (K, I), 0, None, pulp.LpInteger)

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * redundancy[k][i] +
                       data['costoverman'][k] * overmanning[k][i] +
                       data['costshort'][k] * short[k][i] 
                       for k in K for i in I)

# Constraints
for k in K:
    # Initial employed in year 1
    problem += (employed[k][0] == data['strength'][k] - data['moreonewaste'][k] * data['strength'][k] +
                 recruit[k][0])

for k in K:
    for i in range(1, len(I)):
        # Employed calculation for years > 1
        problem += (employed[k][i] == (employed[k][i-1] - 
                                         (data['lessonewaste'][k] * recruit[k][i-1] + 
                                          data['moreonewaste'][k] * (employed[k][i-1] - recruit[k][i-1])) +
                                         recruit[k][i]))

for k in K:
    for i in I:
        # Employed must meet requirement and overmanning
        problem += (employed[k][i] == data['requirement'][k][i] + overmanning[k][i] + 
                     0.5 * short[k][i])

for k in K:
    for i in I:
        # Recruitment limits
        problem += (recruit[k][i] <= data['recruit'][k])

for i in I:
    # Overmanning limit
    problem += (pulp.lpSum(overmanning[k][i] for k in K) <= data['num_overman'])

for k in K:
    for i in I:
        # Short-time worker limit
        problem += (short[k][i] <= data['num_shortwork'])

for k in K:
    for i in I:
        # Redundancy calculation
        problem += (redundancy[k][i] == employed[k][i] - 
                     (data['requirement'][k][i] + overmanning[k][i] + 
                      0.5 * short[k][i]))

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')