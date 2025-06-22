from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Literal
from datetime import datetime
from datetime import datetime, time
from typing import Sequence, Annotated, TypedDict

from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
class UserPlan(BaseModel):
    class Config:
        arbitrary_types_allowed = True
    date: datetime = Field(..., description="The date of the travel plan in YYYY-MM-DD format")
    time: str = Field(..., description="The time of the travel plan in HH:MM format")


class DestinationValidator(BaseModel):
    international: bool = Field(..., description="Indicates if the travel plan is international")
    single_country: bool = Field(..., description="Indicates if the travel plan is limited to a single country")
    within_country: bool = Field(..., description="Indicates if the travel plan is within the same country")
    place_names: List[str] = Field(..., description="List of specific place names for the travel plan")
    country_names: Optional[List[str]] = Field(default=None, description="The name(s) of the country for the travel plan")
    city_names: Optional[List[str]] = Field(default=None, description="The name(s) of the city for the travel plan")

    @model_validator(mode="after")
    def validate_destination_flags(self):
        international = self.international
        single_country = self.single_country
        within_country = self.within_country
        countries = self.country_names

        if international and within_country:
            raise ValueError("A plan cannot be both international and within-country.")
        if international and single_country and countries and len(countries) != 1:
            raise ValueError("Single-country international plans should only have one country.")
        return self


class AgentRequirement(BaseModel):
    """It contains all the requirements needed to manage the travel plan."""
    class Config:
        arbitrary_types_allowed = True
    travel_start_date: datetime = Field(..., description="The start date of the travel plan in YYYY-MM-DD format")
    travel_end_date: datetime = Field(..., description="The end date of the travel plan in YYYY-MM-DD format")
    travel_destination: str = Field(..., description="The destination for the travel plan")
    travel_budget_lower_limit: float = Field(..., description="The lower limit of the travel budget in the specified currency")
    travel_budget_upper_limit: float = Field(..., description="The upper limit of the travel budget in the specified currency")
    travel_place_type: List[str] = Field(..., description="List of places to visit at the travel destination")
    user_plans_if_exists: Optional[List[UserPlan]] = Field(default=None, description="List of slots that user has already planned")
    travel_with_specific_airline: List[str] = Field(default=["any"], description="List of airline names that user prefers to travel with")
    destination: DestinationValidator = Field(..., description="Destination validator to check the destination of the travel plan")

    # Added Fields
    accommodation_preference: Optional[List[Literal["Hotel", "Hostel", "Airbnb", "Resort", "Guesthouse"]]] = Field(
        default=None, description="Preferred types of accommodation"
    )
    meal_preferences: Optional[List[str]] = Field(
        default=None, description="Any dietary restrictions or meal preferences"
    )
    transport_preferences: Optional[List[Literal["Train", "Bus", "Flight", "Rental Car", "Boat", "Bicycle"]]] = Field(
        default=None, description="Preferred modes of transport during the trip"
    )
    activities_or_experiences: Optional[List[str]] = Field(
        default=None, description="List of activities or experiences the user wants to try"
    )
    number_of_travelers: int = Field(..., description="Total number of people traveling")
    age_groups: Optional[List[str]] = Field(
        default=None,
        description="Age groups of travelers (e.g., 'children', 'teenagers', 'adults', 'seniors')"
    )

    @model_validator(mode="after")
    def check_dates_and_budget(self):
        if self.travel_start_date >= self.travel_end_date:
            raise ValueError("Travel start date must be before end date")
        if self.travel_budget_lower_limit > self.travel_budget_upper_limit:
            raise ValueError("Lower budget limit cannot be higher than upper budget limit")
        return self





