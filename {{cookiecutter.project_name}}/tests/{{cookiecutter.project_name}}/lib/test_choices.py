from {{cookiecutter.project_name}}.lib import choices


class TestChoices:
    def test_choices(self):
        class Options(choices.Choices):
            CHOICE1 = "choice1"
            CHOICE2 = "choice2"

        assert Options.random() in Options.values
