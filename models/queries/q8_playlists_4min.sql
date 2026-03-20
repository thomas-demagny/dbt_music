{{
    config(
        materialized = 'view',
        tags         = ['queries']
    )
}}

select distinct
    pl.Name                     as playlist
from MUSIC_EVAL.MUSIC_SCHEMA.PLAYLIST      pl
join MUSIC_EVAL.MUSIC_SCHEMA.PLAYLISTTRACK pt on pl.PlaylistId = pt.PlaylistId
join {{ ref('fact_track') }}               ft on pt.TrackId    = ft.track_id
where ft.duration_ms > 240000
order by pl.Name
