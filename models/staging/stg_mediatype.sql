with source as (
    select * from MUSIC_EVAL.MUSIC_SCHEMA.MEDIATYPE
)

select
    MediaTypeId as mediatype_id,
    Name        as mediatype_name
from source
