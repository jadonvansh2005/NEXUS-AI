# """
# UPSS Tool Registration

# Responsibilities

# - Register every available tool
# - Populate ToolRegistry
# - Single registration entry point

# Notes

# - No execution logic
# - No discovery logic
# - No provider selection logic
# """

# from __future__ import annotations

# from agents.core.tool_registry import ToolRegistry

# from tools.travel.flight_search_tool import FlightSearchTool
# from tools.travel.hotel_search_tool import HotelSearchTool
# from tools.travel.train_search_tool import TrainSearchTool
# from tools.travel.booking_tool import BookingTool
# from tools.travel.fare_estimator_tool import FareEstimatorTool
# from tools.travel.price_compare_tool import PriceCompareTool
# from tools.travel.flight_cancellation_tool import FlightCancellationTool
# from tools.travel.hotel_cancellation_tool import HotelCancellationTool
# from tools.travel.train_cancellation_tool import TrainCancellationTool
# from tools.travel.itinerary_tool import ItineraryTool
# from tools.travel.budget_tool import BudgetTool
# from tools.travel.currency_converter_tool import CurrencyConverterTool
# from tools.travel.nearby_places_tool import NearbyPlacesTool
# from tools.travel.packing_list_tool import PackingListTool
# from tools.travel.trip_summary_tool import TripSummaryTool
# from tools.travel.visa_tool import VisaTool


# class ToolCatalog:

#     """
#     Registers every UPSS tool.
#     """

#     def __init__(

#         self,

#         registry: ToolRegistry,

#     ):

#         self.registry = registry

#     # =====================================================
#     # Register All
#     # =====================================================

#     def register_all(

#         self,

#     ) -> None:

#         #
#         # Travel
#         #

#         self._register_travel()

#         #
#         # Communication
#         #

#         self._register_communication()

#         #
#         # Coding
#         #

#         self._register_coding()

#         #
#         # Finance
#         #

#         self._register_finance()

#         #
#         # Research
#         #

#         self._register_research()

#         #
#         # Browser
#         #

#         self._register_browser()

#         #
#         # Filesystem
#         #

#         self._register_filesystem()

#         #
#         # Database
#         #

#         self._register_database()

#         #
#         # Calendar
#         #

#         self._register_calendar()

#         #
#         # Email
#         #

#         self._register_email()

#         #
#         # Documents
#         #

#         self._register_documents()

#     # =====================================================
#     # Registration Groups
#     # =====================================================

#     def _register_travel(self):
#         pass

#     def _register_communication(self):
#         pass

#     def _register_coding(self):
#         pass

#     def _register_finance(self):
#         pass

#     def _register_research(self):
#         pass

#     def _register_browser(self):
#         pass

#     def _register_filesystem(self):
#         pass

#     def _register_database(self):
#         pass

#     def _register_calendar(self):
#         pass

#     def _register_email(self):
#         pass

#     def _register_documents(self):
#         pass