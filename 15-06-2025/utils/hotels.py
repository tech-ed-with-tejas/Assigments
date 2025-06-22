from langchain_community.tools import DuckDuckGoSearchResults
search=DuckDuckGoSearchResults(output_format="list")
from langchain.tools import tool

@tool
def search_hotels(location):
    """
    Input:
        location (str): The name of the location where hotels need to be searched.
    Output:
        results (list): A list of dictionaries containing information about famous hotels
                        in the specified location and their average cost per day or night stay.
    Description:
        This function takes a location as input, constructs a query to search for famous hotels
        in that location along with their average cost, and returns the search results.
    """
    query = f"famous hotels in {location} and their average cost per day or per night stay"
    results = search.invoke(query)
    ouput =''
    for i in results:
        ouput += i['snippet'] +"\n\n" 
    return ouput