if __name__ == "__main__":
  
    
    print(AgentRequirement.model_json_schema())
    # Example 1: Domestic travel with specific preferences
    example_1 = AgentRequirement(
        
        travel_start_date=datetime(2025, 6, 20),
        travel_end_date=datetime(2025, 6, 30),
        travel_destination="New York",
        travel_budget_lower_limit=1000.0,
        travel_budget_upper_limit=5000.0,
        travel_place_type=["Museum", "Park", "Theater"],
        user_plans_if_exists=None,
        travel_with_specific_airline=["Delta Airlines"],
        destination=DestinationValidator(
            international=False,
            single_country=True,
            within_country=True,
            place_names=["Central Park", "Times Square"],
            country_names=["USA"],
            city_names=["New York"]
        ),
        accommodation_preference=["Hotel", "Airbnb"],
        meal_preferences=["Vegetarian"],
        transport_preferences=["Train", "Bus"],
        activities_or_experiences=["Broadway Show", "City Tour"],
        number_of_travelers=2,
        age_groups=["adults"]
    )

    # Example 2: International travel with a single country
    example_2 = AgentRequirement(
        travel_start_date=datetime(2025, 7, 1),
        travel_end_date=datetime(2025, 7, 15),
        travel_destination="Paris",
        travel_budget_lower_limit=2000.0,
        travel_budget_upper_limit=10000.0,
        travel_place_type=["Landmark", "Museum"],
        user_plans_if_exists=None,
        travel_with_specific_airline=["Air France"],
        destination=DestinationValidator(
            international=True,
            single_country=True,
            within_country=False,
            place_names=["Eiffel Tower", "Louvre Museum"],
            country_names=["France"],
            city_names=["Paris"]
        ),
        accommodation_preference=["Hotel", "Resort"],
        meal_preferences=["Gluten-Free"],
        transport_preferences=["Flight", "Bicycle"],
        activities_or_experiences=["Wine Tasting", "River Cruise"],
        number_of_travelers=4,
        age_groups=["adults", "teenagers"]
    )

    # Example 3: Multi-country international travel
    example_3 = AgentRequirement(
        travel_start_date=datetime(2025, 8, 10),
        travel_end_date=datetime(2025, 8, 25),
        travel_destination="Europe",
        travel_budget_lower_limit=3000.0,
        travel_budget_upper_limit=15000.0,
        travel_place_type=["Historical Site", "Beach"],
        user_plans_if_exists=None,
        travel_with_specific_airline=["Lufthansa", "British Airways"],
        destination=DestinationValidator(
            international=True,
            single_country=False,
            within_country=False,
            place_names=["Colosseum", "Santorini"],
            country_names=["Italy", "Greece"],
            city_names=["Rome", "Santorini"]
        ),
        accommodation_preference=["Resort", "Guesthouse"],
        meal_preferences=["Vegan"],
        transport_preferences=["Flight", "Boat"],
        activities_or_experiences=["Scuba Diving", "Historical Tour"],
        number_of_travelers=6,
        age_groups=["adults", "seniors"]
    )

    # Example 4: Domestic travel with family
    example_4 = AgentRequirement(
        travel_start_date=datetime(2025, 12, 20),
        travel_end_date=datetime(2025, 12, 27),
        travel_destination="Florida",
        travel_budget_lower_limit=1500.0,
        travel_budget_upper_limit=7000.0,
        travel_place_type=["Theme Park", "Beach"],
        user_plans_if_exists=None,
        travel_with_specific_airline=["any"],
        destination=DestinationValidator(
            international=False,
            single_country=True,
            within_country=True,
            place_names=["Disney World", "Miami Beach"],
            country_names=["USA"],
            city_names=["Orlando", "Miami"]
        ),
        accommodation_preference=["Resort", "Hotel"],
        meal_preferences=["No Pork"],
        transport_preferences=["Rental Car"],
        activities_or_experiences=["Theme Park Visit", "Beach Relaxation"],
        number_of_travelers=5,
        age_groups=["children", "adults"]
    )


    # Example 5: Invalid travel dates
    invalid_example_1 = {
        "travel_start_date": datetime(2025, 8, 25),
        "travel_end_date": datetime(2025, 8, 10),
        "travel_destination": "Europe",
        "travel_budget_lower_limit": 3000.0,
        "travel_budget_upper_limit": 15000.0,
        "travel_place_type": ["Historical Site", "Beach"],
        "user_plans_if_exists": None,
        "travel_with_specific_airline": ["Lufthansa", "British Airways"],
        "destination": {
            "international": True,
            "single_country": False,
            "within_country": False,
            "place_names": ["Colosseum", "Santorini"],
            "country_names": ["Italy", "Greece"],
            "city_names": ["Rome", "Santorini"]
        },
        "accommodation_preference": ["Resort", "Guesthouse"],
        "meal_preferences": ["Vegan"],
        "transport_preferences": ["Flight", "Boat"],
        "activities_or_experiences": ["Scuba Diving", "Historical Tour"],
        "number_of_travelers": 6,
        "age_groups": ["adults", "seniors"]
    }

    # Example 6: Invalid budget limits
    invalid_example_2 = {
        "travel_start_date": datetime(2025, 9, 1),
        "travel_end_date": datetime(2025, 9, 15),
        "travel_destination": "Paris",
        "travel_budget_lower_limit": 12000.0,
        "travel_budget_upper_limit": 10000.0,
        "travel_place_type": ["Landmark", "Museum"],
        "user_plans_if_exists": None,
        "travel_with_specific_airline": ["Air France"],
        "destination": {
            "international": True,
            "single_country": True,
            "within_country": False,
            "place_names": ["Eiffel Tower", "Louvre Museum"],
            "country_names": ["France"],
            "city_names": ["Paris"]
        },
        "accommodation_preference": ["Hotel", "Resort"],
        "meal_preferences": ["Gluten-Free"],
        "transport_preferences": ["Flight", "Bicycle"],
        "activities_or_experiences": ["Wine Tasting", "River Cruise"],
        "number_of_travelers": 4,
        "age_groups": ["adults", "teenagers"]
    }

    # Example 7: Invalid destination flags
    invalid_example_3 = {
        "travel_start_date": datetime(2025, 10, 1),
        "travel_end_date": datetime(2025, 10, 15),
        "travel_destination": "New York",
        "travel_budget_lower_limit": 2000.0,
        "travel_budget_upper_limit": 8000.0,
        "travel_place_type": ["Museum", "Park"],
        "user_plans_if_exists": None,
        "travel_with_specific_airline": ["Delta Airlines"],
        "destination": {
            "international": True,
            "single_country": True,
            "within_country": True,
            "place_names": ["Central Park", "Times Square"],
            "country_names": ["USA"],
            "city_names": ["New York"]
        },
        "accommodation_preference": ["Hotel", "Airbnb"],
        "meal_preferences": ["Vegetarian"],
        "transport_preferences": ["Train", "Bus"],
        "activities_or_experiences": ["Broadway Show", "City Tour"],
        "number_of_travelers": 2,
        "age_groups": ["adults"]
    }

    # Validate examples with errors
    # print("Validation for Example 5:")
    # print(handle_validation_error(invalid_example_1))
    # print("\nValidation for Example 6:")
    # print(handle_validation_error(invalid_example_2))
    # print("\nValidation for Example 7:")
    # print(handle_validation_error(invalid_example_3))
    # # Convert examples to JSON strings and print them
    # print("Example 1 JSON:")
    # print(example_1.model_dump_json(indent=2))
    # print("\nExample 2 JSON:")
    # print(example_2.model_dump_json(indent=2))
    # print("\nExample 3 JSON:")
    # print(example_3.model_dump_json(indent=2))
    # print("\nExample 4 JSON:")
    # print(example_4.model_dump_json(indent=2))