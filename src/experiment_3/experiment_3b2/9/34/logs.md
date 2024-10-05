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
To solve this problem, we will formulate it as a Linear Programming (LP) model. The goal is to minimize the total cost of purchasing foods while meeting the nutritional requirements. We will express this problem in a mathematical form and then convert it to a LaTeX format.

Let's define the variables and constraints for the LP problem.

######### Variables
- \( x_k \): Quantity of food \( k \) to purchase.

######### Parameters
- \( \text{price}_k \): Price per unit of food \( k \).
- \( \text{demand}_m \): Minimum required units of nutrient \( m \).
- \( \text{nutri}_{k, m} \): Units of nutrient \( m \) in one unit of food \( k \).

######### Objective
Minimize the total cost of purchasing the foods:
\[ \text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_k \cdot x_k \]

######### Constraints
Ensure that the nutritional demands are met:
\[ \sum_{k=1}^{K} \text{nutri}_{k, m} \cdot x_k \geq \text{demand}_m \quad \forall m = 1, \ldots, M \]

######### Non-negativity constraints
\[ x_k \geq 0 \quad \forall k = 1, \ldots, K \]

Now, let's write the LaTeX code for this LP formulation:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

We are given:

- Prices of foods: \(\text{price}_k\) for \(k = 1, \ldots, K\).
- Nutritional demands: \(\text{demand}_m\) for \(m = 1, \ldots, M\).
- Nutrition content: \(\text{nutri}_{k, m}\) for each food \(k\) and nutrient \(m\).

\subsection*{Objective}
Minimize the total cost of purchasing foods:
\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_k \cdot x_k
\]

\subsection*{Constraints}
Meet the nutritional demands:
\[
\sum_{k=1}^{K} \text{nutri}_{k, m} \cdot x_k \geq \text{demand}_m \quad \forall m = 1, \ldots, M
\]

\subsection*{Non-negativity Constraints}
\[
x_k \geq 0 \quad \forall k = 1, \ldots, K
\]

\end{document}
```

This LaTeX code provides a complete representation of the linear programming model for the diet problem described. It includes the objective function and the constraints needed to ensure a balanced diet at the minimum cost.

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

We are given:

- Prices of foods: \(\text{price}_k\) for \(k = 1, \ldots, K\).
- Nutritional demands: \(\text{demand}_m\) for \(m = 1, \ldots, M\).
- Nutrition content: \(\text{nutri}_{k, m}\) for each food \(k\) and nutrient \(m\).

\subsection*{Objective}
Minimize the total cost of purchasing foods:
\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} \text{price}_k \cdot x_k
\]

\subsection*{Constraints}
Meet the nutritional demands:
\[
\sum_{k=1}^{K} \text{nutri}_{k, m} \cdot x_k \geq \text{demand}_m \quad \forall m = 1, \ldots, M
\]

\subsection*{Non-negativity Constraints}
\[
x_k \geq 0 \quad \forall k = 1, \ldots, K
\]

\end{document}</MATH_MODEL>
<DATA>
{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON format
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

#### Number of foods and nutrients
K = len(data['price'])
M = len(data['demand'])

#### Create the problem variable
problem = pulp.LpProblem("Minimize_Food_Cost", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

#### Objective function
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K)), "Total_Cost"

#### Constraints for nutritional demands
for m in range(M):
    problem += (pulp.lpSum(data['nutrition'][k][m] * x[k] for k in range(K)) >= data['demand'][m]), f"Nutritional_Demand_{m+1}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

