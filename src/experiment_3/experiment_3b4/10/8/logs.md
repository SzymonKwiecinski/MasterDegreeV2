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
Based on the problem description, we need to formulate a Linear Programming model to maximize profits while considering the constraints imposed by the capacities of the shops. Let's define the decision variables, objective function, and constraints accordingly.

######### Decision Variables
- Let \( x_k \) be the quantity of spare part \( k \) to be produced.

######### Objective Function
- Maximize the total profit, which can be expressed as:
  \[
  \text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_k \times x_k
  \]

######### Constraints
- For each shop \( s \), the total worker-hours used must not exceed its capacity:
  \[
  \sum_{k=1}^{K} \text{time}_{k,s} \times x_k \leq \text{capacity}_s \quad \text{for each } s = 1, \ldots, S
  \]

- Non-negativity constraint for each \( x_k \):
  \[
  x_k \geq 0 \quad \text{for each } k = 1, \ldots, K
  \]

Below is the Linear Programming model formulated using LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
\begin{align*}
x_k & : \text{Quantity of spare part } k \text{ to be produced, for each } k = 1, \ldots, K
\end{align*}

\subsection*{Objective Function}
\begin{align*}
\text{Maximize } Z & = \sum_{k=1}^{K} \text{profit}_k \times x_k
\end{align*}

\subsection*{Constraints}
\begin{align*}
\sum_{k=1}^{K} \text{time}_{k,s} \times x_k & \leq \text{capacity}_s \quad \text{for each } s = 1, \ldots, S \\
x_k & \geq 0 \quad \text{for each } k = 1, \ldots, K
\end{align*}

\end{document}
```

This LaTeX code properly captures the constraints and objective function for the given problem, ensuring the solution maximizes profit while adhering to shop capacities.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
\begin{align*}
x_k & : \text{Quantity of spare part } k \text{ to be produced, for each } k = 1, \ldots, K
\end{align*}

\subsection*{Objective Function}
\begin{align*}
\text{Maximize } Z & = \sum_{k=1}^{K} \text{profit}_k \times x_k
\end{align*}

\subsection*{Constraints}
\begin{align*}
\sum_{k=1}^{K} \text{time}_{k,s} \times x_k & \leq \text{capacity}_s \quad \text{for each } s = 1, \ldots, S \\
x_k & \geq 0 \quad \text{for each } k = 1, \ldots, K
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

#### Extract data
num_parts = data['NumParts']
num_machines = data['NumMachines']
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']

#### Create a problem instance
problem = pulp.LpProblem("Maximize_Profits", pulp.LpMaximize)

#### Decision variables: Quantity of spare parts to produce
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(num_parts)]

#### Objective function
problem += pulp.lpSum(profit[k] * x[k] for k in range(num_parts)), "Total_Profit"

#### Constraints
for s in range(num_machines):
    problem += pulp.lpSum(time[k][s] * x[k] for k in range(num_parts)) <= capacity[s], f"Capacity_Constraint_{s}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

