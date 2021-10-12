import re
from datetime import datetime, date
from typing import Union
from enum import Enum
from uuid import UUID, uuid4
from utils.constante import REGEX, BULLET_CONTROL, BLITZ_CONTROL, RAPID_CONTROL
from utils.manager import Manager
from models.player import pm


class Tournament:
    """
    Class representing a tournament

    Attributes:
    - Name : str
    - Place : str
    - Start date : str or datetime.date
    - End date : str or datetime.date
    - Time Control : Bullet/Blitz/Rapid
    - Players : list of players identifiers (must be 8)
    - Description : str
    """
    class Control(Enum):
        BULLET = "Bullet"
        BLITZ = "Blitz"
        RAPID = "Rapid"

    def __init__(self, **params):
        err = []
        if "identifier" not in params:
            params['identifier'] = None
        for property in (
                "name", "place", "start_date", "end_date", "time_control", "players", "description", "identifier"):
            try:
                if property in params:
                    setattr(self, property, params[property])
            except(TypeError, ValueError, AttributeError) as e:
                err.append((property, str(e)))
        if err:
            raise AttributeError(err)

    def __repr__(self):
        return f"Tournament(" \
               f"name = {self._name}, " \
               f"place = {self._place}, " \
               f"start_date = {self._start_date}, " \
               f"end_date = {self._end_date}, " \
               f"time_control = {self._time_control}," \
               f"players = {self._players}, " \
               f"description = {self._description}, " \
               f"identifier = {self._identifier})"

    def __str__(self):
        return f"Tournament: {self._name}\n" \
               f"Place: {self._place}\n" \
               f"Dates: {self._start_date} to {self._end_date}\n" \
               f"Time control: {self._time_control}\n" \
               f"Description: {self._description}"

    def __dict__(self):
        return {"name": self._name,
                "place": self._place,
                "start_date": self._start_date.isoformat(),
                "end_date": self._end_date.isoformat(),
                "time_control": self._time_control,
                "players": self._players,
                "description": self._description,
                "identifier": str(self._identifier)}

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        try:
            matched = re.match(REGEX, value)
            if matched:
                self._name = value.capitalize()
            else:
                raise AttributeError(f"'{value}' is not valid, please enter a valid name.")
        except TypeError:
            raise TypeError(f"'{value}' is not valid, please enter a valid name.")
        except ValueError:
            raise ValueError(f"'{value}' is not valid, please enter a valid name.")

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, value: str):
        try:
            matched = re.match(REGEX, value)
            if matched is not None:
                self._place = value.capitalize()
            else:
                raise AttributeError(f"'{value}' is not valid, please enter a valid place.")
        except TypeError:
            raise TypeError(f"'{value}' is not valid, please enter a valid place.")
        except ValueError:
            raise ValueError(f"'{value}' is not valid, please enter a valid place.")

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value: Union[str, datetime.date]):
        try:
            value = date.fromisoformat(value)
            self._start_date = value
        except ValueError:
            raise ValueError(f"'{value}' is not valid, please enter a valid date (YYYY-MM-DD).")
        except TypeError:
            raise TypeError(f"'{value}' is not valid, please enter a valid date (YYYY-MM-DD).")

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value: Union[str, datetime.date]):
        try:
            value = date.fromisoformat(value)
            if self._start_date > value:
                raise AttributeError("Start date cannot be after end date.")
            self._end_date = value
        except ValueError:
            raise ValueError(f"'{value}' is not valid, please enter a valid date (YYYY-MM-DD).")
        except TypeError:
            raise TypeError(f"'{value}' is not valid, please enter a valid date (YYYY-MM-DD).")

    @property
    def time_control(self):
        return self._time_control

    @time_control.setter
    def time_control(self, value: Union[str, Control]):
        try:
            if value.upper() in BULLET_CONTROL:
                self._time_control = Tournament.Control.BULLET.value
            elif value.upper() in BLITZ_CONTROL:
                self._time_control = Tournament.Control.BLITZ.value
            elif value.upper() in RAPID_CONTROL:
                self._time_control = Tournament.Control.RAPID.value
            else:
                raise AttributeError
        except ValueError:
            raise ValueError(
                f":'{value}' is not valid, please enter a valid time control (Bullet, Blitz or Rapid).")
        except AttributeError:
            raise AttributeError(
                    f":'{value}' is not valid, please enter a valid time control (Bullet, Blitz or Rapid).")

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value: str):
        try:
            if isinstance(value, str):
                self._description = value
            else:
                raise AttributeError
        except AttributeError:
            raise AttributeError(f"{value} must be str")

    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, value: list):
        err = []
        players = []
        if isinstance(value, list):
            try:
                len(value) == 8
            except AttributeError:
                raise AttributeError("Players list must contain 8 players")
            for identifier in value:
                if isinstance(identifier, str):
                    try:
                        identifier = UUID(identifier)
                    except(TypeError, ValueError, AttributeError) as e:
                        err.append(str(e))
                if isinstance(identifier, UUID):
                    if not identifier.version == 4:
                        err.append(f"{identifier} must be uuid4")
                else:
                    err.append(f"{identifier} must be str")
            if err:
                raise AttributeError(err)
            else:
                for identifier in value:
                    player = pm.find(identifier)
                    players.append(str(player.identifier))
                self._players = players
        else:
            raise AttributeError(f"{value} is not a list")

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, value: Union[str, UUID]):
        if not value:
            value = uuid4()
        if isinstance(value, str):
            try:
                value = UUID(value)
            except ValueError:
                raise AttributeError("Value is not uuid")
        if isinstance(value, UUID):
            if not value.version == 4:
                raise AttributeError("uuid must be in version 4.")
            else:
                self._identifier = value
        else:
            raise AttributeError("Value is not str")


tm = Manager(Tournament, "tournaments")
