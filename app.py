app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)

    if file:
        df = pd.read_excel(file)
        # Perform KPI calculations here
        # For example: total_sales = df['Sales'].sum()
        
        # Render results page with KPIs
        return render_template('results.html', total_sales=total_sales)
if __name__ == '__main__':
    app.run(debug=True)
