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

\section*{Linear Programming Model for Nutritional Food Allocation}

\subsection*{Sets}
\begin{itemize}
    \item Let \( K \) be the set of foods, indexed by \( k \).
    \item Let \( M \) be the set of nutrients, indexed by \( m \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{price}_{k} \): the price per unit of food \( k \).
    \item \( \text{demand}_{m} \): the minimum required units of nutrient \( m \).
    \item \( \text{nutri}_{k, m} \): the units of nutrient \( m \) contained in one unit of food \( k \).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{quantity}_{k} \): the quantity of food \( k \) to purchase, for \( k \in K \).
\end{itemize}

\subsection*{Objective}
Minimize the total cost of the foods purchased:
\[
\text{Minimize } Z = \sum_{k \in K} \text{price}_{k} \cdot \text{quantity}_{k}
\]

\subsection*{Constraints}
The total amount of each nutrient provided must meet or exceed the demand:
\[
\sum_{k \in K} \text{nutri}_{k, m} \cdot \text{quantity}_{k} \geq \text{demand}_{m}, \quad \forall m \in M
\]

\subsection*{Non-negativity Constraints}
\[
\text{quantity}_{k} \geq 0, \quad \forall k \in K
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

\section*{Linear Programming Model for Nutritional Food Allocation}

\subsection*{Sets}
\begin{itemize}
    \item Let \( K \) be the set of foods, indexed by \( k \).
    \item Let \( M \) be the set of nutrients, indexed by \( m \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{price}_{k} \): the price per unit of food \( k \).
    \item \( \text{demand}_{m} \): the minimum required units of nutrient \( m \).
    \item \( \text{nutri}_{k, m} \): the units of nutrient \( m \) contained in one unit of food \( k \).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{quantity}_{k} \): the quantity of food \( k \) to purchase, for \( k \in K \).
\end{itemize}

\subsection*{Objective}
Minimize the total cost of the foods purchased:
\[
\text{Minimize } Z = \sum_{k \in K} \text{price}_{k} \cdot \text{quantity}_{k}
\]

\subsection*{Constraints}
The total amount of each nutrient provided must meet or exceed the demand:
\[
\sum_{k \in K} \text{nutri}_{k, m} \cdot \text{quantity}_{k} \geq \text{demand}_{m}, \quad \forall m \in M
\]

\subsection*{Non-negativity Constraints}
\[
\text{quantity}_{k} \geq 0, \quad \forall k \in K
\]

\end{document}</MATH_MODEL>
<DATA>
{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the problem statement
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

#### Sets
K = range(len(data['price']))  #### Foods
M = range(len(data['demand']))  #### Nutrients

#### Create the linear programming problem
problem = pulp.LpProblem("Nutritional_Food_Allocation", pulp.LpMinimize)

#### Decision Variables
quantity = pulp.LpVariable.dicts("quantity", K, lowBound=0)

#### Objective Function
problem += pulp.lpSum(data['price'][k] * quantity[k] for k in K), "Total_Cost"

#### Constraints
for m in M:
    problem += pulp.lpSum(data['nutrition'][k][m] * quantity[k] for k in K) >= data['demand'][m], f"Nutrient_Constraint_{m}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

