class Logic:
    def _init_(self, expression):
        self.expression = expression  

    def evaluate(self, model):
        """Evaluates the expression based on the truth values in the model."""
        tokens = self.tokenize(self.expression)
        return self.evaluate_tokens(tokens, model)

    def tokenize(self, expr):
        """Tokenizes the expression into symbols, operators, and parentheses."""
        tokens = []
        temp = ""
        for char in expr:
            if char in "¬∧∨→()":  
                if temp:
                    tokens.append(temp)
                    temp = ""
                tokens.append(char)
            elif char.strip():  
                temp += char
        if temp:
            tokens.append(temp)
        return tokens

    def evaluate_tokens(self, tokens, model):
        """Evaluates a tokenized logical expression using a stack-based approach."""
        def precedence(op):
            return {"¬": 3, "∧": 2, "∨": 1, "→": 0}.get(op, -1)

        def apply_operator(op, values):
            if op == "¬":
                return not values.pop()
            b, a = values.pop(), values.pop()
            if op == "∧":
                return a and b
            if op == "∨":
                return a or b
            if op == "→":
                return not a or b  
        output = []
        operators = []
        for token in tokens:
            if token in model:
                output.append(model[token])
            elif token == "¬":
                operators.append(token)
            elif token in {"∧", "∨", "→"}:
                while operators and precedence(operators[-1]) >= precedence(token):
                    output.append(operators.pop())
                operators.append(token)
            elif token == "(":
                operators.append(token)
            elif token == ")":
                while operators and operators[-1] != "(":
                    output.append(operators.pop())
                operators.pop()

        while operators:
            output.append(operators.pop())

        
        values = []
        for token in output:
            if isinstance(token, bool):
                values.append(token)
            else:
                values.append(apply_operator(token, values))
        return values[0]

class Main:
    def _init_(self):
        self.model = {}

    def set_truth_values(self, assignments):
        """Assigns truth values to symbols."""
        for symbol, value in assignments.items():
            self.model[symbol] = value

    def check_truth(self, expression):
        """Checks if a logical expression evaluates to True given the model."""
        logic = Logic( expression)
        return logic.evaluate(self.model)


main = Main()
main.set_truth_values({"P": True, "Q": False})

expression1 = "(P → Q) ∨ ¬P"
expression2 = "P ∧ Q"

print(main.check_truth(expression1))  
print(main.check_truth(expression2))  