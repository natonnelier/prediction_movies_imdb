#######################################################

def gpt_budget_score(budget_log):
    budget = 10 ** budget_log
    if budget < 5_000_000:
        return 2
    elif budget < 20_000_000:
        return 8
    elif budget < 100_000_000:
        return 10
    elif budget < 200_000_000:
        return 6
    else:
        return 2


def gpt_runtime_score(runtime):
    if 90 <= runtime <= 120:
        return 10
    elif 120 < runtime <= 150:
        return 7
    elif 70 <= runtime < 90:
        return 6
    else:
        return 2


def gpt_language_score(row):
    scores = {
        "lang_en": 10,
        "lang_ja": 7,
        "lang_zh": 7,
        "lang_fr": 6,
        "lang_es": 5,
        "lang_it": 5,
        "lang_ru": 5,
        "lang_hi": 5,
        "lang_ta": 5,
        "lang_fa": 5,
        "lang_other": 4,
    }
    return max((value for key, value in scores.items() if row[key]),default=5)


def gpt_genre_score(row):
    scores = {
        "genre_Horror": 10,
        "genre_Thriller": 9,
        "genre_Mystery": 8,
        "genre_Comedy": 8,
        "genre_Crime": 7,
        "genre_Romance": 7,
        "genre_Drama": 6,
        "genre_Animation": 6,
        "genre_Action": 5,
        "genre_Science Fiction": 4,
        "genre_Fantasy": 3,
        "genre_Adventure": 3,
        "genre_War": 2,
        "genre_History": 2,
        "genre_Documentary": 2,
        "genre_Western": 2,
        "genre_Music": 4,
        "genre_Family": 6,
        "genre_TV Movie": 3
    }
    active = [value for key, value in scores.items()if row[key] == 1]
    return max(active, default=5)


def gpt_country_score(row):
    scores = {
        "country_United States of America": 10,
        "country_United Kingdom": 8,
        "country_Canada": 8,
        "country_Japan": 8,
        "country_France": 6,
        "country_Germany": 6,
        "country_Australia": 6,
        "country_Italy": 5,
        "country_Spain": 5,
        "country_India": 5,
    }
    active = [value for key, value in scores.items()if row[key] == 1]
    return max(active, default=4)


def gpt_company_score(row):
    scores = {
        "company_Walt Disney Pictures": 10,
        "company_Warner Bros. Pictures": 10,
        "company_Universal Pictures": 10,
        "company_Paramount": 9,
        "company_20th Century Fox": 9,
        "company_Columbia Pictures": 9,
        "company_Lionsgate": 8,
        "company_New Line Cinema": 8,
        "company_Metro-Goldwyn-Mayer": 7,
        "company_Miramax": 7,
        "company_Summit Entertainment": 7,
        "company_StudioCanal": 6,
        "company_United Artists": 6,
        "company_Touchstone Pictures": 6,
        "company_Canal+": 5,
    }
    active = [value for key, value in scores.items()if row[key] == 1]

    return max(active, default=5)


def gpt_keyword_score(row):
    positive = {
        "kw_sequel": 4,
        "kw_based on comic": 5,
        "kw_remake": 2,
        "kw_based on novel or book": 3,
        "kw_based on true story": 2,
        "kw_duringcreditsstinger": 3,
        "kw_aftercreditsstinger": 3,
    }

    negative = {
        "kw_biography": -1,
        "kw_woman director": -1,
    }

    score = 5
    score += sum(value for key, value in positive.items()if row[key] == 1)
    score += sum(value for key, value in negative.items()if row[key] == 1)

    return min(max(score, 0), 10)


def gpt_release_score(row):
    blockbuster_months = {
        "month_5",
        "month_6",
        "month_7",
        "month_11",
        "month_12",
    }

    good_months = {
        "month_3",
        "month_4",
    }

    if any(row[m] == 1 for m in blockbuster_months):
        return 10

    if any(row[m] == 1 for m in good_months):
        return 7

    return 5


