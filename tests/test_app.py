from pathlib import Path
from streamlit.testing.v1 import AppTest


def test_streamlit_app_imports_project_modules():
    text = Path("app.py").read_text(encoding="utf-8")
    assert "run_analysis" in text
    assert "load_csv_url" in text
    assert "Custom CSV URL" in text
    assert "95%" in text
    assert "st.cache_data" in text
    assert "st.cache_resource" in text
    assert "reset_source_state" in text
    assert "hero" in text
    assert "st.tabs" in text


def test_default_problem_ui_and_full_analysis():
    app = AppTest.from_file(Path(__file__).parents[1] / "app.py", default_timeout=30).run()
    assert not app.exception
    assert app.selectbox[0].value.startswith("Problem A")
    app.button[0].click().run(timeout=30)
    assert not app.exception
    assert any("Evaluation" in heading.value for heading in app.subheader)

