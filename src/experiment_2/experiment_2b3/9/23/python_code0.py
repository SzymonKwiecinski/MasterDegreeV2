import pulp

# Input Data
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

# Extracting data
requirement = data['requirement']
strength = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit_limit = data['recruit']
costredundancy = data['costredundancy']
num_overman = data['num_overman']
costoverman = data['costoverman']
num_shortwork = data['num_shortwork']
costshort = data['costshort']

K = len(strength)  # number of manpower types
I = len(requirement[0])  # number of years

# Initialize the problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("Recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
overmanning = pulp.LpVariable.dicts("Overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("Short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
redundancy = pulp.LpVariable.dicts("Redundancy", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective Function: Minimize Total Costs
total_costs = (
    pulp.lpSum([costredundancy[k] * redundancy[k, i] for k in range(K) for i in range(I)]) +
    pulp.lpSum([costoverman[k] * overmanning[k, i] for k in range(K) for i in range(I)]) +
    pulp.lpSum([costshort[k] * short[k, i] for k in range(K) for i in range(I)])
)

problem += total_costs

# Constraints
for k in range(K):
    employees_last_year = strength[k]
    for i in range(I):
        # Employees available in year i
        employees_now = employees_last_year - redundancy[k, i] - moreonewaste[k] * employees_last_year + recruit[k, i] * (1 - lessonewaste[k])
        
        # Account for short-time working: 2 short-time = 1 full-time
        production_met = employees_now + 0.5 * short[k, i] + overmanning[k, i]
        
        # Requirement Constraint
        problem += production_met >= requirement[k][i], f"Requirement_Constraint_{k}_{i}"
        
        # Recruitment Limit
        problem += recruit[k, i] <= recruit_limit[k], f"Recruitment_Limit_{k}_{i}"
        
        # Short-time working Constraint
        problem += short[k, i] <= num_shortwork, f"Short_Time_Limit_{k}_{i}"
        
        employees_last_year = employees_now

# Overmanning Constraint Sum
problem += pulp.lpSum(overmanning[k, i] for k in range(K) for i in range(I)) <= num_overman, "Overmanning_Constraint"

# Solve the problem
problem.solve()

# Create output
output = {
    "recruit": [[pulp.value(recruit[k, i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[k, i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[k, i]) for i in range(I)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')