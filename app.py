import streamlit as st
import pandas as pd
from llm import analyze_ticket
from storage import save_ticket, load_tickets
from analysis import detect_trends, detect_drift
from st_aggrid import AgGrid, GridOptionsBuilder
from analysis import (
    detect_trends,
    detect_drift,
    ticket_volume_over_time,
    urgency_distribution,
    category_shift,
    new_categories_detected,
    confidence_trend,
    issue_complexity_trend
)

if "results" not in st.session_state:
    st.session_state.results = None


# ---------------- Page Config ----------------
st.set_page_config(
    page_title="AssistFlow AI",
    layout="wide"
)

st.title("AssistFlow AI")
st.caption("LLM-powered support co-pilot for ticket analysis and triage")

# ---------------- Helpers ----------------
def format_urgency(level: str) -> str:
    return level.capitalize()

def format_confidence(value: float) -> str:
    return f"{int(value * 100)}%"

def format_actions(actions):
    if isinstance(actions, str):
        try:
            actions = eval(actions)
        except Exception:
            return actions
    return "\n".join([f"- [ ] {a}" for a in actions])

# ---------------- Tabs ----------------
# tab_analysis, = st.tabs(["Analysis"])
tab_analysis, tab_history, tab_analytics = st.tabs( ["Analysis", "History", "Analytics"] )


# =========================================================
# TAB 1: ANALYSIS
# =========================================================
# ---------------- Analysis Output ----------------
with tab_analysis:
    st.header("Ticket analysis")

    ticket_text = st.text_area(
        "Customer ticket",
        placeholder="Paste the customer message here",
        height=150
    )

    ab_test = st.checkbox(
        "Enable A/B testing (compare multiple models)"
    )

    model = st.selectbox(
        "AI model",
        [
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile",
            "openai/gpt-oss-120b"
        ]
    )

    analyze_clicked = st.button("Analyze ticket", type="primary")
    if analyze_clicked:
        if not ticket_text.strip():
            st.warning("Please enter a ticket message before analyzing.")
        else:
            results = []

            if ab_test:
                st.info("Running A/B testing across models...")
                models = [
                    "llama-3.1-8b-instant",
                    "llama-3.3-70b-versatile",
                    "openai/gpt-oss-120b"
                ]
                for m in models:
                    res = analyze_ticket(ticket_text, m)
                    save_ticket(res)
                    results.append(res)
            else:
                res = analyze_ticket(ticket_text, model)
                save_ticket(res)
                results.append(res)

                # ✅ STORE RESULTS SAFELY
                st.session_state.results = results
            if st.session_state.results:
                results = st.session_state.results
            primary_result = results[0]

        st.divider()
        st.subheader("Analysis summary")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Issue category", primary_result["category"])

        with col2:
            st.metric("Urgency", format_urgency(primary_result["urgency"]))

        with col3:
            st.metric("Confidence", format_confidence(primary_result["confidence"]))

        with col4:
            st.metric("Model", primary_result["model_used"])

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Suggested actions")
            st.markdown(format_actions(primary_result["suggested_actions"]))

        with col2:
            st.subheader("Explanation")
            st.info(primary_result["explanation"])

        st.divider()
        st.caption(f"Timestamp: {primary_result['timestamp']}")
        st.success("Ticket analyzed and saved.")





# =========================================================
# TAB 2: HISTORY
# =========================================================
with tab_history:
    st.header("Ticket history")

    df = load_tickets()

    if df.empty:
        st.info("No tickets found.")
    else:
        display_df = df.copy()

        # Format fields for display
        display_df["timestamp"] = display_df["timestamp"].dt.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        display_df["confidence"] = display_df["confidence"].apply(format_confidence)
        display_df["suggested_actions"] = display_df["suggested_actions"].apply(
            format_actions
        )

        display_df = display_df.rename(
            columns={
                "timestamp": "Timestamp",
                "issue": "Issue",
                "category": "Category",
                "urgency": "Urgency",
                "suggested_actions": "Suggested actions",
                "explanation": "Explanation",
                "confidence": "Confidence",
                "model_used": "Model"
            }
        )

        gb = GridOptionsBuilder.from_dataframe(display_df)
        gb.configure_default_column(
            wrapText=True,
            autoHeight=True,
            filter=True,
            sortable=True,
            resizable=True
        )
        gb.configure_column("Explanation", width=300)
        gb.configure_column("Suggested actions", width=250)
        grid_options = gb.build()

        AgGrid(
            display_df,
            gridOptions=grid_options,
            height=500,
            theme="streamlit"
        )
        if st.session_state.results and len(st.session_state.results) > 1:
            results = st.session_state.results

            st.subheader("A/B Testing Comparison")

            compare_df = pd.DataFrame([
                {
                    "Model": r["model_used"],
                    "Category": r["category"],
                    "Urgency": r["urgency"],
                    "Confidence": r["confidence"],
                    "Explanation": r["explanation"]
                }
                for r in results
            ])

            st.dataframe(compare_df, use_container_width=True)

            # Detect disagreement
            urgencies = set(compare_df["Urgency"])
            if len(urgencies) > 1:
                st.warning("⚠ Model disagreement detected on urgency level")


# =========================================================
# TAB 3: ANALYTICS
# =========================================================
with tab_analytics:
    st.header("Support analytics")

    df = load_tickets()

    if df.empty:
        st.info("No data available.")
    else:
        # ---- Row 0 ----
        # col1, col2 = st.columns(2)

        # with col1:
        #     st.subheader("Issue category trends")
        #     st.bar_chart(detect_trends(df))

        # with col2:
        #     st.subheader("Recent drift signals")
        #     st.bar_chart(detect_drift(df))

        # ---- Row 1 ----
        # col1, col2 = st.columns(2)

        # with col1:
        #     st.subheader("Ticket volume over time")
        #     st.line_chart(ticket_volume_over_time(df))

        # with col2:
        #     st.subheader("Urgency distribution")
        #     st.bar_chart(urgency_distribution(df))

        # st.divider()

        # ---- Row 2 ----
        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Category shift detection")
            st.bar_chart(category_shift(df))

        with col4:
            st.subheader("New issue categories")
            st.dataframe(
                new_categories_detected(df).head(10),
            )

        st.divider()

        # ---- Row 3 ----
        # col5, col6 = st.columns(2)

        # with col5:
        #     st.subheader("Model confidence trend")
        #     st.line_chart(confidence_trend(df))

        # with col6:
        #     st.subheader("Issue complexity trend")
        #     st.line_chart(issue_complexity_trend(df))

        st.divider()

        st.subheader("Model usage (A/B testing)")
        st.bar_chart(df["model_used"].value_counts())
    st.subheader("Average confidence per model")
    st.bar_chart(
        df.groupby("model_used")["confidence"].mean()
    )
    st.subheader("Urgency distribution by model")
    urgency_dist = pd.crosstab(df["model_used"], df["urgency"])
    st.bar_chart(urgency_dist)
    # st.subheader("Confidence trend by model")

    # conf_trend = (
    #     df.sort_values("timestamp")
    #     .groupby("model_used")[["timestamp", "confidence"]]
    # )

    # for model_name, group in conf_trend:
    #     st.line_chart(
    #         group.set_index("timestamp")["confidence"],
    #         height=200
    #     )

