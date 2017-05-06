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
            "ingen skade", "ikke tegn", "mangler",
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
            "under påvirkning", "ordensforstyrrelse", "ranet", "fraranet", "ruspåvirket", "bråk", "slått", "innbrudd",
            "innbruddsforsøk", "tent på", "tagging", "tagget", "herværk", "vandalisme", "støy", "husbråk", "trussel", "trusler",
            "skallet ned", "kaste", "slåss", "banket opp", "true", "kaster", "kastet", "bråk",
            "kamp", "vikeplikt", "usikret", "naken", "slossing", "tømt", "påtent", "narkotika", "hasj", "alkohol",
            "cannabis", "amfetamin", "kokain", "dop",
            "promille", "kroppskade", "ruset", "luske", "barke", "vold", "bite", "bitt", "promille",
            "terror",
        ],
        'weapon': [
            "kniv", "pistol", "våpen", "gevær", "rifle", "hagle", "skytevåpen", "hammer", "øks", "machete",
            "skarp gjenstand", "flaske",
        ],
        'prank': [  # vettafan hvæ denna burde heti
            "guttestreker", "spøk", "prank", "tull", "påfunn", "plages", "plaget"
        ],
        'animal': [
            "hund", "katt", "valp", "hest", "kattunge",
        ],
        'bad_guy': [
            "tyv", "morder", "mistenkt", "mistenkelig", "vinningskriminell", "innbruddstyv", "biltyv",
            "gjerningsmannen", "gj.mannen",
            "pøbel", "russ", "kamphanene", "gjerningsmennene", "mystisk"
        ],
        'good_guy': [
            "politi", "brannvesen", "ambulanse", "nødetat", "tauebil", "bilberg", "OBRE",
            "legevakt", "OKL", "amb.", "vaktbil", "VTS", "helsepersonell", "innsatsleder", "OVA", "vegtrafikksentralen",
            "bombegrupp", "politimann", "politimenn", "tjenestemenn", "sykehus",
        ],
        'victim': [
            "fornærmede", "fornærmet", "forn.", "skadede", "offeret", "omkommet", "fotgjenger", "personskade",
            "syklist",
        ],
        'person_description': [
            "CM høy", "år gammel", "iført", "har på seg", "ikledd", "sett i", "mann", "kvinne",
            "jente", "gutt", "ung", "eldre", "person", "pensjonist", "politimann", "norsk", "afrikansk",
            "arabisk", "hvit", "asiatisk", "teit", "svensk",
        ],
        'missing': [
            'savnet', 'savner', 'sist sett', 'sist observert'
        ],
        'neturals': [
            "vitne", "vitnet", "publikum",
        ],
        'call_to_action': [
            "har noen sett", "har du sett", "vet du noe om", "har du informasjon", "02800", "leter etter",
        ],
        'vehicle': [
            "buss", "lastebil", "trailer", "personbil", "MC", "motorsykkel",
        ],
        'residence': [
            "leilighet", "enebolig", "hjemme hos", "hybel", "blokk", "villa", "bygget"
        ],
        'accidents': [
            "ulykke", "trafikkulykke", "trafikkuhell", "uhell", "kollidert", "kjedekollisjon", "påkjørt", "sporet av", "rundkast",
            "utkjøring", "savnet", "kollisjon", "global jihad",
        ],
        'reported': [
            "melding om", "meldinger om", "rapportert", "ukjent skadeomfang", "meldt om", "skal være", "øvelse",
            "klager om", "flere klager"
        ],
        'taking_action': [
            "rykker ut", "på vei", "underveis",
        ],
        'damage': [
            "skade", "såre", "kritisk skadet", "omkommet", "død", "drept", "slått seg", "vondt i", "smerte"
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
            "beslag", "beslaglegges", "ryddet veibanen", "forlatt stedet", "opphevet", "åpen for trafikk",
            "normal trafikk",
        ],
    }
