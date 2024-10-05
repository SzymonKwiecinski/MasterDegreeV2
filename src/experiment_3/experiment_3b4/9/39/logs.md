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
To formulate this problem as a Linear Programming problem, we can define the decision variables, constraints, and the objective function in detail. We'll use binary decision variables to represent whether an employee is working or resting on a given day.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{LP Model for Cafeteria Employee Scheduling}

Given the input parameters:
\begin{itemize}
    \item \( \text{num}[n] \) for \( n = 1, \ldots, N \), representing the required number of employees on day \( n \).
    \item \( n_{\text{working\_days}} \) represents the number of consecutive working days.
    \item \( n_{\text{resting\_days}} \) represents the number of consecutive rest days.
\end{itemize}

We define:
\begin{align*}
    & \text{Decision Variables:} \\
    & x_{i,n} = 
    \begin{cases} 
    1, & \text{if employee } i \text{ works on day } n \\
    0, & \text{otherwise}
    \end{cases} \\
    & \text{for } i = 1, \ldots, \text{total\_number} \text{ and } n = 1, \ldots, N.
\end{align*}

\subsection*{Objective Function}

Minimize the total number of employees:
\[
\min \text{total\_number}
\]

\subsection*{Constraints}

\begin{enumerate}
    \item Ensure enough employees each day:
    \[
    \sum_{i=1}^{\text{total\_number}} x_{i,n} \geq \text{num}[n] \quad \forall n = 1, \ldots, N
    \]
    
    \item Working and resting schedule constraints:
    \begin{align*}
    & \text{For each } i, \text{ if } x_{i,n} = 1 \text{ for } n = k, k+1, \ldots, k + n_{\text{working\_days}} - 1, \text{ then } \\
    & x_{i,n'} = 0 \text{ for } n' = k + n_{\text{working\_days}}, \ldots, k + n_{\text{working\_days}} + n_{\text{resting\_days}} - 1
    \end{align*}

    \item Binary constraints for decision variables:
    \[
    x_{i,n} \in \{0, 1\} \quad \forall i, \forall n
    \]
\end{enumerate}

\subsection*{Summary}

The above model calculates the minimum number of employees (total\_number) and assigns a working/resting schedule (is\_work) such that the required number of employees is available each day while respecting the working and resting day rules.

\end{document}
```

The constraints ensure that each employee works exactly \( n_{\text{working\_days}} \) consecutive days followed by \( n_{\text{resting\_days}} \) consecutive days of rest, satisfying the daily demand `num`. The model aims to minimize the total number of employees required.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{LP Model for Cafeteria Employee Scheduling}

Given the input parameters:
\begin{itemize}
    \item \( \text{num}[n] \) for \( n = 1, \ldots, N \), representing the required number of employees on day \( n \).
    \item \( n_{\text{working\_days}} \) represents the number of consecutive working days.
    \item \( n_{\text{resting\_days}} \) represents the number of consecutive rest days.
\end{itemize}

We define:
\begin{align*}
    & \text{Decision Variables:} \\
    & x_{i,n} = 
    \begin{cases} 
    1, & \text{if employee } i \text{ works on day } n \\
    0, & \text{otherwise}
    \end{cases} \\
    & \text{for } i = 1, \ldots, \text{total\_number} \text{ and } n = 1, \ldots, N.
\end{align*}

\subsection*{Objective Function}

Minimize the total number of employees:
\[
\min \text{total\_number}
\]

\subsection*{Constraints}

\begin{enumerate}
    \item Ensure enough employees each day:
    \[
    \sum_{i=1}^{\text{total\_number}} x_{i,n} \geq \text{num}[n] \quad \forall n = 1, \ldots, N
    \]
    
    \item Working and resting schedule constraints:
    \begin{align*}
    & \text{For each } i, \text{ if } x_{i,n} = 1 \text{ for } n = k, k+1, \ldots, k + n_{\text{working\_days}} - 1, \text{ then } \\
    & x_{i,n'} = 0 \text{ for } n' = k + n_{\text{working\_days}}, \ldots, k + n_{\text{working\_days}} + n_{\text{resting\_days}} - 1
    \end{align*}

    \item Binary constraints for decision variables:
    \[
    x_{i,n} \in \{0, 1\} \quad \forall i, \forall n
    \]
\end{enumerate}

\subsection*{Summary}

The above model calculates the minimum number of employees (total\_number) and assigns a working/resting schedule (is\_work) such that the required number of employees is available each day while respecting the working and resting day rules.

\end{document}</MATH_MODEL>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Extract data
data = {
    'num': [5, 10, 2, 3, 2, 10],
    'n_working_days': 5,
    'n_resting_days': 2
}

num_days = len(data['num'])
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

#### Define the problem
problem = pulp.LpProblem("Cafeteria_Employee_Scheduling", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", ((i, n) for i in range(num_days) for n in range(num_days)),
                          cat='Binary')

#### Objective function: Minimize the total number of employees needed
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')
problem += total_number

#### Constraints
#### Ensure enough employees each day
for n in range(num_days):
    problem += pulp.lpSum(x[i, n] for i in range(num_days)) >= data['num'][n]

#### Working and resting schedule constraints
for i in range(num_days):
    for k in range(num_days - n_working_days - n_resting_days + 1):
        #### If working for n_working_days
        for n in range(k, k + n_working_days):
            if n < num_days:
                problem += x[i, n] == 1

        #### Then resting for n_resting_days
        for n_prime in range(k + n_working_days, k + n_working_days + n_resting_days):
            if n_prime < num_days:
                problem += x[i, n_prime] == 0

#### The total_number should be at least the maximum active employees any day
for n in range(num_days):
    problem += total_number >= pulp.lpSum(x[i, n] for i in range(num_days))

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


