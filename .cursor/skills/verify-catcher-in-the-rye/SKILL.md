# Verify CatcherInTheRye
Catcher in the Rye dashboard - streamlit explorer of characters, symbols and themes (graphviz).
## Launch
pip install streamlit graphviz, then streamlit run catcher_dashboard.py.
## Doctor
`python3 .cursor/skills/verify-catcher-in-the-rye/verify.py`
## Drive
Compiles every python module, then boots the streamlit dashboard headless and asserts it serves the app.
## Evidence
`.cursor/skills/verify-catcher-in-the-rye/evidence.json`
## Cleanup
Static/streamlit server terminated after the render.
## Known boundaries
Render smoke only; scene quality and e2e suites not exercised here.
