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
    instrument text, -- the name of the instrument, such as ovirs or otes
    loc text, -- the "location" of the data file. I use existing and delivered
    proclevel text, -- the processing level of the data (raw or calibrated). Could also be used for other things, like geometry
    filepath text, -- the path of the file relative to the bundle
    obsdate text, -- the iso date of the observation
    obsstamp integer, -- the date of the observation, expressed in milliseconds from the epoch
    component text, -- the type of file segment that was evaluated (Table_Binary, Array_3D, etc)
    local_id text, -- the local identifier of the segment, if it was provided
    sha256sum text -- the checksum of the segment
);

/**
If necessary, one could add additional metadata for each segment, such as offset and object_length, by modifying this schema and the ingest script.
*/

-- this index helps match up against similar files more easily
create index ix_element on element(instrument, loc, proclevel, obsstamp)