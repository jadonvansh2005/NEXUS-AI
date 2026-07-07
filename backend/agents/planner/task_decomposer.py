"""
Task Decomposer

Responsibilities

- Break a user goal into executable tasks.
- Create logical workflow tasks.
- Do NOT select tools.
"""

from __future__ import annotations

from typing import List

from agents.planner.schemas import PlannerTask


class TaskDecomposer:

    def decompose(
        self,
        query: str,
        domain: str,
    ) -> List[PlannerTask]:

        if domain == "data_science":

            return [

                PlannerTask(
                    id="task_1",
                    name="Load Dataset",
                    description="Load the dataset for analysis."
                ),

                PlannerTask(
                    id="task_2",
                    name="Perform EDA",
                    description="Analyze dataset statistics.",
                    depends_on=["task_1"]
                ),

                PlannerTask(
                    id="task_3",
                    name="Train Model",
                    description="Train machine learning model.",
                    depends_on=["task_2"]
                ),

                PlannerTask(
                    id="task_4",
                    name="Evaluate Model",
                    description="Evaluate model performance.",
                    depends_on=["task_3"]
                ),

                PlannerTask(
                    id="task_5",
                    name="Generate Report",
                    description="Generate final report.",
                    depends_on=["task_4"]
                )

            ]

        elif domain == "travel":
            q_lower = query.lower()
            if "flight" in q_lower or "air" in q_lower:
                return [
                    PlannerTask(
                        id="task_1",
                        name="Search Flights",
                        description="Search for flights between origin and destination.",
                        tool="travel.flights"
                    )
                ]
            elif "hotel" in q_lower or "stay" in q_lower or "room" in q_lower:
                return [
                    PlannerTask(
                        id="task_1",
                        name="Search Hotels",
                        description="Search for hotels at the destination.",
                        tool="travel.hotels"
                    )
                ]
            elif "train" in q_lower or "rail" in q_lower:
                return [
                    PlannerTask(
                        id="task_1",
                        name="Search Trains",
                        description="Search for trains between origin and destination.",
                        tool="travel.trains"
                    )
                ]
            else:
                return [

                    PlannerTask(
                        id="task_1",
                        name="Get Destination",
                        description="Understand destination."
                    ),

                    PlannerTask(
                        id="task_2",
                        name="Collect Travel Requirements",
                        description="Collect travel preferences.",
                        depends_on=["task_1"]
                    ),

                    PlannerTask(
                        id="task_3",
                        name="Search Travel Options",
                        description="Search flights, hotels and transport.",
                        tool="travel.itinerary",
                        depends_on=["task_2"]
                    )

                ]

        elif domain == "career":

            return [

                PlannerTask(
                    id="task_1",
                    name="Analyze Resume",
                    description="Review uploaded resume."
                ),

                PlannerTask(
                    id="task_2",
                    name="Evaluate ATS",
                    description="Calculate ATS score.",
                    depends_on=["task_1"]
                ),

                PlannerTask(
                    id="task_3",
                    name="Suggest Improvements",
                    description="Recommend resume improvements.",
                    depends_on=["task_2"]
                ),

                PlannerTask(
                    id="task_4",
                    name="Recommend Jobs",
                    description="Find matching opportunities.",
                    depends_on=["task_3"]
                )

            ]

        elif domain == "coding":
            import re
            q_lower = re.sub(r'\[workspace:\s*.+?\]', '', query).lower()
            
            # 1. Search Repositories (Check this before generic Git pushes to prevent overriding search queries)
            if "search" in q_lower or "find" in q_lower:
                return [
                    PlannerTask(
                        id="task_1",
                        name="Search Repositories",
                        description="Search repositories on GitHub."
                    )
                ]
                
            # Git & GitHub workflows
            if any(w in q_lower for w in ["push", "upload", "publish", "github", "git"]):
                if "clone" in q_lower:
                    return [
                        PlannerTask(
                            id="task_1",
                            name="Clone Repository",
                            description="Clone repository from GitHub."
                        )
                    ]
                elif "commit" in q_lower:
                    return [
                        PlannerTask(
                            id="task_1",
                            name="Git Commit",
                            description="Create local git commit."
                        )
                    ]
                elif "pull request" in q_lower or "pr" in q_lower:
                    return [
                        PlannerTask(
                            id="task_1",
                            name="Create Pull Request",
                            description="Create Pull Request on GitHub."
                        )
                    ]
                elif "issue" in q_lower:
                    return [
                        PlannerTask(
                            id="task_1",
                            name="Create GitHub Issue",
                            description="Create issue on GitHub."
                        )
                    ]
                else:
                    # Upload to GitHub / Push workflow
                    return [
                        PlannerTask(
                            id="task_1",
                            name="Git Commit",
                            description="Commit local workspace changes."
                        ),
                        PlannerTask(
                            id="task_2",
                            name="Git Push",
                            description="Push committed files to GitHub remote repository.",
                            depends_on=["task_1"]
                        )
                    ]
            
            # Project Generator
            if "project" in q_lower or "boilerplate" in q_lower:
                return [
                    PlannerTask(
                        id="task_1",
                        name="Generate Project",
                        description="Generate standard boilerplate project structures."
                    )
                ]
                
            # Dependency Analyzer
            if "dependency" in q_lower or "package" in q_lower or "imports" in q_lower:
                return [
                    PlannerTask(
                        id="task_1",
                        name="Analyze Dependencies",
                        description="Analyze codebase import dependencies."
                    )
                ]

            # Bug Fixer
            if "bug" in q_lower or "fix" in q_lower:
                return [
                    PlannerTask(
                        id="task_1",
                        name="Fix Bugs",
                        description="Generate code bug fixes for errors."
                    )
                ]

            # Debugger
            if "debug" in q_lower or "trace" in q_lower:
                return [
                    PlannerTask(
                        id="task_1",
                        name="Debug Code",
                        description="Analyze and debug execution runtime errors."
                    )
                ]

            # Refactor
            if "refactor" in q_lower or "clean" in q_lower:
                return [
                    PlannerTask(
                        id="task_1",
                        name="Refactor Code",
                        description="Improve code design structure."
                    )
                ]

            # Test Generator
            if "test" in q_lower or "unit test" in q_lower:
                return [
                    PlannerTask(
                        id="task_1",
                        name="Generate Tests",
                        description="Generate automated test cases."
                    )
                ]

            # Documentation
            if "doc" in q_lower or "comment" in q_lower or "readme" in q_lower:
                return [
                    PlannerTask(
                        id="task_1",
                        name="Generate Documentation",
                        description="Generate developer guides or inline documentation."
                    )
                ]
                
            # Explainer
            if "explain" in q_lower:
                return [
                    PlannerTask(
                        id="task_1",
                        name="Explain Solution",
                        description="Explain code structure."
                    )
                ]


            # Default: generate code
            return [
                PlannerTask(
                    id="task_1",
                    name="Generate Solution",
                    description="Generate clean source code."
                )
            ]

        elif domain == "education":

            return [

                PlannerTask(
                    id="task_1",
                    name="Understand Learning Goal",
                    description="Understand study objective."
                ),

                PlannerTask(
                    id="task_2",
                    name="Collect Learning Resources",
                    description="Collect relevant material.",
                    depends_on=["task_1"]
                ),

                PlannerTask(
                    id="task_3",
                    name="Generate Study Plan",
                    description="Prepare study roadmap.",
                    depends_on=["task_2"]
                )

            ]

        elif domain == "finance":

            return [

                PlannerTask(
                    id="task_1",
                    name="Collect Financial Information",
                    description="Understand financial request."
                ),

                PlannerTask(
                    id="task_2",
                    name="Analyze Financial Data",
                    description="Analyze financial information.",
                    depends_on=["task_1"]
                ),

                PlannerTask(
                    id="task_3",
                    name="Generate Financial Recommendation",
                    description="Prepare recommendation.",
                    depends_on=["task_2"]
                )

            ]

        elif domain == "research":

            return [

                PlannerTask(
                    id="task_1",
                    name="Define Research Topic",
                    description="Understand research objective."
                ),

                PlannerTask(
                    id="task_2",
                    name="Collect Sources",
                    description="Retrieve relevant sources.",
                    depends_on=["task_1"]
                ),

                PlannerTask(
                    id="task_3",
                    name="Analyze Sources",
                    description="Analyze collected information.",
                    depends_on=["task_2"]
                ),

                PlannerTask(
                    id="task_4",
                    name="Generate Research Summary",
                    description="Generate research report.",
                    depends_on=["task_3"]
                )

            ]

        elif domain == "communication":
            q_lower = query.lower()
            if "attachment" in q_lower or "download" in q_lower:
                return [
                    PlannerTask(
                        id="task_1",
                        name="Download Email Attachment",
                        description="Download attachments from email."
                    )
                ]
            elif "draft" in q_lower or "prepare" in q_lower:
                return [
                    PlannerTask(
                        id="task_1",
                        name="Draft Email",
                        description="Create an email draft."
                    )
                ]
            elif "read" in q_lower or "view" in q_lower or "open" in q_lower:
                return [
                    PlannerTask(
                        id="task_1",
                        name="Read Email",
                        description="Read email message contents."
                    )
                ]
            elif "search" in q_lower or "find" in q_lower:
                return [
                    PlannerTask(
                        id="task_1",
                        name="Search Email",
                        description="Search mail box."
                    )
                ]
            else:
                # Default to email sending workflow
                return [
                    PlannerTask(
                        id="task_1",
                        name="Send Email",
                        description="Deliver the email to the recipient."
                    )
                ]

        elif domain == "business":

            return [

                PlannerTask(
                    id="task_1",
                    name="Understand Business Goal",
                    description="Analyze business request."
                ),

                PlannerTask(
                    id="task_2",
                    name="Analyze Business Strategy",
                    description="Analyze strategy.",
                    depends_on=["task_1"]
                ),

                PlannerTask(
                    id="task_3",
                    name="Generate Business Recommendations",
                    description="Prepare recommendations.",
                    depends_on=["task_2"]
                )

            ]

        elif domain == "healthcare":

            return [

                PlannerTask(
                    id="task_1",
                    name="Understand Health Query",
                    description="Understand healthcare request."
                ),

                PlannerTask(
                    id="task_2",
                    name="Analyze Symptoms",
                    description="Analyze provided information.",
                    depends_on=["task_1"]
                ),

                PlannerTask(
                    id="task_3",
                    name="Generate Health Guidance",
                    description="Provide guidance.",
                    depends_on=["task_2"]
                )

            ]

        elif domain == "legal":

            return [

                PlannerTask(
                    id="task_1",
                    name="Understand Legal Request",
                    description="Understand legal issue."
                ),

                PlannerTask(
                    id="task_2",
                    name="Analyze Legal Context",
                    description="Analyze request.",
                    depends_on=["task_1"]
                ),

                PlannerTask(
                    id="task_3",
                    name="Generate Legal Guidance",
                    description="Generate legal response.",
                    depends_on=["task_2"]
                )

            ]

        elif domain == "productivity":

            return [

                PlannerTask(
                    id="task_1",
                    name="Understand Productivity Goal",
                    description="Understand planning request."
                ),

                PlannerTask(
                    id="task_2",
                    name="Create Productivity Plan",
                    description="Generate schedule or task plan.",
                    depends_on=["task_1"]
                )

            ]

        elif domain == "system":

            return [

                PlannerTask(
                    id="task_1",
                    name="Analyze System Request",
                    description="Analyze system operation."
                ),

                PlannerTask(
                    id="task_2",
                    name="Prepare System Action",
                    description="Prepare requested action.",
                    depends_on=["task_1"]
                )

            ]

        # General domain dynamic sub-task plans
        if domain == "general":
            q_lower = query.lower()
            
            # 1. Browser Screenshot
            if any(w in q_lower for w in ["screenshot", "screen capture", "capture webpage", "capture page"]):
                return [
                    PlannerTask(
                        id="task_1",
                        name="Capture Screenshot",
                        description="Capture webpage screenshot."
                    )
                ]

            # 2. Browser Download
            if any(w in q_lower for w in ["download", "fetch file"]):
                if "email" not in q_lower and "attachment" not in q_lower:
                    return [
                        PlannerTask(
                            id="task_1",
                            name="Download File",
                            description="Download file from URL."
                        )
                    ]

            # 3. Browser History
            if "history" in q_lower or "visited" in q_lower:
                return [
                    PlannerTask(
                        id="task_1",
                        name="Retrieve Browser History",
                        description="Fetch browser navigation log."
                    )
                ]

            # 4. Browser Search
            if "browser search" in q_lower or "web search" in q_lower:
                return [
                    PlannerTask(
                        id="task_1",
                        name="Browser Search",
                        description="Search webpage content."
                    )
                ]
                
            if any(w in q_lower for w in ["weather", "forecast", "temp", "temperature", "climate", "aqi", "air quality", "pollution", "alert", "warning"]):
                if "air quality" in q_lower or "aqi" in q_lower or "pollution" in q_lower:
                    task_name = "Fetch Air Quality"
                    task_desc = "Retrieve real-time air quality information."
                elif "alert" in q_lower or "warning" in q_lower:
                    task_name = "Fetch Weather Alerts"
                    task_desc = "Retrieve active weather alerts."
                elif "forecast" in q_lower or "predict" in q_lower:
                    task_name = "Fetch Weather Forecast"
                    task_desc = "Retrieve weather forecast details."
                else:
                    task_name = "Fetch Current Weather"
                    task_desc = "Retrieve real-time weather information."
                    
                return [
                    PlannerTask(
                        id="task_1",
                        name="Analyze Weather Request",
                        description="Identify location for weather report."
                    ),
                    PlannerTask(
                        id="task_2",
                        name=task_name,
                        description=task_desc,
                        depends_on=["task_1"]
                    )
                ]
            
            if any(w in q_lower for w in ["calculate", "calculator", "math", "+", "-", "*", "/", "sum", "add", "multiply", "divide"]):
                # Guard against weather or maps queries that happen to use the word "calculate"
                if not any(w in q_lower for w in ["weather", "forecast", "temp", "temperature", "climate", "aqi", "air quality", "pollution", "alert", "warning", "distance", "route", "map", "navigation", "geocode", "coordinates", "places", "nearby", "directions", "direction"]):
                    return [
                        PlannerTask(
                            id="task_1",
                            name="Analyze Math Expression",
                            description="Identify expression to calculate."
                        ),
                        PlannerTask(
                            id="task_2",
                            name="Calculate Expression",
                            description="Evaluate mathematical expression.",
                            depends_on=["task_1"]
                        )
                    ]
                
            if any(w in q_lower for w in ["distance", "route", "map", "navigation", "between", "from", "geocode", "coordinates", "places", "nearby"]):
                if "geocode" in q_lower or "coordinates" in q_lower:
                    task_name = "Geocode Address"
                    task_desc = "Convert address to geographic coordinates."
                elif "navigation" in q_lower or "directions" in q_lower:
                    task_name = "Generate Navigation Guidance"
                    task_desc = "Provide turn-by-turn navigation instructions."
                elif "places" in q_lower or "nearby" in q_lower:
                    task_name = "Search Nearby Places"
                    task_desc = "Find nearby points of interest."
                elif "route" in q_lower:
                    task_name = "Calculate Best Route"
                    task_desc = "Compute optimal route legs and steps."
                else:
                    task_name = "Calculate Map Distance"
                    task_desc = "Compute distance between locations."

                return [
                    PlannerTask(
                        id="task_1",
                        name="Analyze Map Request",
                        description="Identify origin, destination or address."
                    ),
                    PlannerTask(
                        id="task_2",
                        name=task_name,
                        description=task_desc,
                        depends_on=["task_1"]
                    )
                ]

        return [

            PlannerTask(
                id="task_1",
                name="Understand Query",
                description="Understand user request."
            ),

            PlannerTask(
                id="task_2",
                name="Generate Response",
                description="Generate final response.",
                depends_on=["task_1"]
            )

        ]