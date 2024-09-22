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
import json

#### Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

#### Create the LP problem
problem = pulp.LpProblem("Cafeteria_Staffing_Problem", pulp.LpMinimize)

#### Decision variables
total_number = pulp.LpVariable('total_number', lowBound=1, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(1, total_number+1)), cat='Binary')

#### Objective function: Minimize the number of employees
problem += total_number

#### Constraints: Ensure enough staff on each day
for day in range(N):
    problem += pulp.lpSum(is_work[day][i] for i in range(1, total_number+1) if i <= total_number) >= num[day]

#### Each employee works n_working_days and rests n_resting_days
for i in range(1, total_number + 1):
    for day in range(N):
        for j in range(n_working_days):
            if day + j < N:
                problem += is_work[day + j][i] <= 1  #### They cannot work on overlapping days
        for j in range(n_resting_days):
            if day + n_working_days + j < N:
                problem += is_work[day + n_working_days + j][i] == 0  #### They must rest after working days

#### Solve the problem
problem.solve()

#### Prepare output
total_employees = int(pulp.value(total_number))
work_schedule = [[int(pulp.value(is_work[day][i])) for day in range(N)] for i in range(1, total_employees + 1)]

#### Print output in required format
output = {
    "total_number": total_employees,
    "is_work": work_schedule
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

