document.addEventListener('DOMContentLoaded', (event) => {
    const searchBar = document.getElementById('searchbar');
    const dataDisplay = document.getElementById('data_display');
    const suggestionsList = document.getElementById('suggestions'); 
    const ItemList = new Array()

    searchBar.addEventListener('input', function () {
        const query = searchBar.value.trim();

        if (query.length > 0) {
            fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({ 'query': query })
            })
            .then(response => response.json())
            .then(data => {
                displaySuggestions(data.food_names);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        } else {
            suggestionsList.innerHTML = '';
            dataDisplay.innerHTML = '';
        }
    });

    function displaySuggestions(foodNames) {
        suggestionsList.innerHTML = '';
        if (foodNames.length > 0) {
            foodNames.forEach(name => {
                const suggestionItem = document.createElement('li');
                suggestionItem.textContent = name;
                suggestionItem.addEventListener('click', function () {
                    searchBar.value = name;
                    fetchFoodDetails(name);
                    suggestionsList.innerHTML = ''; // Clear suggestions when an item is clicked
                });
                suggestionsList.appendChild(suggestionItem);
            });
        }
    }

    function fetchFoodDetails(foodName) {
        fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({ 'query': foodName })
        })
        .then(response => response.json())
        .then(data => {
            displayResults(data.results);
            suggestionsList.innerHTML = ''; // Clear suggestions after fetching details
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    function displayResults(results) {
        if (results === "Error: Unable to retrieve search results") {
            dataDisplay.innerHTML = '<p>Error retrieving results</p>';
            return;
        }

        let tableContent = `
            <div class='scrollable-table'>
                <table class='table_style'>
                    <thead>
                        <tr>
                            <th class='food_header'>${results.Name}</th>
                            <th class='nutrient_header'>Nutrients</th>
                        </tr>
                    </thead>
                    <tbody>
        `;

        results.Nutrients.forEach(nutrient => {
            tableContent += `
                <tr>
                    <td>${nutrient.name}</td>
                    <td>${nutrient.value} ${nutrient.unit}</td>
                </tr>
            `;
        });

        tableContent += `
                    </tbody>
                </table>
            </div>
            <button class='add_item' type='button'>Add To List</button>
            <button class='mylist' type='button'>My List</button>
        `;

        dataDisplay.innerHTML = tableContent;

        const addButton = document.querySelector('.add_item');
        addButton.addEventListener('click', () => {
            if (!(ItemList.includes((results.Name,results.Nutrients)))){
                ItemList.push((results.Name,results.Nutrients));
            }
            
        });
    }
});
