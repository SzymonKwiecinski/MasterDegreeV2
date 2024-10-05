# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- A foundry receives a specific order for \var{n_steel_quant} tons of steel. 
- This steel must meet the following characteristics: it must contain at least \var{mn_percent} percentage of manganese (Mn) while its percentage of silicon (SI) must be between \var{si_min} and \var{si_max}.
- To cast this steel, the foundry has limited quantities of several types of minerals.
- The contents expressed in percentage per mineral \var{k} are \var{contsi_{k}} for Si and \var{contmn_{k}} for Mn.
- The process for producing steel is such that direct addition of Mn is possible.
- This Manganese is available at a price of \var{mang_price} million euros per ton. 
- As for the minerals, it costs \var{cost_{k}} million euros per thousand tons for mineral \var{k}.
- The foundry plans to sell the steel produced at \var{sell_price} million euros per ton.
- The cost of smelting a ton of mineral is \var{melt_price} million euros.

INPUT FORMAT:

{
	"n_steel_quant": n_steel_quant,
	"mn_percent": mn_percent,
	"si_min": si_min,
	"si_max": si_max,
	"contsi": [contsi_{k} for k in 1,...,K]
	"contmn": [contmn_{k} for k in 1,...,K]
	"mang_price": mang_price,
	"cost": [cost_{k} for k in 1,...,K]
	"sell_price": sell_price,
	"melt_price": melt_price
}

OBJECTIVE: How should the manufacture manage the steel to maximize profit?

OUTPUT INFO:

- \var{amount} represents the amount of each mineral melted
- \var{num_mang} represents the amount of Manganese directly added

OUTPUT FORMAT:

{
	"amount": [amount_{k} for k in 1,...,K]
	"num_mang": [num_mang]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To address the problem of maximizing profits in steel production for the foundry, we can formulate a linear programming model. The objective is to decide on the optimal quantities of each mineral and manganese to use, ensuring compliance with the required steel characteristics while minimizing costs. Below is the mathematical model expressed in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Mathematical Model:}

\begin{itemize}
    \item Let \( K \) be the number of different minerals available.
    \item Let \( \text{amount}_k \) be the amount (in tons) of mineral \( k \) to be used.
    \item Let \( \text{num\_mang} \) be the amount (in tons) of Manganese directly added.
    \item Let \( \text{contsi}_k \) and \( \text{contmn}_k \) be the Si and Mn content percentage of mineral \( k \).
    \item Let \( \text{cost}_k \) be the cost of using 1000 tons of mineral \( k \) in million euros.
    \item Let \( \text{n\_steel\_quant} \) be the total amount of steel required in tons.
    \item Let \( \text{mn\_percent} \), \( \text{si\_min} \), and \( \text{si\_max} \) be the specified Mn percentage, minimum Si percentage, and maximum Si percentage respectively.
    \item Let \( \text{mang\_price} \) and \( \text{melt\_price} \) be the cost of Manganese per ton and smelting cost per ton respectively.

\end{itemize}

\textbf{Objective Function:}

Maximize profit:
\[
\text{Maximize: } \text{profit} = \text{sell\_price} \cdot \text{n\_steel\_quant} - \sum_{k=1}^{K} \left( \text{amount}_k \cdot \left(\frac{\text{cost}_k}{1000} + \text{melt\_price}\right) \right) - \text{num\_mang} \cdot \text{mang\_price}
\]

\textbf{Constraints:}

\begin{align*}
& 1. \ \sum_{k=1}^{K} \text{amount}_k + \text{num\_mang} = \text{n\_steel\_quant} \quad &\text{(Balance constraint for total steel quantity)} \\
& 2. \ \sum_{k=1}^{K} \text{contmn}_k \cdot \text{amount}_k + \text{num\_mang} \geq \text{mn\_percent} \cdot \text{n\_steel\_quant} \quad &\text{(Manganese content requirement)} \\
& 3. \ \text{si\_min} \cdot \text{n\_steel\_quant} \leq \sum_{k=1}^{K} \text{contsi}_k \cdot \text{amount}_k \leq \text{si\_max} \cdot \text{n\_steel\_quant} \quad &\text{(Silicon content requirement)} \\
& 4. \ \text{amount}_k \geq 0 \quad \forall k=1,...,K \quad &\text{(Non-negativity for minerals)} \\
& 5. \ \text{num\_mang} \geq 0 \quad &\text{(Non-negativity for Manganese)}
\end{align*}

