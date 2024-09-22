# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MILP

PROBLEM INFO: 
- A hospital wants to make a weekly night shift (12pm-8am) schedule for its nurses. 
- The demand for nurses for the night shift on day \var{j} = 1,...,7 is an integer \var{d_j}. 
- Every nurse works \var{period} days in a row on the night shift, followed by (7 - \var{period}) days off.


INPUT FORMAT: 

{
    "period": period,
    "demand": [d_j for j in 1, ...,7]
}

OBJECTIVE: The goal is to find the minimal number of nurses the hospital needs to hire. 

OUTPUT INFO: 

- for each day \var{j} = 1,...,7, \var{start_j} which shows the number of nurses that start their period on day \var{j}.
- the total number of nurses hired.

OUTPUT FORMAT:

{
    "start": [start_j for j in 1, ...,7],
    "total": total
}


</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{MILP Model for Nurse Scheduling}
\author{}
\date{}
\maketitle

\section{Problem Definition}
A hospital needs to create a weekly night shift schedule for nurses. The demand for nurses for the night shift on day \( j \) (where \( j = 1, \ldots, 7 \)) is given as an integer \( d_j \). Each nurse works for \( \text{period} \) days in a row and then has \( 7 - \text{period} \) days off.

\section{Variables}
Let:
\begin{itemize}
    \item \( x_j \): Number of nurses that start their period on day \( j \) for \( j = 1, \ldots, 7 \).
    \item \( N \): Total number of nurses hired.
\end{itemize}

\section{Objective Function}
Minimize the total number of nurses hired:
\[
\text{Minimize } N = \sum_{j=1}^{7} x_j
\]

\section{Constraints}
For each day \( j \), the total number of nurses available must meet or exceed the demand:
\[
\sum_{k=0}^{\text{period}-1} x_{(j-k \mod 7)} \geq d_j \quad \forall j = 1, \ldots, 7
\]

\section{Input Format}
The model requires the following inputs:
\begin{itemize}
    \item \( \text{period} \): Number of consecutive days a nurse works.
    \item \( d_j \): Array of integer demands for each day \( j \).
\end{itemize}

\section{Output Format}
The output should provide:
\begin{itemize}
    \item \( \text{start} \): Array containing \( x_j \) for \( j = 1, \ldots, 7 \).
    \item \( \text{total} \): Total number of nurses hired, \( N \).
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

\title{MILP Model for Nurse Scheduling}
\author{}
\date{}
\maketitle

\section{Problem Definition}
A hospital needs to create a weekly night shift schedule for nurses. The demand for nurses for the night shift on day \( j \) (where \( j = 1, \ldots, 7 \)) is given as an integer \( d_j \). Each nurse works for \( \text{period} \) days in a row and then has \( 7 - \text{period} \) days off.

\section{Variables}
Let:
\begin{itemize}
    \item \( x_j \): Number of nurses that start their period on day \( j \) for \( j = 1, \ldots, 7 \).
    \item \( N \): Total number of nurses hired.
\end{itemize}

\section{Objective Function}
Minimize the total number of nurses hired:
\[
\text{Minimize } N = \sum_{j=1}^{7} x_j
\]

\section{Constraints}
For each day \( j \), the total number of nurses available must meet or exceed the demand:
\[
\sum_{k=0}^{\text{period}-1} x_{(j-k \mod 7)} \geq d_j \quad \forall j = 1, \ldots, 7
\]

\section{Input Format}
The model requires the following inputs:
\begin{itemize}
    \item \( \text{period} \): Number of consecutive days a nurse works.
    \item \( d_j \): Array of integer demands for each day \( j \).
\end{itemize}

\section{Output Format}
The output should provide:
\begin{itemize}
    \item \( \text{start} \): Array containing \( x_j \) for \( j = 1, \ldots, 7 \).
    \item \( \text{total} \): Total number of nurses hired, \( N \).
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON format
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}

#### Extract data
T = data['T']
period = data['Period']
demand = data['Demand']

#### Define the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(T), lowBound=0, cat='Integer')

#### Objective function
problem += pulp.lpSum([x[j] for j in range(T)])

#### Constraints
for j in range(T):
    problem += pulp.lpSum([x[(j-k) % T] for k in range(period)]) >= demand[j]

#### Solve the problem
problem.solve(pulp.PULP_CBC_CMD(msg=0))

#### Fetch results
start = [pulp.value(x[j]) for j in range(T)]
total = pulp.value(problem.objective)

#### Print the results
print(f"(Start): {start}")
print(f"(Total Nurses): {total}")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

