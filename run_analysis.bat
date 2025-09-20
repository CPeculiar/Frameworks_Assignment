@echo off
echo CORD-19 Data Analysis Project
echo =============================
echo.
echo Installing required packages...
pip install -r requirements.txt
echo.
echo Running main analysis...
python cord19_analysis.py
echo.
echo Analysis complete! Check the generated PNG files for visualizations.
echo.
echo To run the Streamlit app, use: streamlit run streamlit_app.py
pause