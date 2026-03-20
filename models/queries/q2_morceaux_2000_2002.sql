{{
    config(
        materialized = 'view',
        tags         = ['queries']
    )
}}

select
    ft.track_name           as morceau,
    da.album_title          as album,
    da.production_year      as annee_production
from {{ ref('fact_track') }} ft
join {{ ref('dim_album') }}  da on ft.album_id = da.album_id
where da.production_year in (2000, 2002)
order by da.production_year, ft.track_name
