{{
    config(
        materialized = 'table',
        tags         = ['star_schema']
    )
}}

select
    artist_id,
    artist_name,
    birth_year,
    country
from {{ ref('stg_artist') }}
