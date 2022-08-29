import pathlib
import sqlite3

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
            "INSERT INTO comps (guild_id, creator_id, state, name, description, end) values (?, ?, ?, ?, ?, ?) RETURNING comp_id",
            (guild_id, creator_id, CompState.SUBMIT.value, name, description, end),
        )
        comp_id = next(res)
        self.conns["comps"].commit()
        return comp_id
    
    def set_comp_state(self, comp_id: int, state: CompState):
        print(type(comp_id), type(state))
        self.curs["comps"].execute("UPDATE comps SET state = ? WHERE comp_id = ?", (state.value, comp_id))
        self.conns["comps"].commit()

    def get_comp(self, comp_id):
        self.curs["comps"].execute("SELECT * FROM comps WHERE comp_id = ?", (comp_id,))
        res = self.curs["comps"].fetchone()
        self.conns["comps"].commit()
        return res
    
    def get_guild_comps(self, guild_id, state: CompState = None):
        self.curs["comps"].execute("SELECT * FROM comps WHERE guild_id = ?", (guild_id,))
        res = self.curs["comps"].fetchall()
        self.conns["comps"].commit()
        return [comp for comp in res if comp[3] == state.value] if isinstance(state, CompState) else res

database = DBClient()
