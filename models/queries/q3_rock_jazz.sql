{{
    config(
        materialized = 'view',
        tags         = ['queries']
    )
}}

select
    ft.track_name           as morceau,
    ft.composer             as compositeur,
    dg.genre_name           as genre
from {{ ref('fact_track') }} ft
join {{ ref('dim_genre') }}  dg on ft.genre_id = dg.genre_id
where dg.genre_name in ('Rock', 'Jazz')
order by dg.genre_name, ft.track_name
