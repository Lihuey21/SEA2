from flask import Flask, render_template, request

app = Flask(__name__)

# Currency conversion rates (static for now, you can integrate with an API for live rates)
conversion_rates = {
    "USD": {"MYR": 4.7, "SGD": 1.35, "JPY": 110},
    "MYR": {"USD": 0.21, "SGD": 0.29, "JPY": 23.4},
    "SGD": {"USD": 0.74, "MYR": 3.4, "JPY": 17.5},
    "JPY": {"USD": 0.0091, "MYR": 0.043, "SGD": 0.057}
}

# Calculator functions
def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a / b

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    mode = request.form.get("mode", "calculator")  # Get the selected mode, default to calculator
    source_currency = "MYR"  # Default source currency
    target_currency = "SGD"  # Default target currency

    if request.method == "POST":
        if mode == "calculator":
            try:
                num1 = float(request.form.get("num1", ""))
                num2 = float(request.form.get("num2", ""))
                operation = request.form.get("operation", "")

                if operation == "+":
                    result = add(num1, num2)
                elif operation == "-":
                    result = subtract(num1, num2)
               
                
        elif mode == "converter":
            try:
                amount = float(request.form.get("amount", ""))
                source_currency = request.form.get("source_currency", "MYR")
                target_currency = request.form.get("target_currency", "SGD")

                # Ensure the conversion rates dictionary contains the required currencies
                rate = conversion_rates.get(source_currency, {}).get(target_currency, None)
                if rate is not None:
                    result = f"{amount} {source_currency} = {amount * rate:.2f} {target_currency}"
                else:
                    result = "Invalid currency conversion pair."
            except ValueError:
                result = "Please enter valid numbers."

    return render_template("index.html", result=result, mode=mode, source_currency=source_currency, target_currency=target_currency)

if __name__ == "__main__":
    app.run(debug=True)
    
