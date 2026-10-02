import streamlit as st
import pandas as pd
import plotly.express as px

from core.ingestion import read_uploaded_file, IngestionError
from core.profiling import profile_dataframe
from core.cleaning import clean_dataframe
from core.mapping import resolve_column_mappings, summarize_transformations
from core.analytics import (
    calculate_summary,
    calculate_category_analysis,
    calculate_trend_analysis,
    generate_summary_insights,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Budget Variance Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>
.stApp {
    background-color: #F7F8FC;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #172033;
}

.hero-card {
    background: linear-gradient(
        135deg,
        #EEF0FF 0%,
        #F8F9FC 55%,
        #EAF7F2 100%
    );
    border: 1px solid #E4E7EC;
    border-radius: 22px;
    padding: 38px;
    margin-bottom: 28px;
}

.upload-info-card {
    background: #FFFFFF;
    border: 1px solid #EAECF0;
    border-radius: 18px;
    padding: 26px;
    margin-top: 20px;
}

.footer {
    text-align: center;
    color: #98A2B3;
    font-size: 12px;
    padding-top: 30px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "raw_df" not in st.session_state:
    st.session_state.raw_df = None

if "clean_df" not in st.session_state:
    st.session_state.clean_df = None

if "profile" not in st.session_state:
    st.session_state.profile = None

if "transformations" not in st.session_state:
    st.session_state.transformations = []

if "mappings" not in st.session_state:
    st.session_state.mappings = {}

if "view" not in st.session_state:
    st.session_state.view = "upload"

if "file_name" not in st.session_state:
    st.session_state.file_name = None


# ============================================================
# HELPERS
# ============================================================

def reset_application():
    st.session_state.raw_df = None
    st.session_state.clean_df = None
    st.session_state.profile = None
    st.session_state.transformations = []
    st.session_state.mappings = {}
    st.session_state.view = "upload"
    st.session_state.file_name = None


def format_number(value):
    if value is None:
        return "—"

    try:
        return f"{float(value):,.2f}"
    except Exception:
        return str(value)


def format_percentage(value):
    if value is None:
        return "—"

    try:
        return f"{float(value):,.2f}%"
    except Exception:
        return str(value)


def process_file(uploaded_file):

    raw_df = read_uploaded_file(
        uploaded_file.getvalue(),
        uploaded_file.name,
    )

    if raw_df.empty:
        raise ValueError(
            "The uploaded file contains no data."
        )

    profile = profile_dataframe(raw_df)

    clean_df, transformations = clean_dataframe(
        raw_df
    )

    mappings = resolve_column_mappings(
        list(clean_df.columns)
    )

    st.session_state.raw_df = raw_df
    st.session_state.clean_df = clean_df
    st.session_state.profile = profile
    st.session_state.transformations = transformations
    st.session_state.mappings = mappings
    st.session_state.file_name = uploaded_file.name
    st.session_state.view = "understand"


# ============================================================
# UPLOAD SCREEN
# ============================================================

if st.session_state.clean_df is None:

    st.html(
        """
        <div class="hero-card">

            <div style="
                color:#6875E8;
                font-size:13px;
                font-weight:700;
                letter-spacing:1.5px;
                margin-bottom:10px;
            ">
                FP&A ANALYTICS WORKSPACE
            </div>

            <div style="
                color:#172033;
                font-size:38px;
                font-weight:750;
                line-height:1.15;
                margin-bottom:12px;
            ">
                Budget Variance Analyzer
            </div>

            <div style="
                color:#667085;
                font-size:16px;
                line-height:1.6;
                max-width:720px;
            ">
                Transform financial data into structured analysis,
                variance insights and decision-ready answers.
            </div>

        </div>
        """
    )

    st.subheader("Upload your financial data")

    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file",
        type=["csv", "xlsx", "xls"],
        help="Supported formats: CSV, XLSX and XLS.",
    )

    if uploaded_file is not None:

        if st.session_state.file_name != uploaded_file.name:

            with st.spinner("Preparing your data..."):

                try:

                    process_file(
                        uploaded_file
                    )

                except IngestionError as exc:

                    st.error(str(exc))
                    st.stop()

                except Exception as exc:

                    st.error(
                        f"Unable to process the file: {exc}"
                    )
                    st.stop()

            st.rerun()

    st.html(
        """
        <div class="upload-info-card">

            <div style="
                color:#172033;
                font-size:18px;
                font-weight:700;
                margin-bottom:18px;
            ">
                What you can do
            </div>

            <div style="
                color:#475467;
                line-height:1.7;
            ">

                <b>① Understand Your Data</b>
                <br>
                Review structure, quality, missing values,
                duplicates and transformations.

                <br><br>

                <b>② Analyze Your Data</b>
                <br>
                Explore budget vs actual, category performance
                and financial trends.

                <br><br>

                <b>③ Ask a Question</b>
                <br>
                Ask targeted questions about your financial
                dataset using AI.

            </div>

        </div>
        """
    )

    st.stop()


# ============================================================
# APPLICATION HEADER
# ============================================================

header_left, header_right = st.columns(
    [5, 1]
)

with header_left:

    st.html(
        f"""
        <div style="
            color:#172033;
            font-size:27px;
            font-weight:750;
        ">
            Budget Variance Analyzer
        </div>

        <div style="
            color:#667085;
            font-size:14px;
            margin-top:4px;
        ">
            📄 {st.session_state.file_name}
        </div>
        """
    )

with header_right:

    if st.button(
        "New File",
        use_container_width=True,
    ):

        reset_application()
        st.rerun()


st.divider()


# ============================================================
# NAVIGATION
# ============================================================

nav1, nav2, nav3 = st.columns(3)

with nav1:

    if st.button(
        "Understand Your Data",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.view == "understand"
            else "secondary"
        ),
    ):

        st.session_state.view = "understand"
        st.rerun()


