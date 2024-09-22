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

\section*{Cafeteria Employee Scheduling Model}

\subsection*{Parameters}
Let:
\begin{itemize}
    \item \( num_n \): the number of desired employees on day \( n \) for \( n = 1, \ldots, N \)
    \item \( n_{\text{working}} \): the number of consecutive working days for each employee 
    \item \( n_{\text{resting}} \): the number of consecutive days off for each employee
\end{itemize}

\subsection*{Decision Variables}
Define \( x \): the total number of employees to hire, and let \( is\_work_{n,i} \) be a binary variable that indicates whether employee \( i \) is working on day \( n \):
\[
is\_work_{n,i} = 
\begin{cases} 
1 & \text{if employee } i \text{ is working on day } n \\
0 & \text{otherwise} 
\end{cases}
\]

\subsection*{Objective Function}
The objective is to minimize the total number of employees hired:
\[
\text{Minimize } x
\]

\subsection*{Constraints}
For each day \( n \) from \( 1 \) to \( N \), the following constraint ensures that the number of employees working on that day meets the required number:
\[
\sum_{i=1}^{x} is\_work_{n,i} \geq num_n \quad \forall n \in \{1, \ldots, N\}
\]

Additionally, to account for the working and resting days of each employee, we need to ensure that employees adhere to their schedule. For each employee \( i \):
\[
is\_work_{n,i} = 1 \quad \text{for } n \in \{j, j+1, \ldots, j+n_{\text{working}}-1\} \text{ and } 0 \text{ for } n \in \{j+n_{\text{working}}, j+n_{\text{working}}+1, \ldots, j+n_{\text{working}}+n_{\text{resting}}-1\}
\]
for suitable \( j \).

\subsection*{Output Variables}
The output variables will be:
\begin{itemize}
    \item \( total\_number = x \): the total number of employees hired.
    \item \( is\_work \): a matrix where \( is\_work[n][i] \) indicates whether employee \( i \) works on day \( n \).
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

\section*{Cafeteria Employee Scheduling Model}

\subsection*{Parameters}
Let:
\begin{itemize}
    \item \( num_n \): the number of desired employees on day \( n \) for \( n = 1, \ldots, N \)
    \item \( n_{\text{working}} \): the number of consecutive working days for each employee 
    \item \( n_{\text{resting}} \): the number of consecutive days off for each employee
\end{itemize}

\subsection*{Decision Variables}
Define \( x \): the total number of employees to hire, and let \( is\_work_{n,i} \) be a binary variable that indicates whether employee \( i \) is working on day \( n \):
\[
is\_work_{n,i} = 
\begin{cases} 
1 & \text{if employee } i \text{ is working on day } n \\
0 & \text{otherwise} 
\end{cases}
\]

\subsection*{Objective Function}
The objective is to minimize the total number of employees hired:
\[
\text{Minimize } x
\]

\subsection*{Constraints}
For each day \( n \) from \( 1 \) to \( N \), the following constraint ensures that the number of employees working on that day meets the required number:
\[
\sum_{i=1}^{x} is\_work_{n,i} \geq num_n \quad \forall n \in \{1, \ldots, N\}
\]

Additionally, to account for the working and resting days of each employee, we need to ensure that employees adhere to their schedule. For each employee \( i \):
\[
is\_work_{n,i} = 1 \quad \text{for } n \in \{j, j+1, \ldots, j+n_{\text{working}}-1\} \text{ and } 0 \text{ for } n \in \{j+n_{\text{working}}, j+n_{\text{working}}+1, \ldots, j+n_{\text{working}}+n_{\text{resting}}-1\}
\]
for suitable \( j \).

\subsection*{Output Variables}
The output variables will be:
\begin{itemize}
    \item \( total\_number = x \): the total number of employees hired.
    \item \( is\_work \): a matrix where \( is\_work[n][i] \) indicates whether employee \( i \) works on day \( n \).
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON format
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num_n = data['num']
n_working = data['n_working_days']
n_resting = data['n_resting_days']
N = len(num_n)

#### Create the problem
problem = pulp.LpProblem("Cafeteria_Employee_Scheduling", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable('x', lowBound=0, cat='Integer')  #### Total number of employees
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(100)), cat='Binary')  #### 100 is arbitrary for maximum employees

#### Objective function
problem += x, "Minimize_Employees"

#### Constraints for the required number of employees each day
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(100)) >= num_n[n], f"Employee_Requirement_Day_{n+1}"

#### Constraints for working/resting schedule
for i in range(100):
    for j in range(N - n_working - n_resting + 1):
        #### Working days
        for k in range(n_working):
            problem += is_work[j + k][i] == 1, f"Working_Days_Employee_{i+1}_Start_{j+1}"
        
        #### Resting days
        for k in range(n_resting):
            problem += is_work[j + n_working + k][i] == 0, f"Resting_Days_Employee_{i+1}_After_Work_{j+1}"

#### Solve the problem
problem.solve()

#### Output the results
total_number = int(pulp.value(x))
print(f'Total number of employees hired: {total_number}')

is_work_matrix = [[int(is_work[n][i].value()) for i in range(100)] for n in range(N)]
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

