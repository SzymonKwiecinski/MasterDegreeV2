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

\section*{Linear Programming Model for Maximizing Profit in Spare Parts Production}

\subsection*{Variables}
Let:
\begin{itemize}
    \item \( K \) be the number of spare parts.
    \item \( S \) be the number of shops.
    \item \( quantity_k \) be the quantity of spare part \( k \) produced.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( time_{k,s} \): required worker-hours for part \( k \) in shop \( s \).
    \item \( profit_k \): profit from part \( k \).
    \item \( capacity_s \): working hours available in shop \( s \).
\end{itemize}

\subsection*{Objective Function}
We want to maximize the total profit, which is given by:
\[
\text{Maximize } Z = \sum_{k=1}^{K} profit_k \cdot quantity_k
\]

\subsection*{Constraints}
The production of spare parts is limited by the capacity of each shop. Thus, the following constraints must hold for each shop \( s \):
\[
\sum_{k=1}^{K} time_{k,s} \cdot quantity_k \leq capacity_s \quad \text{for } s = 1, \ldots, S
\]

Additionally, the quantity of each spare part must be non-negative:
\[
quantity_k \geq 0 \quad \text{for } k = 1, \ldots, K
\]

\subsection*{Summary of the Model}
The linear programming model can be summarized as follows:

\begin{align*}
\text{Maximize } & Z = \sum_{k=1}^{K} profit_k \cdot quantity_k \\
\text{subject to } & \sum_{k=1}^{K} time_{k,s} \cdot quantity_k \leq capacity_s, \quad s = 1, \ldots, S \\
& quantity_k \geq 0, \quad k = 1, \ldots, K
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

\section*{Linear Programming Model for Maximizing Profit in Spare Parts Production}

\subsection*{Variables}
Let:
\begin{itemize}
    \item \( K \) be the number of spare parts.
    \item \( S \) be the number of shops.
    \item \( quantity_k \) be the quantity of spare part \( k \) produced.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( time_{k,s} \): required worker-hours for part \( k \) in shop \( s \).
    \item \( profit_k \): profit from part \( k \).
    \item \( capacity_s \): working hours available in shop \( s \).
\end{itemize}

\subsection*{Objective Function}
We want to maximize the total profit, which is given by:
\[
\text{Maximize } Z = \sum_{k=1}^{K} profit_k \cdot quantity_k
\]

\subsection*{Constraints}
The production of spare parts is limited by the capacity of each shop. Thus, the following constraints must hold for each shop \( s \):
\[
\sum_{k=1}^{K} time_{k,s} \cdot quantity_k \leq capacity_s \quad \text{for } s = 1, \ldots, S
\]

Additionally, the quantity of each spare part must be non-negative:
\[
quantity_k \geq 0 \quad \text{for } k = 1, \ldots, K
\]

\subsection*{Summary of the Model}
The linear programming model can be summarized as follows:

\begin{align*}
\text{Maximize } & Z = \sum_{k=1}^{K} profit_k \cdot quantity_k \\
\text{subject to } & \sum_{k=1}^{K} time_{k,s} \cdot quantity_k \leq capacity_s, \quad s = 1, \ldots, S \\
& quantity_k \geq 0, \quad k = 1, \ldots, K
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = '{"NumParts": 5, "NumMachines": 2, "Time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], "Profit": [30, 20, 40, 25, 10], "Capacity": [700, 1000]}'
data = json.loads(data)

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Define the number of spare parts and shops
num_parts = data['NumParts']
num_machines = data['NumMachines']

#### Create decision variables for quantity of each spare part produced
quantity = pulp.LpVariable.dicts("Quantity", range(num_parts), lowBound=0)

#### Define the objective function
problem += pulp.lpSum(data['Profit'][k] * quantity[k] for k in range(num_parts)), "Total_Profit"

#### Define the constraints based on shop capacities
for s in range(num_machines):
    problem += pulp.lpSum(data['Time'][k][s] * quantity[k] for k in range(num_parts)) <= data['Capacity'][s], f"Capacity_Constraint_{s}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

