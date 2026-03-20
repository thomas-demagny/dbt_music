{{
    config(
        materialized = 'view',
        tags         = ['queries']
    )
}}

select
    dg.genre_name                                   as genre,
    round(avg(ft.file_size_bytes), 0)               as taille_moyenne_bytes,
    round(avg(ft.file_size_bytes) / 1048576.0, 2)   as taille_moyenne_mo
from {{ ref('fact_track') }}  ft
join {{ ref('dim_genre') }}   dg on ft.genre_id = dg.genre_id
where ft.file_size_bytes is not null
group by dg.genre_id, dg.genre_name
order by taille_moyenne_bytes desc
