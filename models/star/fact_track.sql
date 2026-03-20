{{
    config(
        materialized = 'table',
        tags         = ['star_schema']
    )
}}

select
    t.track_id,
    t.track_name,
    t.composer,
    al.album_id,
    ar.artist_id,
    g.genre_id,
    mt.mediatype_id,
    t.milliseconds                          as duration_ms,
    round(t.milliseconds / 60000.0, 2)      as duration_min,
    t.bytes                                 as file_size_bytes,
    t.unit_price
from {{ ref('stg_track') }} t
join {{ ref('stg_album') }}     al  on t.album_id     = al.album_id
join {{ ref('stg_artist') }}    ar  on al.artist_id   = ar.artist_id
join {{ ref('stg_genre') }}     g   on t.genre_id     = g.genre_id
left join {{ ref('stg_mediatype') }} mt on t.mediatype_id = mt.mediatype_id
