{{
    config(
        materialized = 'view',
        tags         = ['queries']
    )
}}

select
    dg.genre_name               as genre,
    count(ft.track_id)          as nb_tracks
from {{ ref('fact_track') }}  ft
join {{ ref('dim_genre') }}   dg on ft.genre_id  = dg.genre_id
join {{ ref('dim_album') }}   da on ft.album_id  = da.album_id
where da.production_year between 2000 and 2009
group by dg.genre_id, dg.genre_name
order by nb_tracks desc
limit 1
