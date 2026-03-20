with source as (
    select * from MUSIC_EVAL.MUSIC_SCHEMA.TRACK
)

select
    TrackId     as track_id,
    Name        as track_name,
    Composer    as composer,
    AlbumId     as album_id,
    GenreId     as genre_id,
    MediaTypeId as mediatype_id,
    Milliseconds as milliseconds,
    Bytes       as bytes,
    UnitPrice   as unit_price
from source