def heuristica_gpt(row):
    score = (
        0.15 * gpt_budget_score(row["budget"])
        + 0.15 * gpt_genre_score(row)
        + 0.10 * gpt_release_score(row)
        + 0.10 * gpt_runtime_score(row["runtime"])
        + 0.20 * gpt_company_score(row)
        + 0.10 * gpt_country_score(row)
        + 0.05 * gpt_language_score(row)
        + 0.15 * gpt_keyword_score(row)
    )

    return score * 10 >= 60 #devuelve true o false



##################################################################################################

# Heusristica Sonnet 4.6 de Anthropic

GENRE_ROI_SCORE = {
    "Horror": 2.0, "Animation": 1.8, "Family": 1.6, "Adventure": 1.4,
    "Science Fiction": 1.3, "Action": 1.2, "Comedy": 1.1, "Thriller": 1.0,
    "Mystery": 1.0, "Fantasy": 0.9, "Crime": 0.8, "Romance": 0.8,
    "Drama": 0.7, "War": 0.6, "Western": 0.6, "History": 0.5,
    "Documentary": 0.5, "Music": 0.5, "TV Movie": 0.3,
}

SEASON_SCORE = {
    1: 0.3, 2: 0.4, 3: 0.7, 4: 0.7,  5: 1.0,
    6: 1.0, 7: 1.0, 8: 0.8, 9: 0.5, 10: 0.6,
    11: 0.9, 12: 1.0,
}

MAJOR_STUDIO_COLS = {
    "company_Warner Bros. Pictures", "company_Universal Pictures",
    "company_Paramount", "company_20th Century Fox", "company_Columbia Pictures",
    "company_Metro-Goldwyn-Mayer", "company_New Line Cinema",
    "company_Walt Disney Pictures", "company_Miramax", "company_Lionsgate",
    "company_United Artists", "company_StudioCanal", "company_Summit Entertainment",
}

GENRE_COLS = [
    "genre_Action", "genre_Adventure", "genre_Animation", "genre_Comedy",
    "genre_Crime", "genre_Documentary", "genre_Drama", "genre_Family",
    "genre_Fantasy", "genre_History", "genre_Horror", "genre_Music",
    "genre_Mystery", "genre_Romance", "genre_Science Fiction",
    "genre_TV Movie", "genre_Thriller", "genre_War", "genre_Western",
]

MONTH_COLS = [
    "month_1", "month_2", "month_3", "month_4", "month_5", "month_6",
    "month_7", "month_8", "month_9", "month_10", "month_11", "month_12",
]


def sonnet_score_budget(budget):
    budget = 10 ** budget
    if budget < 1_000_000:
        return 0.5
    elif budget < 10_000_000:
        return 1.0
    elif budget < 80_000_000:
        return 2.0
    elif budget < 200_000_000:
        return 1.5
    else:
        return 1.0


def sonnet_score_genre(row):
    active = [col.replace("genre_", "") for col in GENRE_COLS if row[col] == 1]
    if not active:
        return 0.5
    scores = [GENRE_ROI_SCORE.get(g, 0.7) for g in active]
    best = max(scores)
    avg = sum(scores) / len(scores)
    return round(min((best * 0.7 + avg * 0.3) * 1.25, 2.5), 2)


def sonnet_score_season(row):
    for col in MONTH_COLS:
        if row[col] == 1:
            month_number = int(col.replace("month_", ""))
            return round(SEASON_SCORE[month_number] * 2, 2)
    return 1.0


def sonnet_score_language(row):
    return 1.0 if row["lang_en"] else 0.3


def sonnet_score_studio(row):
    matches = sum(1 for col in MAJOR_STUDIO_COLS if row.get(col, 0) == 1)
    if matches >= 2:
        return 2.0
    elif matches == 1:
        return 1.3
    else:
        return 0.0


def sonnet_score_runtime(runtime):
    if 80 <= runtime <= 140:
        return 0.5
    elif runtime < 70:
        return 0.1
    else:
        return 0.2


def heuristica_sonnet(row):
    total = (
        sonnet_score_budget(row["budget"])
        + sonnet_score_genre(row)
        + sonnet_score_season(row)
        + sonnet_score_language(row)
        + sonnet_score_studio(row)
        + sonnet_score_runtime(row["runtime"])
    )
    return total >= 7.0 #devuelve true o false