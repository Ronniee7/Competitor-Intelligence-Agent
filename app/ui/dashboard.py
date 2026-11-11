import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Competitor Intelligence",
    page_icon="🔎",
    layout="wide",
)

st.title("Competitor Intelligence Agent")

st.caption(
    "AI-powered competitive research and market intelligence."
)

# Sidebar
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select a section",
    [
        "Research",
        "Competitors",
    ],
)

if page == "Research":

    st.header("Research a competitor")

    with st.form("research_form"):

        name = st.text_input("Company name")

        website = st.text_input(
            "Company website",
            placeholder="https://example.com",
        )

        submitted = st.form_submit_button(
            "Start research",
        )

    if submitted:

        if not name or not website:

            st.error("Please provide both fields.")

        else:

            with st.spinner("Researching competitor..."):

                try:

                    response = requests.post(
                        f"{API_URL}/research/competitor",
                        json={
                            "name": name,
                            "website": website,
                        },
                        timeout=180,
                    )

                    response.raise_for_status()

                    result = response.json()

                    st.success("Research completed.")

                    st.json(result)

                    st.session_state["last_competitor_id"] = (
                        result["competitor_id"]
                    )

                except requests.RequestException as exc:

                    st.error(f"Research failed: {exc}")

    competitor_id = st.session_state.get(
        "last_competitor_id"
    )

    if competitor_id:

        if st.button("Generate intelligence report"):

            with st.spinner("Analysing competitor..."):

                try:

                    response = requests.post(
                        f"{API_URL}/analysis/{competitor_id}",
                        timeout=300,
                    )

                    response.raise_for_status()

                    report = response.json()

                    st.success("Analysis completed.")

                    st.subheader("Company intelligence")

                    st.json(report["intelligence"])

                    st.subheader("Generated report")

                    st.markdown(
                        report["markdown_report"]
                    )

                    st.download_button(
                        "Download Markdown report",
                        data=report["markdown_report"],
                        file_name="competitor_report.md",
                        mime="text/markdown",
                    )

                except requests.RequestException as exc:

                    st.error(f"Analysis failed: {exc}")

elif page == "Competitors":

    st.header("Research database")

    if st.button("Refresh competitors"):

        try:

            response = requests.get(
                f"{API_URL}/competitors/",
                timeout=30,
            )

            response.raise_for_status()

            competitors = response.json()

            if competitors:

                st.dataframe(
                    competitors,
                    use_container_width=True,
                )

            else:

                st.info("No competitors researched yet.")

        except requests.RequestException as exc:

            st.error(f"Could not retrieve competitors: {exc}")