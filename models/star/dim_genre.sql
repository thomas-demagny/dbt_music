{{
    config(
        materialized = 'table',
        tags         = ['star_schema']
    )
}}

select
    genre_id,
    genre_name
from {{ ref('stg_genre') }}
