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

#### Given data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

#### Problem Definition
N = len(num)  #### Number of days
total_days = N  #### Total number of days we need to cover
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')  #### Total number of employees to hire

#### Create a problem
problem = pulp.LpProblem("Cafeteria_Staffing_Problem", pulp.LpMinimize)

#### Decision variables: whether employee i is working on day n
is_work = pulp.LpVariable.dicts("is_work", (range(total_days), range(total_number)), cat='Binary')

#### Objective Function
problem += total_number, "Minimize_Employees"

#### Constraints: Ensure sufficient staff for each day
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(total_number)) >= num[n], f"Staff_requirement_day_{n}"

#### Constraints: Employee working structure
for i in range(total_number):
    for n in range(total_days):
        for k in range(n_working_days):
            if n + k < total_days:
                problem += is_work[n + k][i] == 1  #### Employee works for n_working_days
        for k in range(n_resting_days):
            if n + n_working_days + k < total_days:
                problem += is_work[n + n_working_days + k][i] == 0  #### Employee rests for n_resting_days

#### Solve the problem
problem.solve()

#### Collecting results
total_employees = int(pulp.value(total_number))
is_work_schedule = [[int(pulp.value(is_work[n][i])) for n in range(total_days)] for i in range(total_employees)]

#### Output results
output = {
    "total_number": total_employees,
    "is_work": is_work_schedule
}

#### Print Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

#### Print output
print(json.dumps(output))
```

