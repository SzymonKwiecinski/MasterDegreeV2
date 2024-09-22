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

\title{Linear Programming Model for Spare Automobile Parts Production}
\author{}
\date{}
\maketitle

\section*{Problem Statement}
A small firm specializes in making some types of spare automobile parts. Each part must go through several shops, and we want to determine the quantities of each spare part to maximize the profit.

\section*{Variables}
Let:
\begin{itemize}
    \item \( K \): Number of different spare parts.
    \item \( S \): Number of different shops.
    \item \( x_k \): Quantity of part \( k \) to be produced, for \( k = 1, \ldots, K \).
\end{itemize}

\section*{Parameters}
Given:
\begin{itemize}
    \item \( time_{k,s} \): Required worker-hours for part \( k \) in shop \( s \).
    \item \( profit_k \): Profit for part \( k \).
    \item \( capacity_s \): Capacity of shop \( s \) in working hours.
\end{itemize}

\section*{Objective Function}
The objective is to maximize the total profit, which can be expressed as:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} profit_k \cdot x_k
\]

\section*{Constraints}
The constraints ensure that the total worker-hours used in each shop does not exceed its capacity. For each shop \( s \), the constraint is given by:
\[
\sum_{k=1}^{K} time_{k,s} \cdot x_k \leq capacity_s \quad \forall s = 1, \ldots, S
\]

Additionally, we have non-negativity constraints for all parts produced:
\[
x_k \geq 0 \quad \forall k = 1, \ldots, K
\]

\section*{Complete Formulation}
Putting it all together, the linear programming model can be formulated as follows:

\begin{align*}
\text{Maximize} & \quad Z = \sum_{k=1}^{K} profit_k \cdot x_k \\
\text{subject to} & \quad \sum_{k=1}^{K} time_{k,s} \cdot x_k \leq capacity_s \quad \forall s = 1, \ldots, S \\
& \quad x_k \geq 0 \quad \forall k = 1, \ldots, K
\end{align*}

\section*{Output}
The output of this model will be the quantities of each spare part to be made:
\[
\text{Output: } \{ "quantity": [x_k \text{ for } k = 1, \ldots, K] \}
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

\title{Linear Programming Model for Spare Automobile Parts Production}
\author{}
\date{}
\maketitle

\section*{Problem Statement}
A small firm specializes in making some types of spare automobile parts. Each part must go through several shops, and we want to determine the quantities of each spare part to maximize the profit.

\section*{Variables}
Let:
\begin{itemize}
    \item \( K \): Number of different spare parts.
    \item \( S \): Number of different shops.
    \item \( x_k \): Quantity of part \( k \) to be produced, for \( k = 1, \ldots, K \).
\end{itemize}

\section*{Parameters}
Given:
\begin{itemize}
    \item \( time_{k,s} \): Required worker-hours for part \( k \) in shop \( s \).
    \item \( profit_k \): Profit for part \( k \).
    \item \( capacity_s \): Capacity of shop \( s \) in working hours.
\end{itemize}

\section*{Objective Function}
The objective is to maximize the total profit, which can be expressed as:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} profit_k \cdot x_k
\]

\section*{Constraints}
The constraints ensure that the total worker-hours used in each shop does not exceed its capacity. For each shop \( s \), the constraint is given by:
\[
\sum_{k=1}^{K} time_{k,s} \cdot x_k \leq capacity_s \quad \forall s = 1, \ldots, S
\]

Additionally, we have non-negativity constraints for all parts produced:
\[
x_k \geq 0 \quad \forall k = 1, \ldots, K
\]

\section*{Complete Formulation}
Putting it all together, the linear programming model can be formulated as follows:

\begin{align*}
\text{Maximize} & \quad Z = \sum_{k=1}^{K} profit_k \cdot x_k \\
\text{subject to} & \quad \sum_{k=1}^{K} time_{k,s} \cdot x_k \leq capacity_s \quad \forall s = 1, \ldots, S \\
& \quad x_k \geq 0 \quad \forall k = 1, \ldots, K
\end{align*}

\section*{Output}
The output of this model will be the quantities of each spare part to be made:
\[
\text{Output: } \{ "quantity": [x_k \text{ for } k = 1, \ldots, K] \}
\]

\end{document}</MATH_MODEL>
<DATA>
{'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data in JSON format
data = {'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 
        'profit': [30, 20, 40, 25, 10], 
        'capacity': [700, 1000]}

#### Extracting data
time = data['time']
profit = data['profit']
capacity = data['capacity']

#### Defining the problem
K = len(profit)  #### Number of spare parts
S = len(capacity)  #### Number of shops
problem = pulp.LpProblem("Spare_Parts_Production", pulp.LpMaximize)

#### Defining decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K)), "Total_Profit"

#### Constraints for each shop
for s in range(S):
    problem += (pulp.lpSum(time[k][s] * x[k] for k in range(K)) <= capacity[s]), f"Shop_Capacity_{s}"

#### Solve the problem
problem.solve()

#### Output the results
quantities = [x[k].varValue for k in range(K)]
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Output: {{"quantity": {quantities}}}')
```

