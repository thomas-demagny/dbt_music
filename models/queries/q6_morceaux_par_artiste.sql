{{
    config(
        materialized = 'view',
        tags         = ['queries']
    )
}}

select
    dar.artist_name                 as artiste,
    count(ft.track_id)              as nb_morceaux
from {{ ref('fact_track') }}  ft
join {{ ref('dim_artist') }}  dar on ft.artist_id = dar.artist_id
group by dar.artist_id, dar.artist_name
order by nb_morceaux desc
