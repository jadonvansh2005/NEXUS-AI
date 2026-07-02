import re

import nltk

from nltk.corpus import stopwords

from nltk.stem.porter import (
    PorterStemmer
)

nltk.download(
    "stopwords",
    quiet=True
)

stop_words = set(
    stopwords.words(
        "english"
    )
)

ps = PorterStemmer()


class TextCleaner:

    def clean_text(
        self,
        text
    ):

        if text is None:

            return ""

        text = str(text)

        text = text.lower()

        text = re.sub(
            r"http\S+|www\S+|https\S+",
            "",
            text
        )

        text = re.sub(
            r"\S+@\S+",
            "",
            text
        )

        text = re.sub(
            r"[^\w\s]",
            " ",
            text
        )

        text = re.sub(
            r"\d+",
            "",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        ).strip()

        words = []

        for word in text.split():

            if word not in stop_words:

                words.append(

                    ps.stem(
                        word
                    )

                )

        return " ".join(
            words
        )