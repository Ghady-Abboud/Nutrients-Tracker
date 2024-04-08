
'''
We have 4 different API endpoints: 

/food/{fdcId} : Fetches details for one food item by FDC ID
/foods : Fetches details for multiple food items using input FDC IDs
/foods/list : Returns a paged list of foods, in the 'abridged' format
/foods/search : Returns a list of foods that matched search (query) keywords   ---> This will be the one we'll use 

Import these modules when working with flask: jsonify, request

'''
from flask import Flask, jsonify, request, render_template
import requests

response = requests.get('https://api.nal.usda.gov/fdc/v1/foods/list?api_key=n0REEKBm9KoyfBmL0UneSt5WSej8lzTmziYBpncl') 
data = response.json() # Parse the content of of an HTTP reponse as JSON format 


app = Flask(__name__)

@app.route('/foods/search') # Define the routes for the search function 
def search():
    query = request.args.get('query')

    API_URL = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key=n0REEKBm9KoyfBmL0UneSt5WSej8lzTmziYBpncl&query={query}"
    response = requests.get(API_URL)


    if response.status_code == 200:
        search_results = response.json()
        food_name = search_results['foods'][0]['description']
        nutrients = [] 
        for nutrient in search_results['foods'][0]['foodNutrients']:
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
    
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)