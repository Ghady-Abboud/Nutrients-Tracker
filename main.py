'''

/food/{fdcId} : Fetches details for one food item by FDC ID
/foods : Fetches details for multiple food items using input FDC IDs
/foods/list : Returns a paged list of foods, in the 'abridged' format
/foods/search : Returns a list of foods that matched search (query) keywords

'''

from flask import Flask, jsonify, render_template, request, redirect, url_for
import requests


app = Flask(__name__)

def search(query): 


    API_URL = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key=n0REEKBm9KoyfBmL0UneSt5WSej8lzTmziYBpncl&query={query}"
    response = requests.get(API_URL) 

    try:
        if response.status_code == 200:
            search_results = response.json()
            
            shorter_nutrients = {
                "Protein" : "Protein",
                "Total lipid (fat)" : "Fat",
                "Energy": "Energy",
                "Total Sugars":"Total Sugar",
                "Fiber, total dietary" : "Fiber",
                "Calcium, Ca": "Calcium",
                "Iron, Fe": "Iron",
                "Sodium, Na":"Sodium",
                "Vitamin A, IU":"Vitamin A",
                "Vitamin C, total ascorbic acid" : "Vitamin C",
                "Cholesterol": "Cholesterol",
                "Fatty acids, total trans": "Trans Fat",
                "Fatty acids, total saturated":"Saturated Fat",
                "Carbohydrate, by difference" :"Carbohydrates"
            }

            relevant_nutrients = ['Protein',    
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

            food_name = search_results['foods'][0]['description']
            nutrients = [] 
            for nutrient in search_results['foods'][0]['foodNutrients']:
                if nutrient['nutrientName'] in relevant_nutrients:
                    
                    if nutrient['nutrientName'] in shorter_nutrients:
                        # If it is, use the shorter version
                        nutrient_name = shorter_nutrients[nutrient['nutrientName']]
                        
                    nutrient_info = {
                        'name': nutrient_name,
                        'value': nutrient['value'],
                        'unit': nutrient['unitName']
                    }
                    
                    nutrients.append(nutrient_info)
            
            filtered_data = {
                'Name' : food_name,
                'Nutrients' : nutrients
            }
            
            return filtered_data 
        
    except:
        return "Error: Unable to retrieve search results"


@app.route('/', methods = ['GET','POST'])
def home():
    if request.method == 'POST' :
        new_query = request.form['query']
        results = search(query = new_query)
        return render_template('index.html',results=results)
        
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)