with nav2:

    if st.button(
        "Analyze Your Data",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.view == "analyze"
            else "secondary"
        ),
    ):

        st.session_state.view = "analyze"
        st.rerun()


with nav3:

    if st.button(
        "Ask a Question",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.view == "question"
            else "secondary"
        ),
    ):

        st.session_state.view = "question"
        st.rerun()


st.divider()


# ============================================================
# DATA REFERENCES
# ============================================================

df = st.session_state.clean_df

mappings = st.session_state.mappings

budget_column = mappings.get("budget")
actual_column = mappings.get("actual")
category_column = mappings.get("category")
date_column = mappings.get("date")


# ============================================================
# UNDERSTAND YOUR DATA
# ============================================================

if st.session_state.view == "understand":

    st.header("Understand Your Data")

    st.caption(
        "Review the structure, quality and preparation "
        "of the uploaded dataset."
    )

    profile = profile_dataframe(df)

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Rows",
            f"{profile['row_count']:,}",
        )

    with col2:

        st.metric(
            "Columns",
            f"{profile['column_count']:,}",
        )

    with col3:

        st.metric(
            "Missing Values",
            f"{profile['total_missing_values']:,}",
        )

    with col4:

        st.metric(
            "Duplicate Rows",
            f"{profile['duplicate_rows']:,}",
        )

    st.markdown("### Column Overview")

    column_rows = []

    for column in profile["columns"]:

        column_rows.append(
            {
                "Column": column["name"],
                "Type": column["data_type"],
                "Missing": column["missing_values"],
                "Missing %": (
                    f"{column['missing_percentage']:.2f}%"
                ),
                "Unique Values": column["unique_values"],
            }
        )

    st.dataframe(
        pd.DataFrame(column_rows),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### Data Preparation")

    transformation_summary = summarize_transformations(
        st.session_state.transformations
    )

    if transformation_summary["total_changes"] == 0:

        st.success(
            "No automatic transformations were required."
        )

    else:

        st.info(
            transformation_summary["summary"]
        )

        for item in transformation_summary["items"]:

            st.write(
                f"• {item['description']}"
            )

    st.markdown("### Data Preview")

    st.dataframe(
        df.head(100),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# ANALYZE YOUR DATA
# ============================================================

elif st.session_state.view == "analyze":

    st.header("Analyze Your Data")

    st.caption(
        "Choose the type of financial analysis you want to perform."
    )

    analysis_type = st.selectbox(
        "Analysis",
        [
            "Overall Analysis",
            "Budget vs Actual",
            "Category Performance",
            "Trend Analysis",
        ],
        index=0,
    )

    st.divider()


    # ========================================================
    # OVERALL ANALYSIS
    # ========================================================

    if analysis_type == "Overall Analysis":

        st.subheader("Executive Overview")

        if budget_column and actual_column:

            summary = calculate_summary(
                df,
                budget_column,
                actual_column,
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "Total Budget",
                    format_number(
                        summary["total_budget"]
                    ),
                )

            with col2:

                st.metric(
                    "Total Actual",
                    format_number(
                        summary["total_actual"]
                    ),
                )

            with col3:

                st.metric(
                    "Total Variance",
                    format_number(
                        summary["total_variance"]
                    ),
                )

            with col4:

                st.metric(
                    "Variance %",
                    format_percentage(
                        summary["variance_percentage"]
                    ),
                )

            st.markdown("### Key Observations")

            insights = generate_summary_insights(
                summary
            )

            for insight in insights:

                st.info(insight)

            if category_column:

                st.markdown(
                    "### Category Performance"
                )

                try:

                    category_df = calculate_category_analysis(
                        df,
                        category_column,
                        budget_column,
                        actual_column,
                    )

                    st.dataframe(
                        category_df,
                        use_container_width=True,
                        hide_index=True,
                    )

                    fig = px.bar(
                        category_df,
                        x=category_column,
                        y="Variance",
                        title="Variance by Category",
                    )

                    fig.update_layout(
                        template="plotly_white",
                        height=420,
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True,
                    )

                except Exception as exc:

                    st.warning(
                        f"Category analysis unavailable: {exc}"
                    )

            if date_column:

                st.markdown("### Financial Trend")

                try:

                    trend_df = calculate_trend_analysis(
                        df,
                        date_column,
                        budget_column,
                        actual_column,
                    )

                    if not trend_df.empty:

                        fig = px.line(
                            trend_df,
                            x="Period",
                            y=["Budget", "Actual"],
                            markers=True,
                            title="Budget vs Actual Trend",
                        )

                        fig.update_layout(
                            template="plotly_white",
                            height=420,
                        )

                        st.plotly_chart(
                            fig,
                            use_container_width=True,
                        )

                    else:

                        st.info(
                            "No usable date information was found."
                        )

                except Exception as exc:

                    st.warning(
                        f"Trend analysis unavailable: {exc}"
                    )

        else:

            st.warning(
                "Budget and Actual columns could not be "
                "identified automatically."
            )

            st.info(
                "The application does not silently guess "
                "financial column meanings."
            )


    # ========================================================
    # BUDGET VS ACTUAL
    # ========================================================

    elif analysis_type == "Budget vs Actual":

        st.subheader("Budget vs Actual")

        if budget_column and actual_column:

            result = df.copy()

            result["Variance"] = (
                result[actual_column]
                - result[budget_column]
            )

            result["Variance %"] = (
                result["Variance"]
                / result[budget_column].replace(
                    0,
                    pd.NA,
                )
            ) * 100

            st.dataframe(
                result,
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.warning(
                "Budget and Actual columns could not "
                "be identified."
            )


    # ========================================================
    # CATEGORY PERFORMANCE
    # ========================================================

    elif analysis_type == "Category Performance":

        st.subheader("Category Performance")

        if (
            budget_column
            and actual_column
            and category_column
        ):

            try:

                category_df = calculate_category_analysis(
                    df,
                    category_column,
                    budget_column,
                    actual_column,
                )

                st.dataframe(
                    category_df,
                    use_container_width=True,
                    hide_index=True,
                )

                fig = px.bar(
                    category_df,
                    x=category_column,
                    y="Variance",
                    title="Variance by Category",
                )

                fig.update_layout(
                    template="plotly_white",
                    height=420,
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )

            except Exception as exc:

                st.error(
                    f"Unable to generate category analysis: {exc}"
                )

        else:

            st.warning(
                "Category, Budget and Actual columns "
                "could not all be identified."
            )


    # ========================================================
    # TREND ANALYSIS
    # ========================================================

    elif analysis_type == "Trend Analysis":

        st.subheader("Trend Analysis")

        if (
            budget_column
            and actual_column
            and date_column
        ):

            try:

                trend_df = calculate_trend_analysis(
                    df,
                    date_column,
                    budget_column,
                    actual_column,
                )

                if trend_df.empty:

                    st.warning(
                        "No usable dates were found."
                    )

                else:

                    st.dataframe(
                        trend_df,
                        use_container_width=True,
                        hide_index=True,
                    )

                    fig = px.line(
                        trend_df,
                        x="Period",
                        y=["Budget", "Actual"],
                        markers=True,
                        title="Budget vs Actual Trend",
                    )

                    fig.update_layout(
                        template="plotly_white",
                        height=420,
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True,
                    )

            except Exception as exc:

                st.error(
                    f"Unable to generate trend analysis: {exc}"
                )

        else:

            st.warning(
                "Date, Budget and Actual columns "
                "could not all be identified."
            )


# ============================================================
# ASK A QUESTION
# ============================================================

elif st.session_state.view == "question":

    st.header("Ask a Question")

    st.caption(
        "Ask a targeted question about the uploaded dataset."
    )

    question = st.text_input(
        "Your question",
        placeholder=(
            "Example: Which company has the highest D/E ratio?"
        ),
    )

    if st.button(
        "Ask AI",
        type="primary",
        disabled=not question.strip(),
    ):

        with st.spinner(
            "Analyzing your data..."
        ):

            try:

                from core.questions import answer_question

                answer = answer_question(
                    df,
                    question,
                )

                st.markdown("### AI Answer")

                st.success(answer)

            except Exception as exc:

                st.error(
                    f"Unable to answer the question: {exc}"
                )


# ============================================================
# DATA PREPARATION DETAILS
# ============================================================

with st.expander(
    "Data preparation details"
):

    st.markdown(
        "### Detected Column Mapping"
    )

    mapping_table = pd.DataFrame(
        [
            {
                "Concept": "Budget",
                "Detected Column": (
                    budget_column or "Not identified"
                ),
            },
            {
                "Concept": "Actual",
                "Detected Column": (
                    actual_column or "Not identified"
                ),
            },
            {
                "Concept": "Category",
                "Detected Column": (
                    category_column or "Not identified"
                ),
            },
            {
                "Concept": "Date",
                "Detected Column": (
                    date_column or "Not identified"
                ),
            },
        ]
    )

    st.dataframe(
        mapping_table,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        "### Transformations"
    )

    if st.session_state.transformations:

        for item in st.session_state.transformations:

            st.write(
                f"• {item.get('description', '')}"
            )

    else:

        st.write(
            "No automatic transformations were required."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.html(
    """
    <div class="footer">
        Budget Variance Analyzer · Financial Analytics Workspace
    </div>
    """
)
