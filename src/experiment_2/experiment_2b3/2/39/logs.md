# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP or MILP
PROBLEM INFO:

- To operate a cafeteria, the manager must ensure on-call duty based on the statistics on the required staff. 
- In the future days, the number of desired employees on day \var{n} is denoted with \var{num_{n}}.
- Each employee works \var{n_working_days} days in a row and then has \var{n_resting_days} days off.

INPUT FORMAT:

{
	"num": [num_{n} for n in 1,...,N],
	"n_working_days": n_working_days,
	"n_resting_days": n_resting_days
}


OBJECTIVE: Calculate the minimum number of employees to hire

OUTPUT INFO:

- \var{total_number} represents the total number of employees to employ
- \var{is_work} represents whether employee is working a rest on each day. Its length is determined by \var{total_number}

OUTPUT FORMAT:

{
	"total_number": total_number,
	"is_work": [[is_work_{n, i} for n in 1,...,N] for i in 1,...,total_number]
}
</DESCRIPTION>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Parse the input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

#### Number of days
N = len(num)

#### Define the problem
problem = pulp.LpProblem("Cafeteria_Staffing_Problem", pulp.LpMinimize)

#### Define decision variables
#### x_i: 1 if employee i is hired, 0 otherwise
x = [pulp.LpVariable(f'x{i}', cat='Binary') for i in range(N)]

#### y_i_j: 1 if employee i works on day j, 0 otherwise
y = [[pulp.LpVariable(f'y{i}_{j}', cat='Binary') for j in range(N)] for i in range(N)]

#### Add objective: Minimize the number of employees
problem += pulp.lpSum(x), "Minimize_Employees"

#### Add constraints
#### Ensure each day's staffing requirements are met
for day in range(N):
    problem += pulp.lpSum(y[i][day] for i in range(N)) >= num[day], f"Staffing_Requirement_Day_{day}"

#### Ensure the scheduled working and rest days for each employee
for i in range(N):
    for j in range(N):
        if j + n_working_days <= N:
            #### Employee can work for n_working_days straight
            problem += y[i][j] - pulp.lpSum(y[i][j + k] for k in range(n_working_days)) == 0, f"Working_Block_{i}_{j}"
        if j + n_working_days + n_resting_days <= N:
            #### After working n_working_days, employee must rest for n_resting_days
            problem += pulp.lpSum(y[i][j + n_working_days + k] for k in range(n_resting_days)) == 0, f"Rest_Block_{i}_{j}"

#### Ensure employee i works only if they are hired
for i in range(N):
    for j in range(N):
        problem += y[i][j] <= x[i], f"Working_If_Hired_{i}_{j}"

#### Solve the problem
problem.solve()

#### Prepare the output
total_number = sum(pulp.value(x[i]) for i in range(N))
is_work = [[int(pulp.value(y[i][j])) for j in range(N)] for i in range(N)]

output = {
    "total_number": int(total_number),
    "is_work": [is_work[i] for i in range(N) if pulp.value(x[i]) == 1]
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(output)
```

