
Assignment:
    
AI Travel Agent & Expense Planner(Purpose: Trip planning for any city worldwide with Realtime data.")

• Real-time weather information
• Top attractions and activities
• Hotel cost calculation (per day × total days)
• Currency conversion to user's native currency
• Complete itinerary generation
• Total expense calculation
• generate a summary of the entire output
user_input
  |
search attraction and activity
1. search attracation
2. search restaurant
3. search activity
4. search transportation
  |
search weather forcasting
1. get current weather
2. get weather forcast
  |
search hotel costs
1. search hotel
2. estimate the hotel cost
3. budget_range
  |
calculate total cost
1. add
2. multiply
3. calculated total cost
4. calcualte the daily budget
    | 
currency_converion
1. get exchnage rate
2. convert currancy
    | 
Itinery generation (agnet)
1. get day plan
2. crete full itinery
    |
create Trip Summary
    |
Retun complete traval plan

Note: if you know the OOPS then design this entire system using object and class in modular fashion.


deadline is till next friday 9PM IST


 everyone you can submit the assignments in this form. MAke sure to have one GitHub link and put all the assignments there https://forms.gle/g8RZ4qx8yvNcih4B7


 Okay, here's a point-by-point breakdown of how you can leverage **Amadeus Self-Service Travel APIs** to gather the necessary data for your "AI Travel Agent & Expense Planner," specifically for hotels, flights, and activities.

This focuses on *getting the data* for planning, rather than direct booking.

---

### Leveraging Amadeus APIs for Your Travel Agent & Expense Planner

You'll primarily use Amadeus **Self-Service APIs** for data retrieval.

#### 1. Hotel Cost Calculation (per day × total days)

* **Amadeus API:** **Hotel Offers Search** (`/v2/shopping/hotel-offers`)
* **What it provides:**
    * Search for hotels by city code, geographical coordinates, or hotel ID.
    * Filter by check-in/check-out dates, number of guests, number of rooms.
    * Returns available room types, rates (per night), and total prices.
    * Includes basic hotel information like name, address, and star rating.
* **How you'll use it:**
    * Pass the destination city's geocode (obtained from Google Places Geocoding or Amadeus's own City Search) and trip dates.
    * Retrieve a list of hotels with their daily rates.
    * Your application's logic will then:
        * Filter/select hotels based on the user's `daily_budget_usd`.
        * Calculate `cost_per_day × total_days` using the rates provided by the API.
        * Store selected hotel details in your `HotelBooking` data model.

#### 2. Flight Data

* **Amadeus API:** **Flight Offers Search** (`/v2/shopping/flight-offers`)
* **What it provides:**
    * Search for the most cost-effective and relevant flight options.
    * Specify origin, destination, departure/return dates, number of passengers.
    * Returns flight segments, airlines, durations, and total prices.
* **Amadeus API:** **Airport & City Search** (`/v1/reference-data/locations`)
* **What it provides:**
    * Search for airports and cities by keyword.
    * Returns IATA codes, names, and geographical coordinates.
* **How you'll use it:**
    * **Before Flight Search:** Use **Airport & City Search** to validate user-provided origin/destination cities and get their respective IATA airport codes, which are required for flight searches.
    * **Flight Search:** Pass the origin/destination IATA codes and dates to **Flight Offers Search**.
    * Retrieve potential flight itineraries and their costs.
    * Your application's logic will then:
        * Suggest suitable flight options based on price, travel time, and number of layovers.
        * Factor flight costs into the `Total Expense Calculation`.

#### 3. Top Attractions and Activities

* **Amadeus API:** **Activities** (`/v1/shopping/activities`) or **Points of Interest** (`/v1/reference-data/locations/pois`)
* **What it provides:**
    * Search for tours, activities, and points of interest around a geographical location (latitude/longitude).
    * Returns details like name, category, description, website, and sometimes price range or booking links.
* **How you'll use it:**
    * Pass the destination's latitude/longitude (obtained from Google Geocoding or Amadeus City Search).
    * Retrieve a list of popular attractions and available activities in the area.
    * Your application's logic will then:
        * Filter these based on user interests (`Art, Museums, Romantic Dinners`).
        * Integrate them into the `Itinerary Generation`.
        * Estimate costs for these activities where available (Amadeus may provide prices for bookable activities).

---

### Important Considerations:

* **API Keys:** You will need a separate API key for Amadeus for Developers. Set it as an environment variable (e.g., `AMADEUS_API_KEY`).
* **Authentication:** Amadeus Self-Service APIs typically use an OAuth 2.0 client credentials flow (API Key + API Secret to get an access token). Your service class will need to handle obtaining and refreshing this token.
* **Pricing & Quotas:** Review Amadeus's pricing and free tier quotas carefully. Extensive real-time searching can quickly consume free limits.
* **Data Models:** Ensure your Python `dataclass` models (`FlightOffer`, `HotelDetails`, `Activity`) are robust enough to store all relevant information you get from Amadeus APIs.
* **Itinerary Generation Logic:** While Amadeus provides the raw data, the *intelligence* to combine flights, hotels, activities into a coherent, personalized, daily itinerary that respects budget and time constraints will be primarily handled by your **LLM** (as discussed in the prompt engineering). Amadeus feeds the LLM with the necessary real-time inventory information.