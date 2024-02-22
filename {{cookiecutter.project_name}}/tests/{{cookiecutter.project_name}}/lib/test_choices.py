from enum import auto

from cc_bz_project_name.lib import choices


class TestChoices:
    def test_random(self) -> None:
        class Options(choices.Choices):
            CHOICE1 = auto()
            CHOICE2 = auto()

        assert Options.random() in Options

    def test_choices(self) -> None:
        class Options(choices.Choices):
            CHOICE1 = auto()
            CHOICE2 = auto()

        options = Options.choices()
        assert options == sorted(options)
