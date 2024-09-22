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

#### Data from JSON
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

#### Extract data
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

#### Problem definition
problem = pulp.LpProblem("EmployeeScheduling", pulp.LpMinimize)

#### Variables
#### Minimum employees needed, initialized to a large number
max_employees_possible = sum(num)  

#### Create decision variables
work_plan = pulp.LpVariable.dicts("work_plan", ((i, n) for i in range(max_employees_possible) for n in range(N)), cat='Binary')
employed = pulp.LpVariable.dicts("employed", (i for i in range(max_employees_possible)), lowBound=0, upBound=1, cat='Integer')

#### Objective function: Minimize total number of employees hired
problem += pulp.lpSum(employed[i] for i in range(max_employees_possible))

#### Constraints
for n in range(N):
    #### Ensure enough employees on each day
    problem += pulp.lpSum(work_plan[i, n] for i in range(max_employees_possible)) >= num[n]

for i in range(max_employees_possible):
    for n in range(N):
        #### Employee i can only work if they are employed
        problem += work_plan[i, n] <= employed[i]

        #### Ensure working schedule is consistent: n_working_days followed by n_resting_days
        if n + n_working_days + n_resting_days <= N:
            #### Working days constraint
            problem += pulp.lpSum(work_plan[i, n + k] for k in range(n_working_days)) >= \
                       n_working_days * (work_plan[i, n] - work_plan[i, n + n_working_days])
            #### Resting days constraint
            for k in range(n_resting_days):
                problem += work_plan[i, n + n_working_days + k] <= (1 - work_plan[i, n] + work_plan[i, n + n_working_days])

#### Solve the problem
problem.solve()

#### Output the results
total_number = int(pulp.value(problem.objective))
is_work = [[int(pulp.value(work_plan[i, n])) for n in range(N)] for i in range(total_number)]

output = {
    "total_number": total_number,
    "is_work": is_work
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

