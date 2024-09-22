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

\section*{Linear Programming Formulation}

\textbf{Objective:} Maximize the total profit from producing spare parts.

Let:
\begin{itemize}
    \item \( K \) = number of different spare parts
    \item \( S \) = number of shops
    \item \( \text{time}_{k,s} \) = worker-hours required for part \( k \) in shop \( s \)
    \item \( \text{profit}_k \) = profit from part \( k \)
    \item \( \text{capacity}_s \) = capacity of shop \( s \) in working hours
    \item \( q_k \) = quantity of part \( k \) to be produced
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_k \cdot q_k
\]

\textbf{Subject to:}
For each shop \( s \):
\[
\sum_{k=1}^{K} \text{time}_{k,s} \cdot q_k \leq \text{capacity}_s \quad \forall s = 1, 2, \ldots, S
\]

\textbf{Non-negativity Constraints:}
\[
q_k \geq 0 \quad \forall k = 1, 2, \ldots, K
\]

The output format for the quantities of each spare part to be produced is:
\[
\text{quantity} = [q_k \text{ for } k = 1, \ldots, K]
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

\section*{Linear Programming Formulation}

\textbf{Objective:} Maximize the total profit from producing spare parts.

Let:
\begin{itemize}
    \item \( K \) = number of different spare parts
    \item \( S \) = number of shops
    \item \( \text{time}_{k,s} \) = worker-hours required for part \( k \) in shop \( s \)
    \item \( \text{profit}_k \) = profit from part \( k \)
    \item \( \text{capacity}_s \) = capacity of shop \( s \) in working hours
    \item \( q_k \) = quantity of part \( k \) to be produced
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_k \cdot q_k
\]

\textbf{Subject to:}
For each shop \( s \):
\[
\sum_{k=1}^{K} \text{time}_{k,s} \cdot q_k \leq \text{capacity}_s \quad \forall s = 1, 2, \ldots, S
\]

\textbf{Non-negativity Constraints:}
\[
q_k \geq 0 \quad \forall k = 1, 2, \ldots, K
\]

The output format for the quantities of each spare part to be produced is:
\[
\text{quantity} = [q_k \text{ for } k = 1, \ldots, K]
\]

\end{document}</MATH_MODEL>
<DATA>
{'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON format
data = {'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}

#### Extracting data
time = data['time']
profit = data['profit']
capacity = data['capacity']
K = len(profit)
S = len(capacity)

#### Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
q = [pulp.LpVariable(f'q_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective function
problem += pulp.lpSum(profit[k] * q[k] for k in range(K)), "Total Profit"

#### Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * q[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_{s}"

#### Solve the problem
problem.solve()

#### Output the quantities of each spare part to be produced
quantity = [pulp.value(q[k]) for k in range(K)]
print(f'Quantity of each spare part to be produced: {quantity}')

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

