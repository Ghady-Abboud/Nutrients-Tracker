
'''
4 different API endpoints: 

/food/{fdcId} : Fetches details for one food item by FDC ID
/foods : Fetches details for multiple food items using input FDC IDs
/foods/list : Returns a paged list of foods, in the 'abridged' format
/foods/search : Returns a list of foods that matched search (query) keywords   ---> This will be the one we'll use 

Import these modules when working with flask: jsonify, request

'''
from flask import Flask, jsonify, render_template, request, redirect, url_for
import requests

response = requests.get('https://api.nal.usda.gov/fdc/v1/foods/list?api_key=n0REEKBm9KoyfBmL0UneSt5WSej8lzTmziYBpncl') 
data = response.json() # Parse the content of of an HTTP reponse as JSON format 


app = Flask(__name__)

@app.route('/foods/search') 
def search(): # Food Search function 

    query = request.args.get('query') # This gets the query from the user then appends it to the api url

    API_URL = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key=n0REEKBm9KoyfBmL0UneSt5WSej8lzTmziYBpncl&query={query}"
    response = requests.get(API_URL) # This retrieves the HTTP response of the query 


    # If the query from the user was successful, then filter out the data by the relevant nutrients 
    if response.status_code == 200:
        search_results = response.json()

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
                nutrient_info = {
                    'name': nutrient['nutrientName'],
                    'value': nutrient['value'],
                    'unit': nutrient['unitName']
                }
                nutrients.append(nutrient_info)
        
        filtered_data = {
            'Name' : food_name,
            'Nutrients' : nutrients
        }
        return jsonify(filtered_data)
 
    else:
        return jsonify({'Error': 'Unable to retrieve search results'})


@app.route('/',methods = ['GET','POST'])
def index():

    if request.method == 'POST' :
        query = request.form['query']
        return redirect(url_for('search',query=query))
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)