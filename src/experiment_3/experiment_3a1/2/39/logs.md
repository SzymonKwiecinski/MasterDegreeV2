# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
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


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Cafeteria Staff Scheduling}
\author{Operations Research Model}
\date{}
\maketitle

\section*{Problem Definition}

Let \(N\) be the total number of days for which the staff required is known. The number of desired employees on day \(n\) is denoted by \(num_n\). Each employee works \(n_{\text{working\_days}}\) days in a row followed by \(n_{\text{resting\_days}}\) days off.

\section*{Variables}

\begin{align*}
& x: \text{Total number of employees to hire} \\
& is\_work_{n, i}: \text{Binary variable indicating if employee } i \text{ is working on day } n
\end{align*}

\section*{Parameters}

\begin{align*}
& num_n \in \mathbb{Z}^+, \quad n = 1, \ldots, N \\
& n_{\text{working\_days}} \in \mathbb{Z}^+ \\
& n_{\text{resting\_days}} \in \mathbb{Z}^+
\end{align*}

\section*{Objective Function}

The objective is to minimize the total number of employees hired:

\[
\text{Minimize } x
\]

\section*{Constraints}

1. Each day's staffing requirement must be met:

\[
\sum_{i=1}^{x} is\_work_{n, i} \geq num_n, \quad n = 1, \ldots, N
\]

2. Each employee works for \(n_{\text{working\_days}}\) and rests for \(n_{\text{resting\_days}}\):

\[
is\_work_{n, i} = 
\begin{cases}
1 & \text{if employee } i \text{ works on day } n \\
0 & \text{if employee } i \text{ is resting on day } n
\end{cases}
\]

3. Employee's work-rest schedule must be consistent:

\[
is\_work_{n, i} = 1 \text{ for } n \in [k, k + n_{\text{working\_days}} - 1] \implies is\_work_{n + n_{\text{working\_days}}, i} = 0, \quad \text{where } k \text{ is a starting day}
\]

4. Binary constraints on the work variable:

\[
is\_work_{n, i} \in \{0, 1\}
\]

\section*{Output}

The output consists of two variables:

\begin{align*}
& total\_number: x \\
& is\_work: \{[is\_work_{n, i} \text{ for } n = 1, \ldots, N] \text{ for } i = 1, \ldots, total\_number]\}
\end{align*}

\end{document}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Cafeteria Staff Scheduling}
\author{Operations Research Model}
\date{}
\maketitle

\section*{Problem Definition}

Let \(N\) be the total number of days for which the staff required is known. The number of desired employees on day \(n\) is denoted by \(num_n\). Each employee works \(n_{\text{working\_days}}\) days in a row followed by \(n_{\text{resting\_days}}\) days off.

\section*{Variables}

\begin{align*}
& x: \text{Total number of employees to hire} \\
& is\_work_{n, i}: \text{Binary variable indicating if employee } i \text{ is working on day } n
\end{align*}

\section*{Parameters}

\begin{align*}
& num_n \in \mathbb{Z}^+, \quad n = 1, \ldots, N \\
& n_{\text{working\_days}} \in \mathbb{Z}^+ \\
& n_{\text{resting\_days}} \in \mathbb{Z}^+
\end{align*}

\section*{Objective Function}

The objective is to minimize the total number of employees hired:

\[
\text{Minimize } x
\]

\section*{Constraints}

1. Each day's staffing requirement must be met:

\[
\sum_{i=1}^{x} is\_work_{n, i} \geq num_n, \quad n = 1, \ldots, N
\]

2. Each employee works for \(n_{\text{working\_days}}\) and rests for \(n_{\text{resting\_days}}\):

\[
is\_work_{n, i} = 
\begin{cases}
1 & \text{if employee } i \text{ works on day } n \\
0 & \text{if employee } i \text{ is resting on day } n
\end{cases}
\]

3. Employee's work-rest schedule must be consistent:

\[
is\_work_{n, i} = 1 \text{ for } n \in [k, k + n_{\text{working\_days}} - 1] \implies is\_work_{n + n_{\text{working\_days}}, i} = 0, \quad \text{where } k \text{ is a starting day}
\]

4. Binary constraints on the work variable:

\[
is\_work_{n, i} \in \{0, 1\}
\]

\section*{Output}

The output consists of two variables:

\begin{align*}
& total\_number: x \\
& is\_work: \{[is\_work_{n, i} \text{ for } n = 1, \ldots, N] \text{ for } i = 1, \ldots, total\_number]\}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data
data = json.loads('{"num": [5, 10, 2, 3, 2, 10], "n_working_days": 5, "n_resting_days": 2}')
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

#### Number of days
N = len(num)

#### Create the problem
problem = pulp.LpProblem("Cafeteria_Staff_Scheduling", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable("Total_Employees", lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", (range(1, N+1), range(1, 100)), cat='Binary')  #### Assuming a maximum of 100 employees for initialization

#### Objective function
problem += x, "Minimize_Total_Employees"

#### Constraints
#### Each day's staffing requirement must be met
for n in range(1, N + 1):
    problem += pulp.lpSum(is_work[n][i] for i in range(1, 100)) >= num[n - 1], f"Staffing_Requirement_Day_{n}"

#### Each employee's working and resting days schedule must be consistent
for i in range(1, 100):
    for k in range(1, N + 1 - n_working_days):
        problem += pulp.lpSum(is_work[n][i] for n in range(k, k + n_working_days)) == n_working_days, f"Work_Consistency_Employee_{i}_Start_{k}"
        problem += is_work[k + n_working_days][i] == 0, f"Rest_Employee_{i}_After_Start_{k}"

#### The number of employees hired must match the binary variables
for i in range(1, 100):
    problem += pulp.lpSum(is_work[n][i] for n in range(1, N + 1)) <= n_working_days + n_resting_days, f"Max_Work_Rest_Employee_{i}"

problem += x == pulp.lpSum(1 for i in range(1, 100) if pulp.lpSum(is_work[n][i] for n in range(1, N + 1)) > 0), "Total_Employees_Constraint"

#### Solve the problem
problem.solve()

#### Output the results
total_number = pulp.value(x)
is_work_schedule = {i: [pulp.value(is_work[n][i]) for n in range(1, N + 1)] for i in range(1, 100) if pulp.value(is_work[1][i]) is not None}

print(f' (Objective Value): <OBJ>{total_number}</OBJ>')
print(f' (Work Schedule): {is_work_schedule}')
```

