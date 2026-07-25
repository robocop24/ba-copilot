import json
import streamlit as st
from main import build_state


def main():
    st.title("📊 BA Copilot - Business Analyst Assistant")
    st.info("Processing document...")

    try:
        state = build_state()
    except ValueError as e:
        st.error(f"Failed to load document: {e}")
        return

    st.success("✅ Report generated successfully!")

    st.header("🔍 Analysis")
    st.markdown("**Actors:** " + ", ".join(state.analysis.get("actors", [])))
    st.markdown("**Modules:** " + ", ".join(state.analysis.get("modules", [])))
    st.markdown("**Functional Requirements:** " + ", ".join(state.analysis.get("functional_requirements", [])))

    st.header("🧩 User Stories")
    for story in state.stories.get("user_stories", []):
        st.markdown(f"- **Story:** {story.get('story', '')}")

    st.header("✅ Acceptance Criteria")
    for criteria in state.acceptance_criteria.get("criteria", []):
        st.markdown(f"- {criteria}")

    st.header("⚠️ Story Gaps")
    for gap in state.story_gaps.get("gaps", []):
        st.markdown(f"- {gap}")

    st.header("⏱ Effort Estimation")
    for item in state.effort_estimation.get("estimates", []):
        st.markdown(f"- {item}")

    st.header("🧠 Review Summary")
    st.markdown(state.review.get("summary", "No review available."))

    st.header("🔧 Refinement Suggestions")
    for suggestion in state.refinement.get("suggestions", []):
        st.markdown(f"- {suggestion}")

    report_json = state.to_dict()
    st.subheader("📥 Download BA Report")
    st.download_button(
        label="Download BA Report (JSON)",
        data=json.dumps(report_json, indent=4),
        file_name="ba_report.json",
        mime="application/json"
    )


if __name__ == "__main__":
    main()
