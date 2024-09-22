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

#### Parameters
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)
total_days = N

#### Define the problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

#### Variables
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", (range(total_days), range(total_number)), cat='Binary')

#### Constraints
for day in range(total_days):
    problem += pulp.lpSum(is_work[day][i] for i in range(total_number) if is_work[day][i] == 1) >= num[day]

#### Working days and resting days constraints
for i in range(total_number):
    for day in range(total_days):
        for wd in range(n_working_days):
            if day + wd < total_days:
                problem += is_work[day + wd][i] <= 1  #### Cannot work more than one shift in a day
        for rd in range(n_resting_days):
            if day + n_working_days + rd < total_days:
                problem += is_work[day + n_working_days + rd][i] == 0  #### Resting days

#### Objective function
problem += total_number, "Objective"

#### Solve the problem
problem.solve()

#### Prepare the output
is_work_output = [[int(is_work[n][i].value()) for n in range(total_days)] for i in range(int(total_number.value()))]

#### Print result
output = {
    "total_number": int(total_number.value()),
    "is_work": is_work_output
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

