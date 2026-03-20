import argparse
import os
import sys

try:
    import snowflake.connector
except ImportError:
    print("Erreur : pip install snowflake-connector-python")
    sys.exit(1)

try:
    from tabulate import tabulate
except ImportError:
    print("Erreur : pip install tabulate")
    sys.exit(1)


VIEWS = [
    {
        "num": 1,
        "name": "q1_albums_plus_un_cd",
        "description": "Albums ayant plus d'un CD"
    },
    {
        "num": 2,
        "name": "q2_morceaux_2000_2002",
        "description": "Morceaux produits en 2000 ou 2002"
    },
    {
        "num": 3,
        "name": "q3_rock_jazz",
        "description": "Morceaux de Rock et de Jazz"
    },
    {
        "num": 4,
        "name": "q4_top10_albums_longs",
        "description": "Top 10 albums les plus longs"
    },
    {
        "num": 5,
        "name": "q5_albums_par_artiste",
        "description": "Nombre d'albums par artiste"
    },
    {
        "num": 6,
        "name": "q6_morceaux_par_artiste",
        "description": "Nombre de morceaux par artiste"
    },
    {
        "num": 7,
        "name": "q7_genre_annees_2000",
        "description": "Genre le plus représenté dans les années 2000"
    },
    {
        "num": 8,
        "name": "q8_playlists_4min",
        "description": "Playlists avec morceaux > 4 minutes"
    },
    {
        "num": 9,
        "name": "q9_rock_france",
        "description": "Morceaux Rock dont les artistes sont en France"
    },
    {
        "num": 10,
        "name": "q10_taille_moyenne_genre",
        "description": "Taille moyenne des morceaux par genre"
    },
    {
        "num": 11,
        "name": "q11_playlists_artistes_1990",
        "description": "Playlists avec artistes nés avant 1990"
    },
]

# Connexion Snowflake

def get_connection(args):
    return snowflake.connector.connect(
        account=args.account,
        user=args.user,
        password=args.password,
        role="ACCOUNTADMIN",
        warehouse=args.warehouse,
        database=args.database,
        schema=args.schema,
    )

# Vérification d'une vue

def verify_view(cursor, view_name, database, schema, limit=5):
    sql = f"SELECT * FROM {database}.{schema}.{view_name} LIMIT {limit}"
    cursor.execute(sql)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    # Compte total
    cursor.execute(f"SELECT COUNT(*) FROM {database}.{schema}.{view_name}")
    total = cursor.fetchone()[0]

    return columns, rows, total

# Affichage
def print_result(view, columns, rows, total, limit):
    sep  = "=" * 64
    thin = "-" * 64
    num  = view["num"]
    desc = view["description"]
    name = view["name"]

    print(f"\n{sep}")
    print(f"Q{num}. {desc}")
    print(f"Vue : {name}  |  {total} ligne(s) au total")
    print(thin)

    if total == 0:
        print("Aucun résultat ")
    else:
        print(f"Aperçu ({min(limit, total)} première(s) ligne(s)) :\n")
        print(tabulate(rows, headers=columns, tablefmt="psql"))


# Main

def parse_args():
    parser = argparse.ArgumentParser(description="Vérifie les vues dbt dans Snowflake")
    parser.add_argument("--account",   default=os.getenv("SNOWFLAKE_ACCOUNT"))
    parser.add_argument("--user",      default=os.getenv("SNOWFLAKE_USER"))
    parser.add_argument("--password",  default=os.getenv("SNOWFLAKE_PASSWORD"))
    parser.add_argument("--database",  default="MUSIC_EVAL")
    parser.add_argument("--schema",    default="MUSIC_SCHEMA")
    parser.add_argument("--warehouse", default="EXAM_WAREHOUSE")
    parser.add_argument("--limit",     default=5, type=int,
                        help="Nombre de lignes à afficher par vue (défaut: 5)")
    return parser.parse_args()


def main():
    args = parse_args()

    missing = [k for k in ("account", "user", "password")
               if not getattr(args, k)]
    if missing:
        print(f"Paramètres manquants : {', '.join(missing)}")
        print("Utilisez --account, --user, --password ou les variables d'environnement")
        sys.exit(1)

    print(f"Connexion à Snowflake ({args.database}.{args.schema})...")
    conn = get_connection(args)
    cursor = conn.cursor()
    print("Connecté.\n")

    ok    = []
    empty = []
    error = []

    for view in VIEWS:
        print(f"  Vérification Q{view['num']:2d}. {view['name']}...", end=" ", flush=True)
        try:
            columns, rows, total = verify_view(
                cursor, view["name"], args.database, args.schema, args.limit
            )
            print(f"{total} ligne(s)")
            print_result(view, columns, rows, total, args.limit)
            if total == 0:
                empty.append(view["name"])
            else:
                ok.append(view["name"])
        except Exception as e:
            print(f"ERREUR")
            print(f"\n{'='*64}")
            print(f"Q{view['num']}. {view['description']} — ERREUR")
            print(f"{e}")
            error.append(view["name"])

    cursor.close()
    conn.close()

    # Résumé final
    print(f"\n{'='*64}")
    print(f"RÉSUMÉ — {len(VIEWS)} vues vérifiées")
    print(f"{'='*64}")
    print(f" OK      : {len(ok):2d} vues")
    print(f" Vides   : {len(empty):2d} vues  {empty if empty else ''}")
    print(f" Erreurs : {len(error):2d} vues  {error if error else ''}")
    print(f"{'='*64}\n")


if __name__ == "__main__":
    main()
