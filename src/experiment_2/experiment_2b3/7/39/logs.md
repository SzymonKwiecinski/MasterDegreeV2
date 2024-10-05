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

#### Data input
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

#### Unpacking the data
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

#### Create the LP problem
problem = pulp.LpProblem("Minimize_Employees", pulp.LpMinimize)

#### Decision variable for the number of employees
x = pulp.LpVariable('x', lowBound=0, cat='Integer')

#### Decision variables for whether an employee is working on a given day
is_work = [[pulp.LpVariable(f'is_work_{n}_{i}', cat='Binary') for n in range(N)] for i in range(N)]

#### Objective: Minimize the number of employees
problem += x

#### Constraints:
#### Ensure the minimum required employees are working on each day
for n in range(N):
    problem += pulp.lpSum(is_work[i][n] for i in range(N)) >= num[n]

#### Ensure each employee works n_working_days followed by n_resting_days off
for i in range(N):
    for n in range(N):
        if n + n_working_days + n_resting_days <= N:
            problem += pulp.lpSum(is_work[i][j] for j in range(n, n + n_working_days)) <= n_working_days
            for k in range(n + n_working_days, n + n_working_days + n_resting_days):
                problem += is_work[i][k] == 0

#### Solve the problem
problem.solve()

#### Extract the number of employees and their schedules
total_number = int(pulp.value(x))
is_work_result = [[int(pulp.value(is_work[i][n])) for n in range(N)] for i in range(total_number)]

#### Output result
output = {
    "total_number": total_number,
    "is_work": is_work_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

