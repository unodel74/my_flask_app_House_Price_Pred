from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

# Cargar el modelo entrenado
best_model = joblib.load('models/best_model.pkl')

# Definir las opciones del campo district
district_options = [
    'Arganzuela', 'barajas', 'barrio de salamanca', 'carabanchel', 'centro',
    'chamberi', 'chamartin', 'ciudad lineal', 'fuencarral', 'hortaleza',
    'latina', 'moncloa', 'moratalaz', 'puente-de-vallecas', 'retiro',
    'san-blas', 'tetuan', 'usera', 'vicalvaro', 'villa-de-vallecas',
    'villaverde'
]

# Ordenar las opciones alfabéticamente
district_options.sort(key=str.lower)

@app.route('/')
def home():
    return render_template('index.html', district_options=district_options)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Obtener los datos del formulario
        rooms = int(request.form['rooms'])
        m2 = int(request.form['m2'])
        elevator = int(request.form['elevator'])
        garage = 0
        floor = int(request.form['floor'])
        int_ext = request.form['int_ext']
        district = request.form['district']
        
        # Crear un DataFrame con los datos del formulario
        sample = pd.DataFrame([{
            'rooms': rooms,
            'm2': m2,
            'elevator': elevator,
            'garage': garage,
            'floor': floor,
            'int/ext': int_ext,
            'district': district
        }])
        
        # Realizar la predicción
        predict_1 = best_model.predict(sample)
        prediction = round(1.1 * predict_1[0])   
        
        # Formatear el número con separadores de miles, usando puntos, y símbolo del euro
        prediction_formatted = '{:,.0f} €'.format(prediction).replace(',', '.')
        
        return render_template('index.html', 
                               prediction=prediction_formatted,
                               rooms=rooms,
                               m2=m2,
                               elevator=elevator,
                               floor=floor,
                               int_ext=int_ext,
                               district=district,
                               district_options=district_options)

if __name__ == '__main__':
    app.run(debug=True)

