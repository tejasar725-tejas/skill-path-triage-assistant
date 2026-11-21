from app.cli import main


def test_cli_suggestions(capsys):
    assert main(["--skills", "Python, SQL", "--top-n", "3"]) == 0
    output = capsys.readouterr().out
    assert "Suggested next skills" in output


def test_cli_evaluate(capsys):
    assert main(["--evaluate"]) == 0
    assert "top1_accuracy" in capsys.readouterr().out
