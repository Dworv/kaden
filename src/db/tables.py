guilds_table = """
CREATE TABLE IF NOT EXISTS "guilds" (
    "guild_id"  INTEGER NOT NULL
)
"""

comps_table = """
CREATE TABLE IF NOT EXISTS "comps" (
    "comp_id"   INTEGER NOT NULL,
    "guild_id"  INTEGER NOT NULL,
    "creator_id"    INTEGER NOT NULL,
    "state" INTEGER NOT NULL,
    "name"  TEXT NOT NULL,
    "description"   TEXT NOT NULL,
    "end"   INTEGER NOT NULL,
    "start" INTEGER NOT NULL,
    "criteria1" TEXT,
    "criteria2" TEXT,
    "criteria3" TEXT,
    PRIMARY KEY("comp_id" AUTOINCREMENT)
)
"""

submissions_table = """
CREATE TABLE IF NOT EXISTS "submissions" (
    "submission_id" INTEGER NOT NULL,
    "comp_id" INTEGER NOT NULL,
    "user_id" INTEGER NOT NULL,
    "url"   TEXT NOT NULL,
    "creation_date" INTEGER NOT NULL,
    "score1" INTEGER,
    "score2" INTEGER,
    "score3" INTEGER,
    PRIMARY KEY("submission_id" AUTOINCREMENT)
)
"""
