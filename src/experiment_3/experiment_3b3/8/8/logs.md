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

Let \( K \) be the number of spare parts and \( S \) be the number of shops. We define:

\begin{itemize}
    \item \( \text{time}_{k,s} \): the required worker-hours for part \( k \) in shop \( s \).
    \item \( \text{profit}_{k} \): the profit from part \( k \).
    \item \( \text{capacity}_{s} \): the capacity of shop \( s \) in working hours.
    \item \( \text{quantity}_{k} \): the quantity of part \( k \) to be produced.
\end{itemize}

The objective is to maximize the total profit from producing the parts:

\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot \text{quantity}_{k}
\]

Subject to the constraints imposed by the shop capacity:

\[
\sum_{k=1}^{K} \text{time}_{k,s} \cdot \text{quantity}_{k} \leq \text{capacity}_{s}, \quad \forall s = 1,\ldots,S
\]

And the non-negativity constraints:

\[
\text{quantity}_{k} \geq 0, \quad \forall k = 1,\ldots,K
\]

Thus, the complete Linear Programming model can be summarized as:

\[
\begin{aligned}
    \text{Maximize} \quad & Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot \text{quantity}_{k} \\
    \text{subject to} \quad & \sum_{k=1}^{K} \text{time}_{k,s} \cdot \text{quantity}_{k} \leq \text{capacity}_{s} \quad \forall s = 1,\ldots,S \\
    & \text{quantity}_{k} \geq 0 \quad \forall k = 1,\ldots,K
\end{aligned}
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

Let \( K \) be the number of spare parts and \( S \) be the number of shops. We define:

\begin{itemize}
    \item \( \text{time}_{k,s} \): the required worker-hours for part \( k \) in shop \( s \).
    \item \( \text{profit}_{k} \): the profit from part \( k \).
    \item \( \text{capacity}_{s} \): the capacity of shop \( s \) in working hours.
    \item \( \text{quantity}_{k} \): the quantity of part \( k \) to be produced.
\end{itemize}

The objective is to maximize the total profit from producing the parts:

\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot \text{quantity}_{k}
\]

Subject to the constraints imposed by the shop capacity:

\[
\sum_{k=1}^{K} \text{time}_{k,s} \cdot \text{quantity}_{k} \leq \text{capacity}_{s}, \quad \forall s = 1,\ldots,S
\]

And the non-negativity constraints:

\[
\text{quantity}_{k} \geq 0, \quad \forall k = 1,\ldots,K
\]

Thus, the complete Linear Programming model can be summarized as:

\[
\begin{aligned}
    \text{Maximize} \quad & Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot \text{quantity}_{k} \\
    \text{subject to} \quad & \sum_{k=1}^{K} \text{time}_{k,s} \cdot \text{quantity}_{k} \leq \text{capacity}_{s} \quad \forall s = 1,\ldots,S \\
    & \text{quantity}_{k} \geq 0 \quad \forall k = 1,\ldots,K
\end{aligned}
\]

\end{document}</MATH_MODEL>
<DATA>
{'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Extract data from JSON
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

num_parts = data['NumParts']
num_shops = data['NumMachines']
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']

#### Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Define decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(num_parts)]

#### Objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(num_parts)), "Total_Profit"

#### Constraints for shop capacities
for s in range(num_shops):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(num_parts)) <= capacity[s], f"Capacity_Constraint_Shop_{s}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

