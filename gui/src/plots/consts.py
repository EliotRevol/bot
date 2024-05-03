from enum import Enum


class Candidates:
    polls = ["Roussel",
             "Mélenchon",
             "Hidalgo",
             "Montebourg",
             "Jadot",
             "Macron",
             "Pécresse",
             "Dupont-Aignan",
             "Le Pen",
             "Zemmour"
             ]
    official = [
        "Pécresse",
        "Macron",
        "Hidalgo",
        "Mélenchon",
        "Jadot",
        "Zemmour",
        "Roussel",
        "Lassalle",
        "Arthaud",
        "Dupont-Aignan",
        "Le Pen",
        "Poutou"
    ]
    personalized_channels = ["Macron", "Le Pen", "Zemmour", "Pécresse", "Mélenchon"]


class Channels:
    tv_in_csa = ["TF1", "France2", "France3", "France5", "M6", "C8", "BFMTV", "Cnews", "RT France", "LCI",
                 "FranceinfoTV", "France24", "Euronews"]


class Experiments(str, Enum):
    WELCOME_FETCH = "election-welcome-fetch"
    WELCOME_WALK = "election-welcome-walk"
    NATIONAL_NEWS_FETCH = "election-national-news-fetch"
    NATIONAL_NEWS_WALK = "election-national-news-walk"
    CHANNEL_PERSONALIZATION = "election-channel-personalization"


class ResultTypes(str, Enum):
    CSV = ".csv"
    JSON = ".json"
    HTML = "html.gz"
    TRANSCRIPT = "transcript.gz"
    VARS = ".txt"
