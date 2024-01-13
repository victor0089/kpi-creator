from flask import Flask, render_template, request, redirect, flash
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def calculate_kpis(df):
    try:
        total_sales = df['Sales'].sum()
        average_order_value = df['Sales'].mean()
        total_customers = df['CustomerID'].nunique()
        conversion_rate = total_customers / len(df) * 100
        return total_sales, average_order_value, total_customers, conversion_rate
    except Exception as e:
        flash(f"Error calculating KPIs: {str(e)}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            flash("No file part.")
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash("No selected file.")
            return redirect(request.url)

        if file:
            df = pd.read_excel(file)
            kpis = calculate_kpis(df)
            if kpis:
                total_sales, average_order_value, total_customers, conversion_rate = kpis
                return render_template('results.html', 
                                       total_sales=total_sales,
                                       average_order_value=average_order_value,
                                       total_customers=total_customers,
                                       conversion_rate=conversion_rate)
            else:
                return redirect(request.url)
    except Exception as e:
        flash(f"Error processing file: {str(e)}")
        return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
