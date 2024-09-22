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

\section*{Linear Programming Model for Maximizing Profit in Spare Part Production}

\subsection*{Indices}
\begin{itemize}
    \item \( k \): Index for spare parts (\( k = 1, \ldots, K \))
    \item \( s \): Index for shops (\( s = 1, \ldots, S \))
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{time}_{k,s} \): Required worker-hours for part \( k \) in shop \( s \)
    \item \( \text{profit}_{k} \): Profit from part \( k \)
    \item \( \text{capacity}_{s} \): Capacity of shop \( s \) in working hours
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{quantity}_{k} \): Amount of spare part \( k \) to be made
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot \text{quantity}_{k}
\]

\subsection*{Constraints}
\begin{itemize}
    \item Capacity constraints for each shop:
\end{itemize}
\[
\sum_{k=1}^{K} \text{time}_{k,s} \cdot \text{quantity}_{k} \leq \text{capacity}_{s}, \quad \forall s \in \{1, \ldots, S\}
\]
\begin{itemize}
    \item Non-negativity constraints:
\end{itemize}
\[
\text{quantity}_{k} \geq 0, \quad \forall k \in \{1, \ldots, K\}
\]

\subsection*{Output}
The solution will provide the optimal quantities of each spare part to be produced:
\[
\text{quantity} = [\text{quantity}_{1}, \text{quantity}_{2}, \ldots, \text{quantity}_{K}]
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

\section*{Linear Programming Model for Maximizing Profit in Spare Part Production}

\subsection*{Indices}
\begin{itemize}
    \item \( k \): Index for spare parts (\( k = 1, \ldots, K \))
    \item \( s \): Index for shops (\( s = 1, \ldots, S \))
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{time}_{k,s} \): Required worker-hours for part \( k \) in shop \( s \)
    \item \( \text{profit}_{k} \): Profit from part \( k \)
    \item \( \text{capacity}_{s} \): Capacity of shop \( s \) in working hours
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{quantity}_{k} \): Amount of spare part \( k \) to be made
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot \text{quantity}_{k}
\]

\subsection*{Constraints}
\begin{itemize}
    \item Capacity constraints for each shop:
\end{itemize}
\[
\sum_{k=1}^{K} \text{time}_{k,s} \cdot \text{quantity}_{k} \leq \text{capacity}_{s}, \quad \forall s \in \{1, \ldots, S\}
\]
\begin{itemize}
    \item Non-negativity constraints:
\end{itemize}
\[
\text{quantity}_{k} \geq 0, \quad \forall k \in \{1, \ldots, K\}
\]

\subsection*{Output}
The solution will provide the optimal quantities of each spare part to be produced:
\[
\text{quantity} = [\text{quantity}_{1}, \text{quantity}_{2}, \ldots, \text{quantity}_{K}]
\]

\end{document}</MATH_MODEL>
<DATA>
{'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = {'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 
        'profit': [30, 20, 40, 25, 10], 
        'capacity': [700, 1000]}

#### Extract data
time = data['time']
profit = data['profit']
capacity = data['capacity']

K = len(profit)  #### Number of spare parts
S = len(capacity)  #### Number of shops

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

#### Objective Function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

#### Capacity Constraints
for s in range(S):
    problem += (pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s]), f"Capacity_Constraint_{s + 1}"

#### Solve the problem
problem.solve()

#### Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
for k in range(K):
    print(f'Spare part {k + 1}: {quantity[k].varValue}')
```

