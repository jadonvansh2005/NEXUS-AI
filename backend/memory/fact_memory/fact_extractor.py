import re


class FactExtractor:

    def extract(

        self,

        text: str

    ):

        facts = {}

        text = text.strip()

        # -------------------------
        # Name
        # -------------------------

        nickname_terminator = r"(?:[\s,.-]+(?:call sign|call me|my nickname is|friends call me|people call me|nickname))"

        name_patterns = [

            rf"my name is[\s,.-]*(.*?)(?:{nickname_terminator}|$)",
            rf"this is[\s,.-]*(.*?)(?:{nickname_terminator}|$)",
            rf"my\s*self[\s,.-]*(.*?)(?:{nickname_terminator}|$)",
            rf"name is[\s,.-]*(.*?)(?:{nickname_terminator}|$)"

        ]

        for pattern in name_patterns:

            match = re.search(

                pattern,

                text,

                re.IGNORECASE

            )

            if match:

                facts["name"] = (

                    match.group(1)

                    .strip()

                )

                break

        # -------------------------
        # Nickname
        # -------------------------

        nickname_patterns = [

            r"people call me (.+)",
            r"call me (.+)",
            r"call sign (.+)",
            r"my nickname is (.+)",
            r"friends call me (.+)",
            r"you can call me (.+)"

        ]

        for pattern in nickname_patterns:

            match = re.search(

                pattern,

                text,

                re.IGNORECASE

            )

            if match:

                facts["nickname"] = (

                    match.group(1)

                    .strip()

                )

                break

        # -------------------------
        # Location
        # -------------------------

        location_patterns = [

            r"i live in (.+)",
            r"i am from (.+)",
            r"i belong to (.+)",
            r"currently living in (.+)",
            r"i stay in (.+)",
            r"i reside in (.+)"

        ]

        for pattern in location_patterns:

            match = re.search(

                pattern,

                text,

                re.IGNORECASE

            )

            if match:

                facts["location"] = (

                    match.group(1)

                    .strip()

                )

                break

        # -------------------------
        # Hometown
        # -------------------------

        hometown_patterns = [

            r"my hometown is (.+)",
            r"i come from (.+)",
            r"my native place is (.+)",
            r"originally from (.+)"

        ]

        for pattern in hometown_patterns:

            match = re.search(

                pattern,

                text,

                re.IGNORECASE

            )

            if match:

                facts["hometown"] = (

                    match.group(1)

                    .strip()

                )

                break

        # -------------------------
        # College
        # -------------------------

        college_patterns = [

            r"i study at (.+)",
            r"i am studying at (.+)",
            r"my college is (.+)",
            r"i attend (.+)",
            r"i go to (.+)"

        ]

        for pattern in college_patterns:

            match = re.search(

                pattern,

                text,

                re.IGNORECASE

            )

            if match:

                facts["college"] = (

                    match.group(1)

                    .strip()

                )

                break

        # -------------------------
        # Branch
        # -------------------------

        branch_patterns = [

            r"i am a (.+) student",
            r"my branch is (.+)",
            r"i am pursuing (.+)",
            r"i study (.+) engineering"

        ]

        for pattern in branch_patterns:

            match = re.search(

                pattern,

                text,

                re.IGNORECASE

            )

            if match:

                facts["branch"] = (

                    match.group(1)

                    .strip()

                )

                break

        # -------------------------
        # Learning
        # -------------------------

        learning_patterns = [

            r"i am learning (.+)",
            r"i'm learning (.+)",
            r"currently learning (.+)",
            r"learning (.+)",
            r"studying (.+)"

        ]

        for pattern in learning_patterns:

            match = re.search(

                pattern,

                text,

                re.IGNORECASE

            )

            if match:

                facts["learning"] = (

                    match.group(1)

                    .strip()

                )

                break

        # -------------------------
        # Project
        # -------------------------

        project_patterns = [

            r"i am building (.+)",
            r"i'm building (.+)",
            r"working on (.+)",
            r"my project is (.+)",
            r"currently building (.+)"

        ]

        for pattern in project_patterns:

            match = re.search(

                pattern,

                text,

                re.IGNORECASE

            )

            if match:

                facts["project"] = (

                    match.group(1)

                    .strip()

                )

                break

        # -------------------------
        # Career Goal
        # -------------------------

        goal_patterns = [

            r"my goal is to become (.+)",
            r"i want to become (.+)",
            r"i want to be (.+)",
            r"my dream is to become (.+)",
            r"aspiring to become (.+)"

        ]

        for pattern in goal_patterns:

            match = re.search(

                pattern,

                text,

                re.IGNORECASE

            )

            if match:

                facts["career_goal"] = (

                    match.group(1)

                    .strip()

                )

                break

        # -------------------------
        # Dream Company
        # -------------------------

        company_patterns = [

            r"my dream company is (.+)",
            r"i want to work at (.+)",
            r"i want a job at (.+)",
            r"i want to join (.+)"

        ]

        for pattern in company_patterns:

            match = re.search(

                pattern,

                text,

                re.IGNORECASE

            )

            if match:

                facts["dream_company"] = (

                    match.group(1)

                    .strip()

                )

                break

        # -------------------------
        # Favorite Language
        # -------------------------

        language_patterns = [

            r"my favorite language is (.+)",
            r"i love programming in (.+)",
            r"i like coding in (.+)",
            r"preferred language is (.+)"

        ]

        for pattern in language_patterns:

            match = re.search(

                pattern,

                text,

                re.IGNORECASE

            )

            if match:

                facts["favorite_language"] = (

                    match.group(1)

                    .strip()

                )

                break


        # -------------------------
        # Likes
        # -------------------------

        likes_patterns = [

            r"i like (.+)",
            r"i love (.+)",
            r"i enjoy (.+)",
            r"my favorite is (.+)"

        ]

        for pattern in likes_patterns:

            match = re.search(

                pattern,

                text,

                re.IGNORECASE

            )

            if match:

                facts["likes"] = (

                    match.group(1).strip()

                )

                break

        # -------------------------
        # Favorite Subject
        # -------------------------

        subject_patterns = [

            r"my favorite subject is (.+)",
            r"i love studying (.+)",
            r"i like studying (.+)"

        ]

        for pattern in subject_patterns:

            match = re.search(

                pattern,

                text,

                re.IGNORECASE

            )

            if match:

                facts["favorite_subject"] = (

                    match.group(1)

                    .strip()

                )

                break

        # -------------------------
        # Job Role
        # -------------------------

        role_patterns = [

            r"i work as (.+)",
            r"my role is (.+)",
            r"i am working as (.+)",
            r"currently working as (.+)"

        ]

        for pattern in role_patterns:

            match = re.search(

                pattern,

                text,

                re.IGNORECASE

            )

            if match:

                facts["job_role"] = (

                    match.group(1)

                    .strip()

                )

                break

        # -------------------------
        # Skills
        # -------------------------

        skills_patterns = [

            r"my skills are (.+)",
            r"i am skilled in (.+)",
            r"i have experience in (.+)",
            r"i know (.+)"

        ]

        for pattern in skills_patterns:

            match = re.search(

                pattern,

                text,

                re.IGNORECASE

            )

            if match:

                facts["skills"] = (

                    match.group(1)

                    .strip()

                )

                break

        # -------------------------
        # Age
        # -------------------------

        age_patterns = [

            r"i am (\d+) years old",
            r"my age is (\d+)",
            r"i'm (\d+) years old"

        ]

        for pattern in age_patterns:

            match = re.search(

                pattern,

                text,

                re.IGNORECASE

            )

            if match:

                facts["age"] = (

                    match.group(1)

                    .strip()

                )

                break

        # Clean and filter out invalid/question-like values from extracted facts
        cleaned_facts = {}
        for k, v in facts.items():
            cleaned_val = v.strip("?.!,- ")
            # If the value is empty, contains question marks, or looks like a question, ignore it
            if cleaned_val and not any(q_word in cleaned_val.lower() for q_word in ["what", "who", "where", "why", "how", "which", "?", "tell me"]):
                cleaned_facts[k] = cleaned_val

        return cleaned_facts