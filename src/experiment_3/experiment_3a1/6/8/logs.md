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

Let \( K \) be the number of different spare parts and \( S \) be the number of shops. 

Define the following variables:

\begin{itemize}
    \item \( x_k \): quantity of spare part \( k \) produced, for \( k = 1, 2, \ldots, K \).
\end{itemize}

The objective is to maximize the total profit:

\[
\text{Maximize } Z = \sum_{k=1}^{K} profit_k \cdot x_k
\]

Subject to the constraints imposed by the capacity of each shop. For each shop \( s \):

\[
\sum_{k=1}^{K} time_{k,s} \cdot x_k \leq capacity_s \quad \text{for all } s = 1, 2, \ldots, S
\]

Additionally, we need to ensure non-negativity of the variables:

\[
x_k \geq 0 \quad \text{for all } k = 1, 2, \ldots, K
\]

In summary, the linear programming model can be stated as follows:

\begin{align*}
\text{Maximize} \quad & Z = \sum_{k=1}^{K} profit_k \cdot x_k \\
\text{Subject to} \quad & \sum_{k=1}^{K} time_{k,s} \cdot x_k \leq capacity_s, \quad s = 1, 2, \ldots, S \\
& x_k \geq 0, \quad k = 1, 2, \ldots, K
\end{align*}

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

Let \( K \) be the number of different spare parts and \( S \) be the number of shops. 

Define the following variables:

\begin{itemize}
    \item \( x_k \): quantity of spare part \( k \) produced, for \( k = 1, 2, \ldots, K \).
\end{itemize}

The objective is to maximize the total profit:

\[
\text{Maximize } Z = \sum_{k=1}^{K} profit_k \cdot x_k
\]

Subject to the constraints imposed by the capacity of each shop. For each shop \( s \):

\[
\sum_{k=1}^{K} time_{k,s} \cdot x_k \leq capacity_s \quad \text{for all } s = 1, 2, \ldots, S
\]

Additionally, we need to ensure non-negativity of the variables:

\[
x_k \geq 0 \quad \text{for all } k = 1, 2, \ldots, K
\]

In summary, the linear programming model can be stated as follows:

\begin{align*}
\text{Maximize} \quad & Z = \sum_{k=1}^{K} profit_k \cdot x_k \\
\text{Subject to} \quad & \sum_{k=1}^{K} time_{k,s} \cdot x_k \leq capacity_s, \quad s = 1, 2, \ldots, S \\
& x_k \geq 0, \quad k = 1, 2, \ldots, K
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data
data = json.loads('{"NumParts": 5, "NumMachines": 2, "Time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], "Profit": [30, 20, 40, 25, 10], "Capacity": [700, 1000]}')

#### Parameters
K = data['NumParts']  #### Number of different spare parts
S = data['NumMachines']  #### Number of shops
time = data['Time']  #### Production times for each spare part in each shop
profit = data['Profit']  #### Profit for each spare part
capacity = data['Capacity']  #### Capacity of each shop

#### Create a problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  #### Quantity of spare part k produced

#### Objective function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K)), "Total_Profit"

#### Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * x[k] for k in range(K)) <= capacity[s], f"Shop_Capacity_{s}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

