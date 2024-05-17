from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    results, food_names = perform_search(query)
    return jsonify({'results': results, 'food_names': food_names})

def perform_search(query):
    API_URL = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key=n0REEKBm9KoyfBmL0UneSt5WSej8lzTmziYBpncl&query={query}"
    response = requests.get(API_URL)
    
    try:
        if response.status_code == 200:
            search_results = response.json()
            
            shorter_nutrients = {
                "Protein": "Protein",
                "Total lipid (fat)": "Fat",
                "Energy": "Energy",
                "Total Sugars": "Total Sugar",
                "Fiber, total dietary": "Fiber",
                "Calcium, Ca": "Calcium",
                "Iron, Fe": "Iron",
                "Sodium, Na": "Sodium",
                "Vitamin A, IU": "Vitamin A",
                "Vitamin C, total ascorbic acid": "Vitamin C",
                "Cholesterol": "Cholesterol",
                "Fatty acids, total trans": "Trans Fat",
                "Fatty acids, total saturated": "Saturated Fat",
                "Carbohydrate, by difference": "Carbohydrates"
            }

            relevant_nutrients = [
                'Protein',
                "Total lipid (fat)",
                "Energy",
                "Total Sugars",
                "Fiber, total dietary",
                "Calcium, Ca",
                "Iron, Fe",
                "Sodium, Na",
                "Vitamin A, IU",
                "Vitamin C, total ascorbic acid",
                "Cholesterol",
                "Fatty acids, total trans",
                "Fatty acids, total saturated",
                "Carbohydrate, by difference"
            ]

            foods = search_results['foods']
            food_names = [food['description'] for food in foods]

            nutrients = []
            if foods:
                for nutrient in foods[0]['foodNutrients']:
                    if nutrient['nutrientName'] in relevant_nutrients:
                        nutrient_name = shorter_nutrients.get(nutrient['nutrientName'], nutrient['nutrientName'])
                        nutrient_info = {
                            'name': nutrient_name,
                            'value': nutrient['value'],
                            'unit': nutrient['unitName']
                        }
                        nutrients.append(nutrient_info)

                filtered_data = {
                    'Name': foods[0]['description'],
                    'Nutrients': nutrients
                }
            else:
                filtered_data = {}

            return filtered_data, food_names
    except Exception as e:
        print(f"Error: {e}")
        return "Error: Unable to retrieve search results", []

if __name__ == "__main__":
    app.run(debug=True)
