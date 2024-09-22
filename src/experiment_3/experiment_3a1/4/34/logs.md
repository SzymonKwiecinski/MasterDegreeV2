# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- We assume that there are available at the market different foods and that the food \var{k} sells at a price \var{price_{k}} per unit. 
- In addition there are several basic nutritional ingredients and, to achieve a balanced diet, each individual must receive at least \var{demand_{m}} units of nutrient \var{m} per day. 
- Finally, we assume that each unit of food \var{k} contains \var{nutri_{k, m}} units of nutrition \var{m}

INPUT FORMAT:

{
	"price": [price_{k} for k in 1,...,K],
	"demand": [demand_{m} for m in 1,...,M],
	"nutrition": [[nutri_{k, m} for m in 1,...,M] for k in 1,...,K]
}


OBJECTIVE: We want to minimize the total prices of the foods to purchase.

OUTPUT INFO:

- \var{quantity} represents the quantity of each food to purchase

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

\section*{Linear Programming Model}

\subsection*{Definitions}

Let:
\begin{itemize}
    \item \( K \) be the number of different foods,
    \item \( M \) be the number of nutritional ingredients,
    \item \( \text{price}_k \) be the price per unit of food \( k \),
    \item \( \text{demand}_m \) be the minimum daily requirement of nutrient \( m \),
    \item \( \text{nutri}_{k, m} \) be the amount of nutrient \( m \) in one unit of food \( k \),
    \item \( \text{quantity}_k \) be the quantity of food \( k \) to purchase.
\end{itemize}

\subsection*{Objective Function}

The objective is to minimize the total cost of the foods purchased:

\[
\text{Minimize } Z = \sum_{k=1}^{K} \text{price}_k \cdot \text{quantity}_k
\]

\subsection*{Constraints}

To ensure that the dietary requirements are met for each nutrient \( m \), we have the following constraints:

\[
\sum_{k=1}^{K} \text{nutri}_{k, m} \cdot \text{quantity}_k \geq \text{demand}_m \quad \forall m \in \{1, 2, \ldots, M\}
\]

Additionally, we have non-negativity constraints:

\[
\text{quantity}_k \geq 0 \quad \forall k \in \{1, 2, \ldots, K\}
\]

\subsection*{Summary}

The linear programming model can be summarized as follows:

\begin{align*}
\text{Minimize } & Z = \sum_{k=1}^{K} \text{price}_k \cdot \text{quantity}_k \\
\text{subject to } & \sum_{k=1}^{K} \text{nutri}_{k, m} \cdot \text{quantity}_k \geq \text{demand}_m \quad \forall m \\
                   & \text{quantity}_k \geq 0 \quad \forall k
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

\section*{Linear Programming Model}

\subsection*{Definitions}

Let:
\begin{itemize}
    \item \( K \) be the number of different foods,
    \item \( M \) be the number of nutritional ingredients,
    \item \( \text{price}_k \) be the price per unit of food \( k \),
    \item \( \text{demand}_m \) be the minimum daily requirement of nutrient \( m \),
    \item \( \text{nutri}_{k, m} \) be the amount of nutrient \( m \) in one unit of food \( k \),
    \item \( \text{quantity}_k \) be the quantity of food \( k \) to purchase.
\end{itemize}

\subsection*{Objective Function}

The objective is to minimize the total cost of the foods purchased:

\[
\text{Minimize } Z = \sum_{k=1}^{K} \text{price}_k \cdot \text{quantity}_k
\]

\subsection*{Constraints}

To ensure that the dietary requirements are met for each nutrient \( m \), we have the following constraints:

\[
\sum_{k=1}^{K} \text{nutri}_{k, m} \cdot \text{quantity}_k \geq \text{demand}_m \quad \forall m \in \{1, 2, \ldots, M\}
\]

Additionally, we have non-negativity constraints:

\[
\text{quantity}_k \geq 0 \quad \forall k \in \{1, 2, \ldots, K\}
\]

\subsection*{Summary}

The linear programming model can be summarized as follows:

\begin{align*}
\text{Minimize } & Z = \sum_{k=1}^{K} \text{price}_k \cdot \text{quantity}_k \\
\text{subject to } & \sum_{k=1}^{K} \text{nutri}_{k, m} \cdot \text{quantity}_k \geq \text{demand}_m \quad \forall m \\
                   & \text{quantity}_k \geq 0 \quad \forall k
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided in JSON format
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

#### Number of foods and nutrients
K = len(data['price'])
M = len(data['demand'])

#### Define the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

#### Define decision variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

#### Objective function: Minimize the total cost
problem += pulp.lpSum(data['price'][k] * quantity[k] for k in range(K)), "Total_Cost"

#### Constraints to meet nutritional demands
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * quantity[k] for k in range(K)) >= data['demand'][m], f"Nutrient_Requirement_{m+1}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

