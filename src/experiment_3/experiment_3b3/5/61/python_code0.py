import pulp

# Load data
data = {
  'processing_times': {
    'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]},
    'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}
  },
  'costs': {
    'central': 150,
    'distributed': 70
  },
  'max_hours': {
    'central_max_hours': 16,
    'distributed_max_hours': 33
  }
}

# Parameters
N = len(data['processing_times']['central']['isolate'])
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Decision variables
problem = pulp.LpProblem("MILP_Intervention_Problem", pulp.LpMinimize)

x_vars = {}
for i in range(N):
    x_vars[i, 'isolate_central'] = pulp.LpVariable(f'x_{i}_isolate_central', cat='Binary')
    x_vars[i, 'scan_central'] = pulp.LpVariable(f'x_{i}_scan_central', cat='Binary')
    x_vars[i, 'isolate_distributed'] = pulp.LpVariable(f'x_{i}_isolate_distributed', cat='Binary')
    x_vars[i, 'scan_distributed'] = pulp.LpVariable(f'x_{i}_scan_distributed', cat='Binary')

y_central = pulp.LpVariable('y_central', lowBound=0)
y_distributed = pulp.LpVariable('y_distributed', lowBound=0)

# Objective function
problem += pulp.lpSum(
    x_vars[i, 'isolate_central'] * central_cost * data['processing_times']['central']['isolate'][i] +
    x_vars[i, 'scan_central'] * central_cost * data['processing_times']['central']['scan'][i] +
    x_vars[i, 'isolate_distributed'] * distributed_cost * data['processing_times']['distributed']['isolate'][i] +
    x_vars[i, 'scan_distributed'] * distributed_cost * data['processing_times']['distributed']['scan'][i]
    for i in range(N)
)

# Constraints
for i in range(N):
    problem += x_vars[i, 'isolate_central'] + x_vars[i, 'scan_central'] == 1
    problem += x_vars[i, 'isolate_distributed'] + x_vars[i, 'scan_distributed'] == 1

problem += y_central == pulp.lpSum(
    x_vars[i, 'isolate_central'] * data['processing_times']['central']['isolate'][i] +
    x_vars[i, 'scan_central'] * data['processing_times']['central']['scan'][i]
    for i in range(N)
)

problem += y_distributed == pulp.lpSum(
    x_vars[i, 'isolate_distributed'] * data['processing_times']['distributed']['isolate'][i] +
    x_vars[i, 'scan_distributed'] * data['processing_times']['distributed']['scan'][i]
    for i in range(N)
)

problem += y_central <= max_central
problem += y_distributed <= max_distributed

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')