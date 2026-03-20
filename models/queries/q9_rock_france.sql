{{
    config(
        materialized = 'view',
        tags         = ['queries']
    )
}}

select
    ft.track_name               as morceau,
    dar.artist_name             as artiste,
    dar.country                 as pays,
    dg.genre_name               as genre
from {{ ref('fact_track') }}  ft
join {{ ref('dim_genre') }}   dg  on ft.genre_id  = dg.genre_id
join {{ ref('dim_artist') }}  dar on ft.artist_id = dar.artist_id
where dg.genre_name in ('Rock', 'Rock And Roll')
  and dar.country = 'France'
order by dar.artist_name, ft.track_name
