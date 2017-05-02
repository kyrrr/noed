# store here for easy maintenance
# see http://statistikkbanken.oslo.kommune.no/webview/
# http://data.ssb.no/api/klass/v1/api-guide.html
location_kws = {
    'oslo': {
        'discrict': {
            "gamle oslo": {
                "lodalen",  # : {},
                "grønland",  # : {},
                "enerhaugen",  # : {},
                "nedre tøyen",  # : {},
                "kampen",  # : {},
                "vålerenga",  # : {},
                "helsfyr",  # : {},
            },
            "grünerløkka": {
                "grünerløkka vest",  # : {},
                "grünerløkka øst",  # : {},
                "dælenenga",  # : {},
                "sinsen",  # : {},
                "sofienberg",  # : {},
                "hasle-løren",  # : {},
            },
            "sagene": {
                "iladalen",  # : {},
                "bjølsen",  # : {},
                "sandaker",  # : {},
                "torshov",  # : {},
            },
            "st.hanshaugen": {
                "hammersborg",  # : {},
                "bislett",  # : {},
                "ila",  # : {},
                "fagerborg",  # : {},
                "lindern",  # : {},
            },
            "frogner": {
                "bygdøy",  # : {},
                "frogner",  # : {},
                "frognerparken",  # : {},
                "majorstuen",  # : {},  # nord/syd
                "homansbyen",  # : {},
                "uranienborg",  # : {},
                "skillebekk",  # : {},
            },
            "ullern": {
                "ullernåsen",  # : {},
                "lilleaer",  # : {},
                "ullern",  # : {},
                "montebello-hoff",  # : {},
                "skøyen",  # : {},
            },
            "vestre aker": {
                "røa",  # : {},
                "holmenkollen",  # : {},
                "hovseter",  # : {},
                "holmen",  # : {},
                "slemdal",  # : {},
                "grimelund",  # : {},
                "vinderen",  # : {},
            },
            "nordre aker": {
                "disen",  # : {},
                "myrer",  # : {},
                "grefsen",  # : {},
                "kjelsås",  # : {},
                "korsvoll",  # : {},
                "tåsen",  # : {},
                "nordberg",  # : {},
                "ullevål hageby",  # : {},
            },
            "bjerke": {
                "veitvet",  # : {},
                "linderud",  # : {},
                "økern",  # : {},
                "årvoll",  # : {},
            },
            "grorud": {
                "ammerud",  # : {},
                "rødtvet",  # : {},
                "nordtvet",  # : {},
                "grorud",  # : {},
                "romsås",  # : {},
            },
            "stovner": {
                "vestli",  # : {},
                "fossum",  # : {},
                "rommen",  # : {},
                "haugenstua",  # : {},
                "stovner",  # : {},
                "høybråten",  # : {},
            },
            "alna": {
                "furuset",  # : {},
                "ellingsrud",  # : {},
                "lindeberg",  # : {},
                "trosterud",  # : {},
                "hellerudtoppen",  # : {},
                "tveita",  # : {},
                "teisen",  # : {},
            },
            "østensjø": {
                "manglerud",  # : {},
                "godlia",  # : {},
                "oppsal",  # : {},
                "bøler",  # : {},
                "skullerud",  # : {},
                "abildsø",  # : {},
            },
            "nordstrand": {
                "ljan",  # : {},
                "nordstrand",  # : {},
                "bekkelaget",  # : {},
                "simensbråten",  # : {},
                "lambertseter",  # : {},
                "munkerud",  # : {},
            },
            "søndre nordstrand": {
                "holmlia",  # : {},
                "prinsdal",  # : {},
                "bjørnerud",  # : {},
                "mortensrud",  # : {},
                "bjørndal",  # : {},
            },
            "sentrum": {},
            "marka": {},
        }
    }
}

