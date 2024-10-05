import pulp

# Data Input
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

# Extract values for easier reference
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

K = len(requirement)     # Number of manpower types
I = len(requirement[0])  # Number of years

# Create the LP problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision variables
recruit_vars = pulp.LpVariable.dicts("Recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
redundancy_vars = pulp.LpVariable.dicts("Redundancy", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
overmanning_vars = pulp.LpVariable.dicts("Overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short_vars = pulp.LpVariable.dicts("Short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective Function: Minimize redundancy costs
problem += pulp.lpSum(costredundancy[k] * redundancy_vars[k, i] for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(I):
        if i == 0:
            available_strength = strength[k]
        else:
            previous_year = i - 1
            available_strength = ((1 - moreonewaste[k]) * (strength[k] +
                            sum(recruit_vars[k, j] for j in range(i))) + 
                            (1 - lessonewaste[k]) * sum(recruit_vars[k, j] for j in range(i)))

        problem += (available_strength - redundancy_vars[k, i] + recruit_vars[k, i] + 
                   short_vars[k, i] * 0.5 + overmanning_vars[k, i]) >= requirement[k][i]

        problem += recruit_vars[k, i] <= recruit[k]
        problem += short_vars[k, i] <= num_shortwork
        problem += pulp.lpSum(overmanning_vars[k, j] for j in range(I)) <= num_overman

# Solve the problem
problem.solve()

# Prepare the output data
result = {
    "recruit": [[recruit_vars[k, i].varValue for i in range(I)] for k in range(K)],
    "overmanning": [[overmanning_vars[k, i].varValue for i in range(I)] for k in range(K)],
    "short": [[short_vars[k, i].varValue for i in range(I)] for k in range(K)]
}

print(result)

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')