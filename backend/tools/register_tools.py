from agents.core.tool_registry import ToolRegistry

from tools.ds_tools.dataset_analyzer import DatasetAnalyzer
from tools.travel.itinerary_tool import ItineraryTool
from tools.travel.train_search_tool import TrainSearchTool
from tools.travel.hotel_search_tool import HotelSearchTool
from tools.travel.flight_search_tool import FlightSearchTool
from tools.browser.webpage_reader_tool import WebPageReaderTool
from tools.search.web_search_tool import WebSearchTool
from tools.coding.code_generator_tool import CodeGeneratorTool
from tools.coding.code_reviewer_tool import CodeReviewerTool
from tools.coding.code_explainer_tool import CodeExplainerTool
from tools.calculator.calculator_tool import CalculatorTool
from tools.weather.current_weather_tool import CurrentWeatherTool
from tools.weather.air_quality_tool import AirQualityTool
from tools.weather.alerts_tool import AlertsTool
from tools.weather.forecast_tool import ForecastTool
from tools.maps.distance_tool import DistanceTool
from tools.maps.geocode_tool import GeocodeTool
from tools.maps.navigation_tool import NavigationTool
from tools.maps.nearby_places_tool import NearbyPlacesTool
from tools.maps.route_tool import RouteTool
from tools.email.send_email_tool import SendEmailTool
from tools.email.read_email_tool import ReadEmailTool
from tools.email.search_email_tool import SearchEmailTool
from tools.email.draft_email_tool import DraftEmailTool
from tools.email.attachment_tool import AttachmentTool

# GitHub imports
from tools.github.clone_repo_tool import CloneRepositoryTool
from tools.github.commit_tool import CommitTool
from tools.github.push_tool import PushTool
from tools.github.repo_search_tool import RepositorySearchTool
from tools.github.create_pr_tool import CreatePullRequestTool
from tools.github.issue_tool import IssueTool

# Coding imports
from tools.coding.bug_fixer_tool import BugFixTool
from tools.coding.debugger_tool import DebuggerTool
from tools.coding.dependency_analyzer_tool import DependencyAnalyzerTool
from tools.coding.documentation_tool import DocumentationTool
from tools.coding.git_assistant_tool import GitAssistantTool
from tools.coding.project_generator_tool import ProjectGeneratorTool
from tools.coding.refactor_tool import RefactorTool
from tools.coding.test_generator_tool import TestGeneratorTool

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

# 6. Webpage Reader Tool (Research / Browser)
registry.register_tool(
    name="browser.reader",
    tool=WebPageReaderTool(),
    domain="research",
    capabilities=["read_webpage"],
    providers=["generic"]
)

# 7. Web Search Tool (Research / Search)
registry.register_tool(
    name="search.web",
    tool=WebSearchTool(),
    domain="research",
    capabilities=["web_search"],
    providers=["generic"]
)

# 8. Code Generator Tool (Coding)
registry.register_tool(
    name="coding.code_generator",
    tool=CodeGeneratorTool(),
    domain="coding",
    capabilities=["generate_code"],
    providers=["generic"]
)

# 9. Code Reviewer Tool (Coding)
registry.register_tool(
    name="coding.code_reviewer",
    tool=CodeReviewerTool(),
    domain="coding",
    capabilities=["review_code"],
    providers=["generic"]
)

# 10. Code Explainer Tool (Coding)
registry.register_tool(
    name="coding.code_explainer",
    tool=CodeExplainerTool(),
    domain="coding",
    capabilities=["explain_code"],
    providers=["generic"]
)

# 11. Calculator Tool (General)
registry.register_tool(
    name="calculator.calculate",
    tool=CalculatorTool(),
    domain="general",
    capabilities=["calculator"],
    providers=["generic"]
)

# 12. Weather Tool (General)
registry.register_tool(
    name="weather.current",
    tool=CurrentWeatherTool(),
    domain="general",
    capabilities=["current_weather"],
    providers=["generic"]
)

# 12a. Air Quality Tool (General)
registry.register_tool(
    name="weather.air_quality",
    tool=AirQualityTool(),
    domain="general",
    capabilities=["air_quality"],
    providers=["generic"]
)

# 12b. Weather Alerts Tool (General)
registry.register_tool(
    name="weather.alerts",
    tool=AlertsTool(),
    domain="general",
    capabilities=["weather_alerts"],
    providers=["generic"]
)

# 12c. Weather Forecast Tool (General)
registry.register_tool(
    name="weather.forecast",
    tool=ForecastTool(),
    domain="general",
    capabilities=["weather_forecast"],
    providers=["generic"]
)

