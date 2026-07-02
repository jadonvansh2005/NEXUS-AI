from agents.core.tool_registry import ToolRegistry

from tools.ds_tools.dataset_analyzer import DatasetAnalyzer
from tools.travel.itinerary_tool import ItineraryTool
from tools.travel.train_search_tool import TrainSearchTool
from tools.travel.hotel_search_tool import HotelSearchTool
from tools.travel.flight_search_tool import FlightSearchTool

registry = ToolRegistry()

# 1. Dataset Analyzer Tool (Data Science)
registry.register_tool(
    name="dataset_analyzer",
    tool=DatasetAnalyzer(),
    domain="data_science",
    capabilities=["dataset_analysis"],
    providers=["generic"]
)

# 2. Itinerary Generator Tool (Travel)
registry.register_tool(
    name="travel.itinerary",
    tool=ItineraryTool(),
    domain="travel",
    capabilities=["itinerary_generation"],
    providers=["generic"]
)

# 3. Train Search & Booking Tool (Travel)
registry.register_tool(
    name="travel.trains",
    tool=TrainSearchTool(),
    domain="travel",
    capabilities=["train_search", "booking"],
    providers=["irctc"]
)

# 4. Hotel Search Tool (Travel)
registry.register_tool(
    name="travel.hotels",
    tool=HotelSearchTool(),
    domain="travel",
    capabilities=["hotel_search"],
    providers=["generic"]
)

# 5. Flight Search Tool (Travel)
registry.register_tool(
    name="travel.flights",
    tool=FlightSearchTool(),
    domain="travel",
    capabilities=["flight_search"],
    providers=["generic"]
)