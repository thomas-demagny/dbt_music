with source as (
    select * from MUSIC_EVAL.MUSIC_SCHEMA.ARTIST
)

select
    ArtistId  as artist_id,
    Name      as artist_name,
    Birthyear as birth_year,
    Country   as country
from source