\end{document}
```

This linear programming model provides the foundation for computing the optimal mineral and manganese quantities needed to maximize profit while adhering to the steel composition requirements. The constraints ensure that the steel produced meets the minimum and maximum percentages of manganese and silicon, while the objective function maximizes the revenue from selling the steel minus the costs of minerals, manganese, and smelting.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Mathematical Model:}

\begin{itemize}
    \item Let \( K \) be the number of different minerals available.
    \item Let \( \text{amount}_k \) be the amount (in tons) of mineral \( k \) to be used.
    \item Let \( \text{num\_mang} \) be the amount (in tons) of Manganese directly added.
    \item Let \( \text{contsi}_k \) and \( \text{contmn}_k \) be the Si and Mn content percentage of mineral \( k \).
    \item Let \( \text{cost}_k \) be the cost of using 1000 tons of mineral \( k \) in million euros.
    \item Let \( \text{n\_steel\_quant} \) be the total amount of steel required in tons.
    \item Let \( \text{mn\_percent} \), \( \text{si\_min} \), and \( \text{si\_max} \) be the specified Mn percentage, minimum Si percentage, and maximum Si percentage respectively.
    \item Let \( \text{mang\_price} \) and \( \text{melt\_price} \) be the cost of Manganese per ton and smelting cost per ton respectively.

\end{itemize}

\textbf{Objective Function:}

Maximize profit:
\[
\text{Maximize: } \text{profit} = \text{sell\_price} \cdot \text{n\_steel\_quant} - \sum_{k=1}^{K} \left( \text{amount}_k \cdot \left(\frac{\text{cost}_k}{1000} + \text{melt\_price}\right) \right) - \text{num\_mang} \cdot \text{mang\_price}
\]

\textbf{Constraints:}

\begin{align*}
& 1. \ \sum_{k=1}^{K} \text{amount}_k + \text{num\_mang} = \text{n\_steel\_quant} \quad &\text{(Balance constraint for total steel quantity)} \\
& 2. \ \sum_{k=1}^{K} \text{contmn}_k \cdot \text{amount}_k + \text{num\_mang} \geq \text{mn\_percent} \cdot \text{n\_steel\_quant} \quad &\text{(Manganese content requirement)} \\
& 3. \ \text{si\_min} \cdot \text{n\_steel\_quant} \leq \sum_{k=1}^{K} \text{contsi}_k \cdot \text{amount}_k \leq \text{si\_max} \cdot \text{n\_steel\_quant} \quad &\text{(Silicon content requirement)} \\
& 4. \ \text{amount}_k \geq 0 \quad \forall k=1,...,K \quad &\text{(Non-negativity for minerals)} \\
& 5. \ \text{num\_mang} \geq 0 \quad &\text{(Non-negativity for Manganese)}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'n_steel_quant': 1000,
    'mn_percent': 0.45,
    'si_min': 3.25,
    'si_max': 5.0,
    'contsi': [4.0, 1.0, 0.6],
    'contmn': [0.45, 0.5, 0.4],
    'mang_price': 8.0,
    'cost': [21, 25, 15],
    'sell_price': 0.45,
    'melt_price': 0.005
}

K = len(data['contsi'])  #### Number of different minerals available

#### Variables
amount = [pulp.LpVariable(f"amount_{k}", lowBound=0) for k in range(K)]
num_mang = pulp.LpVariable("num_mang", lowBound=0)

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Objective Function: Maximize profit
profit = (data['sell_price'] * data['n_steel_quant'] 
          - sum(amount[k] * (data['cost'][k]/1000 + data['melt_price']) for k in range(K))
          - num_mang * data['mang_price'])

problem += profit, "Profit"

#### Constraints

#### Balance constraint for total steel quantity
problem += sum(amount) + num_mang == data['n_steel_quant'], "Total_Steel_Quantity"

#### Manganese content requirement
problem += sum(data['contmn'][k] * amount[k] for k in range(K)) + num_mang >= data['mn_percent'] * data['n_steel_quant'], "Mn_Content"

#### Silicon content requirement
problem += data['si_min'] * data['n_steel_quant'] <= sum(data['contsi'][k] * amount[k] for k in range(K)), "Si_Content_Min"
problem += sum(data['contsi'][k] * amount[k] for k in range(K)) <= data['si_max'] * data['n_steel_quant'], "Si_Content_Max"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

