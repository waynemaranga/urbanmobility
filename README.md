# HOWTO:

1. Install packages from the [requirements.txt](./requirements.txt) file
2. Run [populate.py](./populate.py) to create and populate the database
3. Add your keys to an [.env](./.env.example) file or the Streamlit secrets file [secrets.toml](./.streamlit/examplesecrets.toml)
4. Start the Streamlit app with `streamlit run app.py` (or `streamlit run app.py --server.port 8501` if you want to run it on a different port)