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

\section*{Mathematical Model for Cafeteria Staff Scheduling}

\subsection*{Parameters}
\begin{itemize}
    \item $N$: Total number of days.
    \item $num_n$: Required number of employees on day $n$, where $n = 1, 2, \ldots, N$.
    \item $n_{working\_days}$: Number of consecutive days an employee works.
    \item $n_{resting\_days}$: Number of consecutive days an employee has off.
\end{itemize}

Let $total\_number$ be the total number of employees to hire.

\subsection*{Variables}
Let $is\_work_{n, i}$ be a binary variable defined as follows:
\[
is\_work_{n, i} = 
\begin{cases} 
1 & \text{if employee } i \text{ is working on day } n \\
0 & \text{if employee } i \text{ is resting on day } n 
\end{cases}
\]
for $i = 1, 2, \ldots, total\_number$ and $n = 1, 2, \ldots, N$.

\subsection*{Objective Function}
Minimize the total number of employees:
\[
\text{Minimize } total\_number
\]

\subsection*{Constraints}

1. Staff requirements for each day:
\[
\sum_{i=1}^{total\_number} is\_work_{n, i} \geq num_n \quad \forall n = 1, 2, \ldots, N
\]

2. Work-rest cycle for each employee:
\[
is\_work_{n, i} + is\_work_{n+1, i} + \ldots + is\_work_{n+n_{working\_days}-1, i} = n_{working\_days} \quad \text{for } n \text{ where } n + n_{working\_days} - 1 \leq N
\]
\[
is\_work_{n+n_{working\_days}, i} + is\_work_{n+n_{working\_days}+1, i} + \ldots + is\_work_{n+n_{working\_days}+n_{resting\_days}-1, i} = 0 \quad \text{for } n+n_{working\_days} \text{ where } n+n_{working\_days}+n_{resting\_days}-1 \leq N
\]

3. Binary constraints:
\[
is\_work_{n, i} \in \{0, 1\} \quad \forall n = 1, 2, \ldots, N, \forall i = 1, 2, \ldots, total\_number
\]

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

\section*{Mathematical Model for Cafeteria Staff Scheduling}

\subsection*{Parameters}
\begin{itemize}
    \item $N$: Total number of days.
    \item $num_n$: Required number of employees on day $n$, where $n = 1, 2, \ldots, N$.
    \item $n_{working\_days}$: Number of consecutive days an employee works.
    \item $n_{resting\_days}$: Number of consecutive days an employee has off.
\end{itemize}

Let $total\_number$ be the total number of employees to hire.

\subsection*{Variables}
Let $is\_work_{n, i}$ be a binary variable defined as follows:
\[
is\_work_{n, i} = 
\begin{cases} 
1 & \text{if employee } i \text{ is working on day } n \\
0 & \text{if employee } i \text{ is resting on day } n 
\end{cases}
\]
for $i = 1, 2, \ldots, total\_number$ and $n = 1, 2, \ldots, N$.

\subsection*{Objective Function}
Minimize the total number of employees:
\[
\text{Minimize } total\_number
\]

\subsection*{Constraints}

1. Staff requirements for each day:
\[
\sum_{i=1}^{total\_number} is\_work_{n, i} \geq num_n \quad \forall n = 1, 2, \ldots, N
\]

2. Work-rest cycle for each employee:
\[
is\_work_{n, i} + is\_work_{n+1, i} + \ldots + is\_work_{n+n_{working\_days}-1, i} = n_{working\_days} \quad \text{for } n \text{ where } n + n_{working\_days} - 1 \leq N
\]
\[
is\_work_{n+n_{working\_days}, i} + is\_work_{n+n_{working\_days}+1, i} + \ldots + is\_work_{n+n_{working\_days}+n_{resting\_days}-1, i} = 0 \quad \text{for } n+n_{working\_days} \text{ where } n+n_{working\_days}+n_{resting\_days}-1 \leq N
\]

3. Binary constraints:
\[
is\_work_{n, i} \in \{0, 1\} \quad \forall n = 1, 2, \ldots, N, \forall i = 1, 2, \ldots, total\_number
\]

\end{document}</MATH_MODEL>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
N = len(data['num'])
num_n = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

#### Create the Linear Programming problem
problem = pulp.LpProblem("Cafeteria_Staff_Scheduling", pulp.LpMinimize)

#### Define the total number of employees (to be determined)
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')

#### Define the binary decision variables
is_work = pulp.LpVariable.dicts("is_work", ((n, i) for n in range(N) for i in range(total_number)), 
                                             cat='Binary')

#### Objective function: Minimize the total number of employees
problem += total_number, "Total_Employees"

#### Constraints for staff requirement each day
for n in range(N):
    problem += pulp.lpSum(is_work[(n, i)] for i in range(total_number)) >= num_n[n], f"Staff_requirement_day_{n}"

#### Work-rest cycle constraints for each employee
for i in range(total_number):
    for n in range(N - n_working_days + 1):
        problem += pulp.lpSum(is_work[(n + j, i)] for j in range(n_working_days)) == n_working_days, f"Work_cycle_{n}_{i}"

    for n in range(N - n_working_days - n_resting_days + 1):
        problem += pulp.lpSum(is_work[(n + n_working_days + j, i)] for j in range(n_resting_days)) == 0, f"Rest_cycle_{n}_{i}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

