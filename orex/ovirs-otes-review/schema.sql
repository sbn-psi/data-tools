/*
Instrument
Status
Filename
Obsdate
Component
ComponentId
Checksum
*/

CREATE TABLE element (
    instrument text,
    loc text,
    proclevel text,
    filepath text,
    obsdate text,
    obsstamp integer,
    component text,
    local_id text,
    sha256sum text
);


create index ix_element on element(instrument, loc, proclevel, obsstamp)