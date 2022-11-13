"""
File containing real word generator class.

Classes:
    RealGenerator(Generator)
"""

from typing import List

from playwright.sync_api import Locator, Page, expect, sync_playwright

from ..response import LetterValidity
from .generator import Generator


class RealGenerator(Generator):
    """
    Real word generator class.

    ...

    Attributes
    ----------
    GUESSES : int
        Number of guesses allowed
    ACTION_SPACE : spaces.Discrete
        Actions allowed
    OBSERVATION_SPACE : spaces.Discrete
        Possible observations
    PLAYWRIGHT : Playwright
        Playwright instance
    PAGE_URL : str
        Url to wordle site
    PAGE_WIDTH : int
        Width to render page at
    PAGE_HEIGHT : int
        Height to render page at
    DATA_STATE_TO_VALIDITY : Dict[str, LetterValidity]
        Dictionary containing mappings from cell states to LetterValidities

    Properties
    ----------
    done : bool
        Whether the game has ended
    guesses_remaining : int
        Remaining guesses

    Methods
    -------
    reset(self) -> None
        Reset the environment
    step(self, action: int) -> Tuple[List[int], float, bool, dict]
        Perform given action
    observe(self) -> List[int]
        Observe current state
    """

    PLAYWRIGHT = sync_playwright().start()
    PAGE_URL = "https://www.nytimes.com/games/wordle/index.html"
    PAGE_WIDTH = 1920
    PAGE_HEIGHT = 1080
    DATA_STATE_TO_VALIDITY = {
        "absent": LetterValidity.GREY,
        "present": LetterValidity.YELLOW,
        "correct": LetterValidity.GREEN,
    }

    def __init__(self) -> None:
        """Initialise object."""
        super().__init__()

        self._tab = self._new_tab()
        self._open_page()

    def reset(self) -> List[int]:
        """
        Reset the environment.

        Returns
        -------
        List[int]
        """
        self._tab = self._new_tab()
        self._open_page()

        return super().reset()

    @classmethod
    def _new_tab(cls) -> Page:
        return cls.PLAYWRIGHT.chromium.launch().new_page(
            viewport={"width": cls.PAGE_WIDTH, "height": cls.PAGE_HEIGHT}
        )

    def _open_page(self) -> None:
        self._tab.goto(self.PAGE_URL)
        if (button := self._tab.locator("#pz-gdpr-btn-reject")).is_visible():
            button.click()
        self._tab.locator('[data-testid="icon-close"]').click()
        expect(self._tab.locator('[data-testid="modal-overlay"]')).to_be_hidden()

    def _guess_word(self, guess: str) -> List[LetterValidity]:
        self._enter(guess)
        self._wait_for_cell(4)

        return [self._letter_validity(pos) for pos in range(len(guess))]

    def _enter(self, guess: str) -> None:
        self._tab.keyboard.type(guess)
        self._tab.keyboard.press("Enter")

    def _wait_for_cell(self, idx: int) -> None:
        expect(self._cell(idx)).not_to_have_attribute("data-state", "empty")
        expect(self._cell(idx)).not_to_have_attribute("data-state", "tbd")

    def _letter_validity(self, pos: int) -> LetterValidity:
        return self.DATA_STATE_TO_VALIDITY[
            str(self._cell(pos).get_attribute("data-state"))
        ]

    def _cell(self, idx: int) -> Locator:
        return (
            self._tab.locator(f'[aria-label="Row {self._current_row}"]')
            .locator(".Tile-module_tile__3ayIZ")
            .nth(idx)
        )

    @property
    def _current_row(self) -> int:
        return self.GUESSES - self._guesses_remaining + 1

    def render(self, _: str = "human") -> None:
        """[NOT IMPLEMENTED] Render current state."""
        raise NotImplementedError(
            "Rendering has not been implemented for this environment"
        )
