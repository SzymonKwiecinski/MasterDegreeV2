# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO: 

- A manager of an oil refinery has \var{allocated_i} million barrels of crude oil type \var{i} allocated for production during the coming month. 
- These resources can be used to make \var{P} different products. product \var{p} sells for $ \var{price_p} per barrel.
- There are \var{L} production processes. Process \var{l} uses \var{input_l_i} barrels of each crude \var{i}, and produces \var{output_l_p} barrels of each product \var{p}. 
- Process \var{l} has a cost of \var{cost_l} per barrel of product produced.
- All \var{input_l_i} quantities and \var{output_l_p} quanitites are in barrels. 
- There are no separate cost items for the cost of the crudes, as they have already been allocated.

INPUT FORMAT: 

{
    "allocated": [allocated_i for i in 1, ..., O],
    "price": [price_p for p in 1, ..., P],
    "input": [[input_l_i for i in 1, ..., O] for l in 1, ..., L],
    "output": [[output_l_p for p in 1, ..., P] for l in 1, ..., L],
    "cost": [cost_l for l in 1, ..., L]
}

OBJECTIVE: We want to know how many times should we execute each process to maximize the revenue for the next month (you can assume that the number of times that each process is executed is a floating point number)

OUTPUT INFO:

- \var{revenue} is the total revenue for the month.
- \var{execute_l} is the number of times that process \var{l} should be executed.

OUTPUT FORMAT:

{
    "revenue": revenue,
    "execute": [execute_l for l in 1, ..., L]
}

</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To model the given problem as a Linear Programming (LP) problem, we need to maximize the revenue by deciding how many times each production process should be executed. The inputs provided to the model include allocated crude oil, prices of products, input and output coefficients for each production process, and the cost associated with each production process. Here is the mathematical formulation of the problem:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( x_l \) be the number of times process \( l \) is executed, for \( l = 1, \ldots, L \).
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize Revenue: } Z = \sum_{p=1}^{P} \sum_{l=1}^{L} \text{output}_{l,p} \cdot \text{price}_p \cdot x_l - \sum_{l=1}^{L} \text{cost}_l \cdot \sum_{p=1}^{P} \text{output}_{l,p} \cdot x_l
\]

\textbf{Constraints:}
\begin{itemize}
    \item \text{Crude Oil Allocation Constraints:}
    \[
    \sum_{l=1}^{L} \text{input}_{l,i} \cdot x_l \leq \text{allocated}_i, \quad \forall i = 1, \ldots, O
    \]

    \item \text{Non-negativity Constraints:}
    \[
    x_l \geq 0, \quad \forall l = 1, \ldots, L
    \]
\end{itemize}

\textbf{Where:}
\begin{itemize}
    \item \( \text{allocated}_i \) is the available quantity of crude oil type \( i \).
    \item \( \text{price}_p \) is the selling price per barrel of product \( p \).
    \item \( \text{input}_{l,i} \) is the number of barrels of crude oil type \( i \) consumed by process \( l \).
    \item \( \text{output}_{l,p} \) is the number of barrels of product \( p \) produced by process \( l \).
    \item \( \text{cost}_l \) is the production cost per barrel of product produced by process \( l \).
\end{itemize}

\end{document}
```

This linear programming model helps determine the optimal execution levels of each production process to maximize the total revenue while respecting the crude oil allocation constraints. The revenue is calculated by considering the selling price of products and subtracting the production costs.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( x_l \) be the number of times process \( l \) is executed, for \( l = 1, \ldots, L \).
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize Revenue: } Z = \sum_{p=1}^{P} \sum_{l=1}^{L} \text{output}_{l,p} \cdot \text{price}_p \cdot x_l - \sum_{l=1}^{L} \text{cost}_l \cdot \sum_{p=1}^{P} \text{output}_{l,p} \cdot x_l
\]

\textbf{Constraints:}
\begin{itemize}
    \item \text{Crude Oil Allocation Constraints:}
    \[
    \sum_{l=1}^{L} \text{input}_{l,i} \cdot x_l \leq \text{allocated}_i, \quad \forall i = 1, \ldots, O
    \]

    \item \text{Non-negativity Constraints:}
    \[
    x_l \geq 0, \quad \forall l = 1, \ldots, L
    \]
\end{itemize}

\textbf{Where:}
\begin{itemize}
    \item \( \text{allocated}_i \) is the available quantity of crude oil type \( i \).
    \item \( \text{price}_p \) is the selling price per barrel of product \( p \).
    \item \( \text{input}_{l,i} \) is the number of barrels of crude oil type \( i \) consumed by process \( l \).
    \item \( \text{output}_{l,p} \) is the number of barrels of product \( p \) produced by process \( l \).
    \item \( \text{cost}_l \) is the production cost per barrel of product produced by process \( l \).
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads('{"O": 2, "P": 2, "L": 3, "Allocated": [8000, 5000], "Price": [38, 33], "Input": [[3, 5], [1, 1], [5, 3]], "Output": [[4, 3], [1, 1], [3, 4]], "Cost": [51, 11, 40]}')

#### Constants
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output_data = data['Output']
cost = data['Cost']

#### Create a linear programming problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(1, L + 1), lowBound=0, cat='Continuous')

#### Objective function
revenue = pulp.lpSum(output_data[l-1][p-1] * price[p-1] * x[l] for l in range(1, L + 1) for p in range(1, P + 1))
costs = pulp.lpSum(cost[l-1] * pulp.lpSum(output_data[l-1][p-1] * x[l] for p in range(1, P + 1)) for l in range(1, L + 1))
problem += revenue - costs, "Total_Profit"

#### Constraints
for i in range(1, O + 1):
    problem += pulp.lpSum(input_data[l-1][i-1] * x[l] for l in range(1, L + 1)) <= allocated[i-1], f"Crude_Oil_Allocation_{i}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

