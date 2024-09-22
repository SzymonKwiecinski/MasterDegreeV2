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

#### Initialize the LP problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

#### Define the number of employees
max_employees = sum(num)  #### An upper bound for the number of employees
employees = pulp.LpVariable.dicts("employee", range(max_employees), 0, 1, pulp.LpBinary)

#### Objective function: Minimize the total number of employees
problem += pulp.lpSum(employees[i] for i in range(max_employees)), "Total_Employees"

#### Constraints
for day in range(N):
    #### Number of employees required on this day
    required = num[day]
    #### Sum up the working employees for the required days
    problem += pulp.lpSum(employees[i] for i in range(max_employees) if (i % (n_working_days + n_resting_days)) < n_working_days) >= required, f"Day_{day+1}_Requirement"

#### Solve the problem
problem.solve()

#### Extract the total number of employees and their work schedules
total_number = int(pulp.value(problem.objective))
is_work = [[0]*N for _ in range(total_number)]

for i in range(total_number):
    for day in range(N):
        if (i % (n_working_days + n_resting_days)) < n_working_days:
            is_work[i][day] = 1

#### Prepare the output
output = {
    "total_number": total_number,
    "is_work": is_work
}

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

