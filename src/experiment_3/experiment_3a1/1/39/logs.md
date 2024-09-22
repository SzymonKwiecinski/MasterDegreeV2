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

\section*{Mathematical Model for Cafeteria Staffing}

\subsection*{Parameters}
\begin{itemize}
    \item $N$: Number of days
    \item $num_n$: Number of employees required on day $n$, for $n = 1, 2, \ldots, N$
    \item $n\_working\_days$: Number of consecutive working days for each employee
    \item $n\_resting\_days$: Number of consecutive days off for each employee
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $total\_number$: Total number of employees to hire
    \item $is\_work_{n,i}$: Binary variable indicating whether employee $i$ is working on day $n$ ($is\_work_{n,i} = 1$ if employee $i$ works on day $n$, 0 otherwise), for $n = 1, \ldots, N$ and $i = 1, \ldots, total\_number$
\end{itemize}

\subsection*{Objective Function}
Minimize the total number of employees:
\[
\text{Minimize } total\_number
\]

\subsection*{Constraints}
1. Ensure that the number of employees working meets the requirement for each day:
\[
\sum_{i=1}^{total\_number} is\_work_{n,i} \geq num_n, \quad \forall n = 1, \ldots, N
\]
2. Define the working and resting schedule for each employee:
If an employee starts working on day $d$, they will work for $n\_working\_days$ and rest for $n\_resting\_days$. Thus:
\[
is\_work_{n,i} = 
\begin{cases}
1 & \text{if } (n - d) \mod (n\_working\_days + n\_resting\_days) < n\_working\_days \\
0 & \text{otherwise}
\end{cases}, \quad \forall i = 1, \ldots, total\_number, \forall n
\]

\subsection*{Output Information}
The output should provide:
\begin{itemize}
    \item $total\_number$: Total number of employees hired.
    \item $is\_work$: A matrix where element $is\_work_{n,i}$ indicates the working status of employee $i$ on day $n$.
\end{itemize}

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

\section*{Mathematical Model for Cafeteria Staffing}

\subsection*{Parameters}
\begin{itemize}
    \item $N$: Number of days
    \item $num_n$: Number of employees required on day $n$, for $n = 1, 2, \ldots, N$
    \item $n\_working\_days$: Number of consecutive working days for each employee
    \item $n\_resting\_days$: Number of consecutive days off for each employee
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $total\_number$: Total number of employees to hire
    \item $is\_work_{n,i}$: Binary variable indicating whether employee $i$ is working on day $n$ ($is\_work_{n,i} = 1$ if employee $i$ works on day $n$, 0 otherwise), for $n = 1, \ldots, N$ and $i = 1, \ldots, total\_number$
\end{itemize}

\subsection*{Objective Function}
Minimize the total number of employees:
\[
\text{Minimize } total\_number
\]

\subsection*{Constraints}
1. Ensure that the number of employees working meets the requirement for each day:
\[
\sum_{i=1}^{total\_number} is\_work_{n,i} \geq num_n, \quad \forall n = 1, \ldots, N
\]
2. Define the working and resting schedule for each employee:
If an employee starts working on day $d$, they will work for $n\_working\_days$ and rest for $n\_resting\_days$. Thus:
\[
is\_work_{n,i} = 
\begin{cases}
1 & \text{if } (n - d) \mod (n\_working\_days + n\_resting\_days) < n\_working\_days \\
0 & \text{otherwise}
\end{cases}, \quad \forall i = 1, \ldots, total\_number, \forall n
\]

\subsection*{Output Information}
The output should provide:
\begin{itemize}
    \item $total\_number$: Total number of employees hired.
    \item $is\_work$: A matrix where element $is\_work_{n,i}$ indicates the working status of employee $i$ on day $n$.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import numpy as np

#### Data from JSON format
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num_n = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num_n)  #### Number of days

#### Create the problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

#### Decision Variables
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", ((n, i) for n in range(N) for i in range(total_number)), cat='Binary')

#### Objective Function
problem += total_number, "Minimize_Total_Employees"

#### Constraints
#### Ensure that the number of employees working meets the requirement for each day
for n in range(N):
    problem += pulp.lpSum(is_work[(n, i)] for i in range(total_number)) >= num_n[n], f"Minimum_Employees_Day_{n}"

#### Define the working and resting schedule for each employee
for i in range(total_number):
    for n in range(N):
        if n - (n_working_days + n_resting_days) >= 0:  #### Check for bounds
            problem += is_work[(n, i)] <= pulp.lpSum(is_work[(n - j, i)] for j in range(n_working_days + n_resting_days)), f"Work_Rest_Schedule_{i}_{n}"

#### Solve the problem
problem.solve()

#### Output
total_employees = pulp.value(total_number)
is_work_matrix = np.array([[pulp.value(is_work[(n, i)]) for i in range(int(total_employees))] for n in range(N)])

print(f'Total Employees Hired: {total_employees}')
print('Work Schedule Matrix:')
print(is_work_matrix)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

