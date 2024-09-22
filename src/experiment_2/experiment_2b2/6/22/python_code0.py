import pulp

# Input JSON data
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

# Extract values
requirement = data['requirement']
strength = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit_cap = data['recruit']
costredundancy = data['costredundancy']
num_overman = data['num_overman']
costoverman = data['costoverman']
num_shortwork = data['num_shortwork']
costshort = data['costshort']

K = len(requirement)   # Number of manpower categories
I = len(requirement[0]) # Number of years

# Define LP problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
redundancy = pulp.LpVariable.dicts("redundancy", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective function: Minimize redundancy costs
problem += pulp.lpSum(costredundancy[k] * redundancy[k, i] for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    available_manpower = strength[k]  # Initial manpower strength for each type
    for i in range(I):
        # Available manpower for the year i
        available_manpower = (available_manpower + recruit[k, i] - lessonewaste[k] * recruit[k, i] 
                              - moreonewaste[k] * (available_manpower - recruit[k, i] - redundancy[k, i])) 
        
        # Requirement constraint
        problem += (available_manpower + overmanning[k, i] + 0.5 * short[k, i] 
                    == requirement[k][i] + redundancy[k, i])
        
        # Recruitment capacity constraint
        problem += recruit[k, i] <= recruit_cap[k]
        
        # Overmanning constraint
        problem += overmanning[k, i] <= num_overman
        
        # Short-time work constraint
        problem += short[k, i] <= num_shortwork

# Solve the problem
problem.solve()

# Extract results
result_recruit = [[pulp.value(recruit[k, i]) for i in range(I)] for k in range(K)]
result_overmanning = [[pulp.value(overmanning[k, i]) for i in range(I)] for k in range(K)]
result_short = [[pulp.value(short[k, i]) for i in range(I)] for k in range(K)]

# Output result
output = {
    "recruit": result_recruit,
    "overmanning": result_overmanning,
    "short": result_short
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')