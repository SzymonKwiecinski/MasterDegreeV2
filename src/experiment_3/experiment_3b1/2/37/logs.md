# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- A small firm specializes in making some types of spare automobile parts. 
- Each part is has to go through several shops 
- The required worker-hours for part \var{k} in shop \var{s} is \var{time_{k, s}}.
- The profit of part \var{k} is \var{profit_{k}}.
- The capacity of shop \var{s} is \var{capacity_{s}} working hours.

INPUT FORMAT:

{
	"time": [[time_{k, s} for s in 1,...,S] for k in 1,...,K],
	"profit": [profit_{k} for k in 1,...,K],
	"capacity": [capacity_{s} for s in 1,...,S]
}


OBJECTIVE: Formulate the problem of determining the quantities of each spare part to be made during the month so as to maximize profit.

OUTPUT INFO:

- \var{quantity} represents the amount of each spare part to be made

OUTPUT FORMAT:

{
	"quantity": [quantity_{k} for k in 1,...,K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Spare Automobile Parts Production}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( x_k \) be the quantity of spare part \( k \) produced, where \( k = 1, 2, \ldots, K \).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( time_{k, s} \): Required worker-hours for part \( k \) in shop \( s \).
    \item \( profit_k \): Profit of part \( k \).
    \item \( capacity_s \): Capacity of shop \( s \) in working hours.
\end{itemize}

\textbf{Objective Function:}
Maximize total profit:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} profit_k \cdot x_k
\]

\textbf{Constraints:}
\begin{itemize}
    \item For each shop \( s \), the total worker-hours used cannot exceed the shop's capacity:
    \[
    \sum_{k=1}^{K} time_{k, s} \cdot x_k \leq capacity_s \quad \text{for } s = 1, 2, \ldots, S
    \]
    \item Non-negativity constraints:
    \[
    x_k \geq 0 \quad \text{for } k = 1, 2, \ldots, K
    \]
\end{itemize}

\textbf{Output:}
The optimal quantities of each spare part to be made are represented as:
\[
\text{quantity} = [x_k \text{ for } k = 1, \ldots, K]
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

\section*{Linear Programming Model for Spare Automobile Parts Production}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( x_k \) be the quantity of spare part \( k \) produced, where \( k = 1, 2, \ldots, K \).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( time_{k, s} \): Required worker-hours for part \( k \) in shop \( s \).
    \item \( profit_k \): Profit of part \( k \).
    \item \( capacity_s \): Capacity of shop \( s \) in working hours.
\end{itemize}

\textbf{Objective Function:}
Maximize total profit:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} profit_k \cdot x_k
\]

\textbf{Constraints:}
\begin{itemize}
    \item For each shop \( s \), the total worker-hours used cannot exceed the shop's capacity:
    \[
    \sum_{k=1}^{K} time_{k, s} \cdot x_k \leq capacity_s \quad \text{for } s = 1, 2, \ldots, S
    \]
    \item Non-negativity constraints:
    \[
    x_k \geq 0 \quad \text{for } k = 1, 2, \ldots, K
    \]
\end{itemize}

\textbf{Output:}
The optimal quantities of each spare part to be made are represented as:
\[
\text{quantity} = [x_k \text{ for } k = 1, \ldots, K]
\]

\end{document}</MATH_MODEL>
<DATA>
{'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from JSON format
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

#### Number of parts and shops
K = len(data['profit'])
S = len(data['capacity'])

#### Create the problem instance
problem = pulp.LpProblem("Spare_Parts_Production", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{k+1}', lowBound=0) for k in range(K)]

#### Objective Function
problem += pulp.lpSum(data['profit'][k] * x[k] for k in range(K)), "Total_Profit"

#### Constraints
for s in range(S):
    problem += pulp.lpSum(data['time'][k][s] * x[k] for k in range(K)) <= data['capacity'][s], f"Capacity_Constraint_{s+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