kws = {
        'negative': [
            "ingen", "ikke", "mangler",
        ],
        'announcement': [
            "holde seg innendørs", "rettelse",
        ],
        'fire': [
            "brann", "boligbrann", "gressbrann", "bilbrann", "røykutvikling", "røyk", "tørrkok", "peis", "branntilløp",
            "røyklukt", "svart røyk", "spredningsfare", "brenner", "brent", "brannalarm", "eksponert", "svidd",
            "tørrkok", "brant", "påtent", "flammer", "røyklukt", "pipebrann", "varmgang", "pipa",
        ],
        'traffic_information': [
            "saktegående", "kø", "lang kø", "kø i begge retninger", "feltet er sperret", "kjøretøystans",
            "glatt veibane", "glatt vegbane", "trafikkkaos", "trafikkfarlig", "redusert hastighet", "trafikale problemer",
            "veltet", "stans", "kollektivfelt", "trafikkontroll", "normal ferdsel", "flyte greit", "forsinkelse",
            "dirigert", "midlertidig sperret", "sperret",
        ],
        'crime': [
            "knivstukket", "stålet", "våpen", "slagsmål", "bombe", "eksplosiv", "mishandlet", "frastjålet", "påvirket tilstand",
            "under påvirkning", "ordensforstyrrelse", "ranet", "fraranet", "ruspåvirket", "bråk", "slag", "slått", "innbrudd",
            "innbruddsforsøk", "tent på", "tagging", "tagget", "herværk", "vandalisme", "støy", "husbråk", "trussel", "trusler",
            "skallet ned", "trusler", "kaste", "slåss",
            "kamp", "vikeplikt", "usikret", "naken", "slossing", "tømt", "påtent", "narkotika",
            "promille", "kroppskade", "ruset", "luske", "barke", "vold", "bite", "bitt",
        ],
        'weapon': [
            "kniv", "pistol", "våpen", "gevær", "rifle", "hagle", "skytevåpen", "hammer", "øks", "machete",
            "skarp gjenstand", "flaske", "stein", "sten", ""
        ],
        'prank': [  # vettafan hvæ denna burde heti
            "guttestreker", "spøk", "prank", "tull", "påfunn",
        ],
        'animal': [
            "hund", "katt", "valp", "hest",
        ],
        'bad_guy': [
            "tyv", "morder", "mistenkt", "mistenkelig", "vinningskriminell", "innbruddstyv", "biltyv",
            "gjerningsmannen", "gj.mannen",
            "pøbel", "russ", "kamphanene", "gjerningsmennene", "mystisk"
        ],
        'good_guy': [
            "politiet", "brannvesenet", "ambulanse", "nødetatene", "tauebil", "bilberger", "OBRE",
            "legevakta", "OKL", "amb.", "vaktbil", "VTS", "helsepersonell", "innsatsleder", "OVA", "vegtrafikksentralen",
            "bombegruppen", "bomegruppa" "politimann", "politimenn", "tjenestemenn",
        ],
        'victim': [
            "fornærmede", "fornærmet", "forn.", "skadede", "offeret", "omkommet", "fotgjenger", "personskade", "syklist", "død",
            "materielle skader", "saknet person", "savnet"
        ],
        'person_description': [
            "CM", "høy", "år", "iført", "har på seg", "ikledd", "sett i", "observert", "mann", "kvinne",
            "jente", "gutt", "ung", "gammel", "eldre", "person",
        ],
        'neturals': [
            "vitne", "vitnet", "publikum",
        ],
        'call_to_action': [
            "har noen sett", "har du sett", "vet du noe om", "har du informasjon", "02800", "leter etter", "søker"
        ],
        'accidents': [
            "ulykke", "trafikkulykke", "trafikkuhell", "uhell", "kollidert", "kjedekollisjon", "påkjørt", "sporet av", "rundkast",
            "utkjøring", "savnet", "kollisjon", "global jihad",
        ],
        'reported': [
            "melding om", "meldinger om", "rapportert", "ukjent skadeomfang", "meldt om", "skal være", "øvelse",
        ],
        'taking_action': [
            "rykker ut", "på vei", "underveis",
        ],
        'damage': [
            "skade", "såre",
        ],
        'resolving': [
            "på stedet", "fremme", "søker området",
            "negativt søk", "evakuerer", "blir på stedet", "rykket ut",
            "avventer", "jobber med", "jobber med", "jobber med å avklare",
        ],
        'resolved': [
            "slukket", "arrestert", "i arrest", "anmeldt", "anmeldelse", "verdensfred", "innbrakt", "anmeldes",
            "evakuert", "ferdig på stedet", "åpen igjen", "åpnet igjen", "veien åpnet", "fri igjen", "udramatisk",
            "avslutter", "drar fra stedet", "beslaglagt", "konfiskert", "pågrepet", "politiarresten", "kontroll på",
            "dimittert", "tauet vekk", "førerkortbeslag", "til rette", "gjenforent", "oppretter sak", "ukadeliggjort",
            "beslag", "beslaglegges", "ryddet veibanen", "forlatt stedet",
        ],
    }
