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

\subsection*{Indices}
\begin{itemize}
    \item \( n \): Day index, where \( n = 1, 2, \ldots, N \)
    \item \( i \): Employee index, where \( i = 1, 2, \ldots, \text{total\_number} \)
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{num}_n \): Number of desired employees on day \( n \)
    \item \( n_{\text{working}} \): Number of consecutive working days for each employee
    \item \( n_{\text{resting}} \): Number of consecutive resting days for each employee
    \item \( T = n_{\text{working}} + n_{\text{resting}} \): Total cycle length of work and rest
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_i \in \{0, 1\} \): 1 if employee \( i \) is working on day \( n \), 0 otherwise
\end{itemize}

\subsection*{Objective Function}
Minimize the total number of employees:
\[
\text{Minimize } \text{total\_number} = \sum_{i=1}^{\text{total\_number}} 1
\]

\subsection*{Constraints}
1. Each day's required staff must be met:
\[
\sum_{i=1}^{\text{total\_number}} x_i \geq \text{num}_n \quad \forall n = 1, \ldots, N
\]

2. Employee work/rest cycles:
\[
\text{For each employee } i, \text{ define the working days according to the cycle:}
\]
\[
x_{i, n} = 
\begin{cases} 
1 & \text{if employee } i \text{ works on day } n \\
0 & \text{if employee } i \text{ is resting on day } n 
\end{cases}
\]
Where:
\[
x_{i, n} = x_{i, n-1} \text{ for } n \in [k \cdot T + 1, k \cdot T + n_{\text{working}}] \text{ (for all } k \text{ being integers)}
\]
\[
x_{i, n} = 0 \text{ for } n \in [k \cdot T + n_{\text{working}} + 1, (k+1) \cdot T] 
\]

\subsection*{Output Variables}
- \( \text{total\_number} \): Total number of employees to employ
- \( \text{is\_work}_{n, i} \): A binary matrix indicating whether employee \( i \) is working on day \( n \)

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

\subsection*{Indices}
\begin{itemize}
    \item \( n \): Day index, where \( n = 1, 2, \ldots, N \)
    \item \( i \): Employee index, where \( i = 1, 2, \ldots, \text{total\_number} \)
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{num}_n \): Number of desired employees on day \( n \)
    \item \( n_{\text{working}} \): Number of consecutive working days for each employee
    \item \( n_{\text{resting}} \): Number of consecutive resting days for each employee
    \item \( T = n_{\text{working}} + n_{\text{resting}} \): Total cycle length of work and rest
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_i \in \{0, 1\} \): 1 if employee \( i \) is working on day \( n \), 0 otherwise
\end{itemize}

\subsection*{Objective Function}
Minimize the total number of employees:
\[
\text{Minimize } \text{total\_number} = \sum_{i=1}^{\text{total\_number}} 1
\]

\subsection*{Constraints}
1. Each day's required staff must be met:
\[
\sum_{i=1}^{\text{total\_number}} x_i \geq \text{num}_n \quad \forall n = 1, \ldots, N
\]

2. Employee work/rest cycles:
\[
\text{For each employee } i, \text{ define the working days according to the cycle:}
\]
\[
x_{i, n} = 
\begin{cases} 
1 & \text{if employee } i \text{ works on day } n \\
0 & \text{if employee } i \text{ is resting on day } n 
\end{cases}
\]
Where:
\[
x_{i, n} = x_{i, n-1} \text{ for } n \in [k \cdot T + 1, k \cdot T + n_{\text{working}}] \text{ (for all } k \text{ being integers)}
\]
\[
x_{i, n} = 0 \text{ for } n \in [k \cdot T + n_{\text{working}} + 1, (k+1) \cdot T] 
\]

\subsection*{Output Variables}
- \( \text{total\_number} \): Total number of employees to employ
- \( \text{is\_work}_{n, i} \): A binary matrix indicating whether employee \( i \) is working on day \( n \)

\end{document}</MATH_MODEL>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load the data
data = json.loads('{"num": [5, 10, 2, 3, 2, 10], "n_working_days": 5, "n_resting_days": 2}')
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)
total_number = len(num)  #### One employee per day for simplicity

T = n_working_days + n_resting_days

#### Create the problem
problem = pulp.LpProblem("Cafeteria_Staff_Scheduling", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("work", (range(total_number), range(N)), cat='Binary')

#### Objective function
problem += pulp.lpSum([1 for i in range(total_number)])

#### Constraints for required staff per day
for n in range(N):
    problem += pulp.lpSum([x[i][n] for i in range(total_number)]) >= num[n], f"StaffRequirement_day_{n+1}"

#### Constraints for employee work/rest cycles
for i in range(total_number):
    for k in range((N // T) + 1):  #### Integer k for T cycles
        #### Working days
        for n in range(k * T + 1, k * T + n_working_days + 1):
            if n < N:  #### Ensure n does not exceed the number of days
                problem += x[i][n] == 1
        #### Rest days
        for n in range(k * T + n_working_days + 1, (k + 1) * T + 1):
            if n < N:  #### Ensure n does not exceed the number of days
                problem += x[i][n] == 0

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

