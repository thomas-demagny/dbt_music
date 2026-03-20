{{
    config(
        materialized = 'table',
        tags         = ['star_schema']
    )
}}

select
    album_id,
    album_title,
    production_year,
    cd_year
from {{ ref('stg_album') }}
