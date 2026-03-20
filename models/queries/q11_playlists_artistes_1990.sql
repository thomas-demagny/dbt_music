{{
    config(
        materialized = 'view',
        tags         = ['queries']
    )
}}

select distinct
    pl.Name                     as playlist,
    dar.artist_name             as artiste,
    dar.birth_year              as annee_naissance
from MUSIC_EVAL.MUSIC_SCHEMA.PLAYLIST      pl
join MUSIC_EVAL.MUSIC_SCHEMA.PLAYLISTTRACK pt  on pl.PlaylistId = pt.PlaylistId
join {{ ref('fact_track') }}               ft  on pt.TrackId    = ft.track_id
join {{ ref('dim_artist') }}               dar on ft.artist_id  = dar.artist_id
where dar.birth_year is not null
  and dar.birth_year < 1990
order by pl.Name, dar.artist_name
