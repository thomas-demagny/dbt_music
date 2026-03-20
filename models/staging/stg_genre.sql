with source as (
    select * from MUSIC_EVAL.MUSIC_SCHEMA.GENRE
)

select
    GenreId as genre_id,
    Name    as genre_name
from source
