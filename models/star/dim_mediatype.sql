{{
    config(
        materialized = 'table',
        tags         = ['star_schema']
    )
}}

select
    mediatype_id,
    mediatype_name
from {{ ref('stg_mediatype') }}
