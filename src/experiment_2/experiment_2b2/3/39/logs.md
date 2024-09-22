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

#### Extracting data from JSON
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

#### Total period for an employee's cycle
total_cycle_days = n_working_days + n_resting_days

#### Problem
problem = pulp.LpProblem("Minimum_Employees", pulp.LpMinimize)

#### Variables
x = pulp.LpVariable.dicts("x", range(N), cat='Binary')  #### Employee starting work on day n
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')

#### Objective Function: Minimize the total number of employees
problem += total_number

#### Constraints
#### Ensure each day's employee requirement is met
for day in range(N):
    problem += (pulp.lpSum(x[(day - start) % N] for start in range(total_cycle_days) if start < n_working_days) >= num[day])

#### Total number of employees should be at least the sum of start days where employees start
problem += total_number == pulp.lpSum(x[i] for i in range(N))

#### Solve the problem
problem.solve()

#### Preparing Output
total_number_value = int(pulp.value(total_number))
is_work = [[0] * N for _ in range(total_number_value)]

#### Filling the work schedule for each employee
employee_count = 0
for start_day in range(N):
    if pulp.value(x[start_day]) > 0.5:
        for day in range(start_day, start_day + n_working_days):
            is_work[employee_count][day % N] = 1
        employee_count += 1

#### Generating final output
output = {
    "total_number": total_number_value,
    "is_work": is_work
}

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

#### Output the result
print(output)
```

