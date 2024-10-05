import pulp
import json

# Data from the JSON format
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

# Set of manpower categories and future years
K = range(len(data['strength']))  # index for manpower categories
I = range(len(data['requirement'][0]))  # index for future years

# Create the LP problem
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", (K, I), lowBound=0)
overmanning = pulp.LpVariable.dicts("overmanning", (K, I), lowBound=0)
short = pulp.LpVariable.dicts("short", (K, I), lowBound=0, upBound=data['num_shortwork'])
redundancy = pulp.LpVariable.dicts("redundancy", (K, I), lowBound=0)
workforce = pulp.LpVariable.dicts("workforce", (K, I), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * redundancy[k][i] + 
                       data['costoverman'][k] * overmanning[k][i] + 
                       data['costshort'][k] * short[k][i] 
                       for k in K for i in I)

# Constraints
for k in K:
    for i in I:
        if i > 0:
            problem += (workforce[k][i] == 
                         recruit[k][i] + 
                         (1 - data['lessonewaste'][k]) * recruit[k][i-1] + 
                         (1 - data['moreonewaste'][k]) * (workforce[k][i-1] - recruit[k][i-1] - redundancy[k][i-1]))

        # Satisfy manpower requirement
        problem += (workforce[k][i] + overmanning[k][i] >= data['requirement'][k][i])
        
        # Short-time working adjustment
        problem += (workforce[k][i] + 0.5 * short[k][i] >= data['requirement'][k][i])

        # Recruitment limit
        problem += (recruit[k][i] <= data['recruit'][k])

# Overmanning limit
for i in I:
    problem += (pulp.lpSum(overmanning[k][i] for k in K) <= data['num_overman'])

# Short-time working limit
for k in K:
    for i in I:
        problem += (short[k][i] <= data['num_shortwork'])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')