# 13. Distance Tool (General)
registry.register_tool(
    name="maps.distance",
    tool=DistanceTool(),
    domain="general",
    capabilities=["map_navigation"],
    providers=["generic"]
)

# 13a. Geocode Tool (General)
registry.register_tool(
    name="maps.geocode",
    tool=GeocodeTool(),
    domain="general",
    capabilities=["geocode"],
    providers=["generic"]
)

# 13b. Navigation Tool (General)
registry.register_tool(
    name="maps.navigation",
    tool=NavigationTool(),
    domain="general",
    capabilities=["navigation"],
    providers=["generic"]
)

# 13c. Nearby Places Tool (General)
registry.register_tool(
    name="maps.nearby_places",
    tool=NearbyPlacesTool(),
    domain="general",
    capabilities=["nearby_places"],
    providers=["generic"]
)

# 13d. Route Tool (General)
registry.register_tool(
    name="maps.route",
    tool=RouteTool(),
    domain="general",
    capabilities=["route"],
    providers=["generic"]
)

# 14. Send Email Tool (Communication)
registry.register_tool(
    name="email.send",
    tool=SendEmailTool(),
    domain="communication",
    capabilities=["send_email"],
    providers=["generic"]
)

# 15. Read Email Tool (Communication)
registry.register_tool(
    name="email.read",
    tool=ReadEmailTool(),
    domain="communication",
    capabilities=["read_email"],
    providers=["generic"]
)

# 16. Search Email Tool (Communication)
registry.register_tool(
    name="email.search",
    tool=SearchEmailTool(),
    domain="communication",
    capabilities=["search_email"],
    providers=["generic"]
)

# 17. Draft Email Tool (Communication)
registry.register_tool(
    name="email.draft",
    tool=DraftEmailTool(),
    domain="communication",
    capabilities=["draft_email"],
    providers=["generic"]
)

# 18. Attachment Tool (Communication)
registry.register_tool(
    name="email.attachment",
    tool=AttachmentTool(),
    domain="communication",
    capabilities=["download_attachments"],
    providers=["generic"]
)

# ==========================================================
# GitHub Tools Registrations
# ==========================================================

registry.register_tool(
    name="github.clone",
    tool=CloneRepositoryTool(),
    domain="coding",
    capabilities=["clone_repo"],
    providers=["generic"]
)

registry.register_tool(
    name="github.commit",
    tool=CommitTool(),
    domain="coding",
    capabilities=["commit_changes"],
    providers=["generic"]
)

registry.register_tool(
    name="github.push",
    tool=PushTool(),
    domain="coding",
    capabilities=["push_changes"],
    providers=["generic"]
)

registry.register_tool(
    name="github.search",
    tool=RepositorySearchTool(),
    domain="coding",
    capabilities=["search_repositories"],
    providers=["generic"]
)

registry.register_tool(
    name="github.pull_request",
    tool=CreatePullRequestTool(),
    domain="coding",
    capabilities=["create_pr"],
    providers=["generic"]
)

registry.register_tool(
    name="github.issue",
    tool=IssueTool(),
    domain="coding",
    capabilities=["create_issue"],
    providers=["generic"]
)

# ==========================================================
# Remaining Coding Tools Registrations
# ==========================================================

registry.register_tool(
    name="coding.bug_fixer",
    tool=BugFixTool(),
    domain="coding",
    capabilities=["fix_bugs"],
    providers=["generic"]
)

registry.register_tool(
    name="coding.debugger",
    tool=DebuggerTool(),
    domain="coding",
    capabilities=["debug_code"],
    providers=["generic"]
)

registry.register_tool(
    name="coding.dependency_analyzer",
    tool=DependencyAnalyzerTool(),
    domain="coding",
    capabilities=["analyze_dependencies"],
    providers=["generic"]
)

registry.register_tool(
    name="coding.documentation",
    tool=DocumentationTool(),
    domain="coding",
    capabilities=["generate_documentation"],
    providers=["generic"]
)

registry.register_tool(
    name="coding.git_assistant",
    tool=GitAssistantTool(),
    domain="coding",
    capabilities=["git_assistance"],
    providers=["generic"]
)

registry.register_tool(
    name="coding.project_generator",
    tool=ProjectGeneratorTool(),
    domain="coding",
    capabilities=["generate_project"],
    providers=["generic"]
)

registry.register_tool(
    name="coding.refactor",
    tool=RefactorTool(),
    domain="coding",
    capabilities=["refactor_code"],
    providers=["generic"]
)

registry.register_tool(
    name="coding.test_generator",
    tool=TestGeneratorTool(),
    domain="coding",
    capabilities=["generate_tests"],
    providers=["generic"]
)