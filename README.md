# Work Hours Logger

This is a modern web application built with [Streamlit](https://streamlit.io) that allows you to log your work shifts, track paid/unpaid vacation, visualize overtime hours, and manage your shift history easily with plots and summaries. All data is stored using SQLite for convenience and portability.

## Features

- Add, view, and edit shifts, with clock-in/clock-out times via time pickers
- Track both paid and unpaid vacation (with appropriate handling of hours/overtime)
- See monthly and overall summaries, and visualize via pie/bar charts using Plotly
- Personalized account settings (default hours, vacation days, etc.)
- Secure, per-user login
- Data never leaves your device/server (unless you run on Streamlit Cloud)



## Installation

1. **Clone this repository:**

    ```bash
    git clone https://github.com/<your-username>/<your-repo>.git
    cd <your-repo>
    ```

2. **(Recommended) Create & activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the app locally:**

    ```bash
    streamlit run app.py
    ```

## Deploy on Streamlit Community Cloud

- Push your repository to GitHub (see below).
- Go to https://streamlit.io/cloud and connect your repository.
- Set `app.py` as your main file and deploy.
- (Optional) Use Streamlit secrets for per-user configuration.

## Contributing

Contributions and suggestions are welcome!  
Feel free to open a pull request or issue.

---

## GitHub Push Instructions

1. **Init and commit your local repo:**

    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    ```

2. **Add your remote (replace with your GitHub URL):**

    ```bash
    git remote add origin https://github.com/<your-username>/<your-repo>.git
    ```

3. **Push to GitHub:**

    ```bash
    git branch -M main
    git push -u origin main
    ```

---

## License

MIT License (or specify your license)



