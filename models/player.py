import re
from datetime import datetime, date
from typing import Union
from enum import Enum
from utils.constante import REGEX, GENDER_M, GENDER_F, MIN, MAX
from uuid import UUID, uuid4
from utils.manager import Manager


class Player:
    """
    Class representing a player
    Attributes:
    - Name
    - Last name
    - Birthdate
    - Gender
    - Rank
    """
    class Gender(Enum):
        MALE = "Male"
        FEMALE = "Female"

    def __init__(self, **params):
        err = []
        if "identifier" not in params:
            params['identifier'] = None
        for property in ("first_name", "last_name", "birthdate", "gender", "rank", "identifier"):
            try:
                if property in params:
                    setattr(self, property, params[property])
            except(TypeError, ValueError, AttributeError) as e:
                err.append((property, str(e)))
        if err:
            raise AttributeError(err)

    def __repr__(self):
        return f"Player(" \
               f"first_name = {self.first_name}, " \
               f"last_name = {self.last_name}, " \
               f"birthdate = {self.birthdate}, " \
               f"gender = {self.gender}, " \
               f"rank = {self.rank}, " \
               f"identifier = {self.identifier})"

    def __str__(self):
        return f"First name: {self._first_name}\n" \
               f"Lastname: {self._last_name}\n" \
               f"Gender: {self._gender}\n" \
               f"Birthdate: {self._birthdate}\n" \
               f"Rank: {self._rank}\n" \
               f"Identifier: {self._identifier}"

    def __dict__(self):
        return {"first_name": self._first_name,
                "last_name": self._last_name,
                "birthdate": self._birthdate.isoformat(),
                "gender": self._gender,
                "rank": self._rank,
                "identifier": str(self._identifier)}

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        try:
            matched = re.match(REGEX, value)
            if matched is not None:
                self._first_name = value.capitalize()
            else:
                raise AttributeError(f"{value} is not valid, please enter a valid firstname.")
        except TypeError:
            raise TypeError(f"'{value}' is not valid, please enter a valid lastname.")
        except ValueError:
            raise ValueError(f"'{value}' is not valid, please enter a valid lastname.")

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        try:
            matched = re.match(REGEX, value)
            if matched is not None:
                self._last_name = value.capitalize()
            else:
                raise AttributeError(f"'{value}' is not valid, please enter a valid lastname.")
        except TypeError:
            raise TypeError(f"'{value}' is not valid, please enter a valid lastname.")
        except ValueError:
            raise ValueError(f"'{value}' is not valid, please enter a valid lastname.")

    @property
    def birthdate(self):
        return self._birthdate

    @birthdate.setter
    def birthdate(self, value: Union[str, datetime.date]):
        try:
            value = date.fromisoformat(value)
            today = date.today()
            check_age = int(str(today - value).split(" ")[0])
            if check_age >= 4382:
                self._birthdate = value
            else:
                raise AttributeError("This person is too young to participate at this tournament...")
        except ValueError:
            raise ValueError(f"'{value}' is not valid, please enter a valid birthdate (YYYY-MM-DD).")
        except TypeError:
            raise TypeError(f"'{value}' is not valid, please enter a valid birthdate (YYYY-MM-DD).")

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value: Union[str, Gender]):
        try:
            if value.upper() in GENDER_M:
                self._gender = Player.Gender.MALE.value
            elif value.upper() in GENDER_F:
                self._gender = Player.Gender.FEMALE.value
            else:
                raise AttributeError(f":'{value}' is not valid, please enter a valid gender (m/f).")
        except ValueError:
            raise ValueError(f":'{value}' is not valid, please enter a valid gender (m/f).")

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, value: int):
        try:
            if value in range(MIN, MAX):
                self._rank = value
            else:
                raise AttributeError(f"'{value}' is not valid, please enter a valid rank (between 1000 and 3000).")
        except ValueError:
            raise ValueError(f"'{value}' is not valid, please enter a valid rank (between 1000 and 3000).")

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


pm = Manager(Player, "players_db.json")
