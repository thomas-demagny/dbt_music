with source as (
    select * from MUSIC_EVAL.MUSIC_SCHEMA.ALBUM
)

select
    AlbumId   as album_id,
    Title     as album_title,
    ArtistId  as artist_id,
    Prod_year as production_year,
    Cd_year   as cd_year
from source
