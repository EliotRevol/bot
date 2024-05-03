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


class Polls:
    round1 = {
        "Macron": 26,
        "Le Pen": 24.5,
        "Mélenchon": 18,
        "Zemmour": 8.55,
        "Pécresse": 7.3,
        "Jadot": 4.85,
        "Lassalle": 2.6,
        "Roussel": 2.55,
        "Dupont-Aignan": 2.3,
        "Hidalgo": 2,
        "Poutou": 1,
        "Arthaud": 0.395
    }  # https://www.contexte.com/pouvoirs/page/pollotron-les-sondages-de-la-presidentielle-2022-et-la-tendance-pour-chaque-candidat.html
    # mean of two values - depuis trois mois


class Folders:
    class Round1:
        minus1month = [
            "03_11_2022",
            "03_12_2022",
            "03_13_2022",
            "03_14_2022",
            "03_15_2022",
            "03_16_2022",
            "03_17_2022",
            "03_18_2022",
            "03_19_2022",
            "03_20_2022",
            "03_21_2022",
            "03_22_2022",
            "03_23_2022",
            "03_24_2022",
            "03_25_2022",
            "03_26_2022",
            "03_27_2022",
            "03_28_2022",
            "03_29_2022",
            "03_30_2022",
            "03_31_2022",
            "04_01_2022",
            "04_02_2022",
            "04_03_2022",
            "04_04_2022",
            "04_05_2022",
            "04_06_2022",
            "04_07_2022",
            "04_08_2022",
            "04_09_2022",
            "04_10_2022",
            "04_11_2022"
        ]
        minus2month = minus1month + ["02_11_2022",
                                     "02_12_2022",
                                     "02_13_2022",
                                     "02_14_2022",
                                     "02_15_2022",
                                     "02_16_2022",
                                     "02_17_2022",
                                     "02_18_2022",
                                     "02_19_2022",
                                     "02_20_2022",
                                     "02_21_2022",
                                     "02_22_2022",
                                     "02_23_2022",
                                     "02_24_2022",
                                     "02_25_2022",
                                     "02_26_2022",
                                     "02_27_2022",
                                     "02_28_2022",
                                     "02_29_2022",
                                     "02_30_2022",
                                     "02_31_2022",
                                     "03_01_2022",
                                     "03_02_2022",
                                     "03_03_2022",
                                     "03_04_2022",
                                     "03_05_2022",
                                     "03_06_2022",
                                     "03_07_2022",
                                     "03_08_2022",
                                     "03_09_2022",
                                     "03_10_2022",
                                     "03_11_2022"]
        minus3month = minus1month + minus2month + ["14.01.2022",
                                                   "01_14_2022",
                                                   "01_15_2022",
                                                   "01_16_2022",
                                                   "01_17_2022",
                                                   "01_18_2022",
                                                   "01_19_2022",
                                                   "01_20_2022",
                                                   "01_21_2022",
                                                   "01_22_2022",
                                                   "01_23_2022",
                                                   "01_24_2022",
                                                   "01_25_2022",
                                                   "01_26_2022",
                                                   "01_27_2022",
                                                   "01_28_2022",
                                                   "01_29_2022",
                                                   "01_30_2022",
                                                   "01_31_2022",
                                                   "02_01_2022",
                                                   "02_02_2022",
                                                   "02_03_2022",
                                                   "02_04_2022",
                                                   "02_05_2022",
                                                   "02_06_2022",
                                                   "02_07_2022",
                                                   "02_08_2022",
                                                   "02_09_2022",
                                                   "02_10_2022",
                                                   "02_11_2022"]
        folders_dict = {"minus1month": minus1month, "minus2month": minus2month, "minus3month": minus3month}


class Results:
    round1 = {
        "Pécresse": 4.78,
        "Macron": 27.85,
        "Hidalgo": 1.75,
        "Mélenchon": 21.95,
        "Jadot": 4.63,
        "Zemmour": 7.07,
        "Roussel": 2.28,
        "Lassalle": 3.13,
        "Arthaud": 0.56,
        "Dupont-Aignan": 2.06,
        "Le Pen": 23.15,
        "Poutou": 0.77
    }
    # https://www.resultats-elections.interieur.gouv.fr/presidentielle-2022/FE.html


class Channels:
    tv_in_csa = ["TF1", "France2", "France3", "France5", "M6", "C8", "BFMTV", "Cnews", "RT France", "LCI",
                 "FranceinfoTV", "France24", "Euronews"]


class Experiments(str, Enum):
    WELCOME_FETCH = "election-welcome-fetch"
    WELCOME_WALK = "election-welcome-walk"
    NATIONAL_NEWS_FETCH = "election-national-news-fetch"
    NATIONAL_NEWS_WALK = "election-national-news-walk"
    CHANNEL_PERSONALIZATION = "election-channel-personalization"
    META_CHANNEL_PERSONALIZATION = "meta-channel-personalization"
    META_WALKS = "meta-walk"


class MetaChannels:
    channel_list = ['news', 'sports', 'music', 'learning', 'gaming', 'fashion']


class ResultTypes(str, Enum):
    CSV = ".csv"
    JSON = ".json"
    HTML = "html.gz"
    TRANSCRIPT = "transcript.gz"
    VARS = ".txt"


#
# class LegislativeParties:
#     Parties = {"LREM": ["La République en marche", "Mouvement démocrate",
#                             "Territoires de progrès", "Agir", "Horizons",
#                             "Parti radical ", "Ensemble", "Renaissance",
#                                                           "Ensemble", "MoDem", "TDP", "H", "PRV"
#                             ],
#                "NUPES": ["La France insoumise", "Parti communiste français",
#                                                                   "Europe Écologie Les Verts", "Parti socialiste",
#                                                                   "Génération.s", "Les Nouveaux Démocrates",
#                                                                   "Génération écologie",
#                                                                     "Nouvelle Union populaire écologique et sociale",
#                                                                   "NUPES", "LFI", "PCF", "EELV", "PS", "G.s", "LND",
#                                                                   "GÉ"],
#
#                "UDC": [" Républicains", "Union des démocrates et indépendants",
#                                                    "Centristes",
#                                                     "Union de la droite et du centre",
#                                                    "LR", "UDI", "LC"],
#
#
#                "Reconquête": "REC",
#
#                "Rassemblement national": "RN",
#                }
#
#     Parties = ["Ensemble", "NUPES"]


class LegislativeParties:
    Parties = {"NUPES": ["Nouvelle Union populaire écologique et sociale"],
               "LREM": ["Renaissance", "La République en marche", "Mouvement démocrate"],
               "RN": ["Rassemblement National"],
               "UDC": ["Républicains", "Centristes"],
               "REC": ["Reconquête"]}
    IncreasedDetail = {"LREM": ["La République en marche", "Mouvement démocrate",
                                "Territoires de progrès", "Agir", "Horizons",
                                "Parti radical ", "Renaissance",
                                "Ensemble", "MoDem", "TDP", "PRV","en marche"
                                ],
                       "NUPES": ["La France insoumise", "Parti communiste français",
                                 "Europe Écologie Les Verts", "Parti socialiste",
                                 "Génération.s", "Les Nouveaux Démocrates",
                                 "Génération écologie",
                                 "Nouvelle Union populaire écologique et sociale",
                                 "LFI", "PCF", "EELV", "PS", "G.s", "LND",
                                 "GÉ"],

                       "UDC": ["Républicains", "Union des démocrates et indépendants",
                               "Centristes",
                               "Union de la droite et du centre",
                               "LR", "UDI", "LC"],

                       "REC": ["Reconquête"],

                       "RN": ["Rassemblement national"],
                       }
