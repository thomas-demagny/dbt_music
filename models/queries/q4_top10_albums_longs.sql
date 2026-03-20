{{
    config(
        materialized = 'view',
        tags         = ['queries']
    )
}}

select
    da.album_title                          as titre_album,
    sum(ft.duration_ms)                     as duree_totale_ms,
    round(sum(ft.duration_min), 2)          as duree_totale_min,
    count(ft.track_id)                      as nb_tracks
from {{ ref('fact_track') }} ft
join {{ ref('dim_album') }}  da on ft.album_id = da.album_id
group by da.album_id, da.album_title
order by duree_totale_ms desc
limit 10
