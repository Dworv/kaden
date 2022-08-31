import pathlib
import sqlite3
import time

from .tables import comps_table, guilds_table, submissions_table
from .enums import CompState


class DBClient:
    def __init__(self):
        tables = {
            "comps": comps_table,
            "guilds": guilds_table,
            "submissions": submissions_table,
        }
        self.conns = {
            table: sqlite3.connect(pathlib.Path(__file__).parent / f"{table}.db")
            for table in tables
        }
        self.curs = {table: self.conns[table].cursor() for table in tables}
        for table in tables:
            self.curs[table].execute(tables[table])

    def create_competition(self, guild_id, creator_id, name, description, end):
        res = self.curs["comps"].execute(
            "INSERT INTO comps (guild_id, creator_id, state, name, description, end, start) values (?, ?, ?, ?, ?, ?, ?) RETURNING comp_id",
            (
                guild_id,
                creator_id,
                CompState.SUBMIT.value,
                name,
                description,
                end,
                int(time.time())
            ),
        )
        comp_id = next(res)[0]
        self.conns["comps"].commit()
        return comp_id

    def set_comp_state(self, comp_id: int, state: CompState):
        self.curs["comps"].execute(
            "UPDATE comps SET state = ? WHERE comp_id = ?", (state.value, comp_id)
        )
        self.conns["comps"].commit()

    def set_comp_criteria(self, comp_id: int, criterias: list[str]):
        self.curs["comps"].execute(
            "UPDATE comps SET (criteria1, criteria2, criteria3) = (?, ?, ?) WHERE comp_id = ?", (*criterias, comp_id)
        )
        self.conns["comps"].commit()

    def get_comp(self, comp_id):
        self.curs["comps"].execute("SELECT * FROM comps WHERE comp_id = ?", (comp_id,))
        return self.curs["comps"].fetchone()

    def get_guild_comps(self, guild_id, state: CompState = None):
        if state is not None:
            self.curs["comps"].execute(
                "SELECT * FROM comps WHERE guild_id = ? AND state = ?",
                (guild_id, state.value),
            )
        else:
            self.curs["comps"].execute(
                "SELECT * FROM comps WHERE guild_id = ?", (guild_id,)
            )
        return self.curs["comps"].fetchall()

    def extend_comp_end(self, comp_id, length):
        self.curs["comps"].execute(
            "UPDATE comps SET end = end + ? WHERE comp_id = ?", (length, comp_id)
        )
        self.conns["comps"].commit()

    def create_submission(self, comp_id, user_id, url):
        res = self.curs["submissions"].execute(
            "INSERT INTO submissions (comp_id, user_id, url, creation_date) values (?, ?, ?, ?) RETURNING submission_id",
            (comp_id, user_id, url, time.time()),
        )
        submission_id = next(res)
        self.conns["submissions"].commit()
        return submission_id

    def set_submission_score(self, submission_id, scores: list[float]):
        self.curs["submissions"].execute(
            "UPDATE submissions SET (score1, score2, score3) = (?, ?, ?) WHERE comp_id = ?", (*scores, submission_id)
        )
        self.conns["submissions"].commit()

    def get_submission(self, submission_id):
        self.curs["submissions"].execute(
            "SELECT * FROM submissions WHERE submission_id = ?", (submission_id,)
        )
        return self.curs["submissions"].fetchone()

    def get_comp_submissions(self, comp_id, scored: bool = None):
        # sourcery skip: simplify-boolean-comparison
        if scored is True:
            self.curs["submissions"].execute(
                "SELECT * FROM comps WHERE guild_id = ? AND NOT score = ?", (comp_id, 0)
            )
        if scored is False:
            self.curs["submissions"].execute(
                "SELECT * FROM comps WHERE guild_id = ? AND score = ?", (comp_id, 0)
            )
        else:
            self.curs["submissions"].execute(
                "SELECT * FROM comps WHERE guild_id = ?", (comp_id,)
            )

        return self.curs["submissions"].fetchall()


database = DBClient()
