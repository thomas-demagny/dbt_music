{{
    config(
        materialized = 'view',
        tags         = ['queries']
    )
}}

select distinct
    da.album_title          as titre_album,
    da.cd_year              as numero_cd_max
from {{ ref('fact_track') }} ft
join {{ ref('dim_album') }}  da on ft.album_id = da.album_id
where da.cd_year = 2
order by da.album_title
