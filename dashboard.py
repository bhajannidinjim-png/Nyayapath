"""
dashboard.py
------------
NyayPath — Final Compliance Dashboard Module
Renders the government-facing compliance dashboard.
Called from app.py Tab 3.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import json


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def parse_deadline(deadline_str: str):
    """
    Try to parse a deadline string into a date object.
    Returns None if it cannot be parsed (e.g. 'within 30 days').
    """
    if not deadline_str or deadline_str.strip().lower() in ("not specified", ""):
        return None
    formats = [
        "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y",
        "%d %B %Y", "%d %b %Y",
        "%B %d, %Y", "%b %d, %Y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(deadline_str.strip(), fmt).date()
        except ValueError:
            continue
    return None


def deadline_status(deadline_str: str):
    """
    Returns (emoji, label, color) based on deadline proximity.
    🔴 Overdue / 🟡 Due Soon (≤7 days) / 🟢 On Track / ⚪ Unknown
    """
    d = parse_deadline(deadline_str)
    if d is None:
        return "⚪", "Unknown", "#aab7b8"
    today = date.today()
    delta = (d - today).days
    if delta < 0:
        return "🔴", f"Overdue by {abs(delta)}d", "#c0392b"
    elif delta <= 7:
        return "🟡", f"Due in {delta}d", "#d35400"
    else:
        return "🟢", f"Due in {delta}d", "#1e8449"


def priority_emoji(p: str) -> str:
    return {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(p, "⚪")


# ─────────────────────────────────────────────
# SECTION 1 — SUMMARY METRICS
# ─────────────────────────────────────────────

def render_summary(verified_actions: dict):
    """Render top-level KPI metric cards."""
    all_items  = list(verified_actions.values())
    approved   = [v for v in all_items if v.get("status") in ("approved", "edited")]
    pending    = [v for v in all_items if v.get("status") == "pending"]
    rejected   = [v for v in all_items if v.get("status") == "rejected"]
    high_pri   = [v for v in approved  if v.get("priority") == "High"]
    overdue    = [v for v in approved  if deadline_status(v.get("deadline",""))[1].startswith("Overdue")]
    depts      = set(v.get("department","Not Specified") for v in approved)

    c1,c2,c3,c4,c5,c6,c7 = st.columns(7)
    c1.metric("📋 Total",       len(all_items))
    c2.metric("✅ Approved",    len(approved))
    c3.metric("⏳ Pending",     len(pending))
    c4.metric("❌ Rejected",    len(rejected))
    c5.metric("🔴 High Priority", len(high_pri))
    c6.metric("⚠️ Overdue",    len(overdue))
    c7.metric("🏛️ Departments", len(depts))


# ─────────────────────────────────────────────
# SECTION 2 — DEPARTMENT-WISE VIEW
# ─────────────────────────────────────────────

def render_department_view(approved: list):
    """Group approved actions by department and render."""
    st.subheader("🏛️ Department-wise Action View")

    if not approved:
        st.info("No approved actions to display.")
        return

    # Group by department
    dept_map = {}
    for action in approved:
        dept = action.get("department", "Not Specified") or "Not Specified"
        dept_map.setdefault(dept, []).append(action)

    for dept, items in sorted(dept_map.items()):
        with st.expander(f"🏛️ {dept}  —  {len(items)} action(s)", expanded=True):
            rows = []
            for a in items:
                emoji, label, _ = deadline_status(a.get("deadline",""))
                rows.append({
                    "Priority":   f"{priority_emoji(a.get('priority',''))} {a.get('priority','')}",
                    "Action":     a.get("action","")[:90] + "...",
                    "Deadline":   a.get("deadline","—"),
                    "Status":     f"{emoji} {label}",
                    "Verified As": a.get("status","").upper(),
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
# SECTION 3 — DEADLINE TRACKER
# ─────────────────────────────────────────────

def render_deadline_tracker(approved: list):
    """Visual deadline tracker with traffic light indicators."""
    st.subheader("📅 Deadline Tracker")

    if not approved:
        st.info("No approved actions to track.")
        return

    overdue, due_soon, on_track, unknown = [], [], [], []

    for a in approved:
        emoji, label, _ = deadline_status(a.get("deadline",""))
        entry = {
            "Action":     a.get("action","")[:70] + "...",
            "Department": a.get("department","—"),
            "Deadline":   a.get("deadline","—"),
            "Status":     label,
        }
        if emoji == "🔴":   overdue.append(entry)
        elif emoji == "🟡": due_soon.append(entry)
        elif emoji == "🟢": on_track.append(entry)
        else:               unknown.append(entry)

    t1, t2, t3, t4 = st.tabs([
        f"🔴 Overdue ({len(overdue)})",
        f"🟡 Due Soon ({len(due_soon)})",
        f"🟢 On Track ({len(on_track)})",
        f"⚪ Unknown ({len(unknown)})",
    ])

    for tab, items, msg in [
        (t1, overdue,  "No overdue actions."),
        (t2, due_soon, "No actions due soon."),
        (t3, on_track, "No on-track actions with known deadlines."),
        (t4, unknown,  "No actions with unknown deadlines."),
    ]:
        with tab:
            if items:
                st.dataframe(pd.DataFrame(items), use_container_width=True, hide_index=True)
            else:
                st.success(msg)


# ─────────────────────────────────────────────
# SECTION 4 — SEARCH + FILTER
# ─────────────────────────────────────────────

def render_search_filter(approved: list):
    """Searchable, filterable table of all verified actions."""
    st.subheader("🔎 Search & Filter Actions")

    if not approved:
        st.info("No approved actions available.")
        return

    # Build filter options
    depts      = sorted(set(a.get("department","Not Specified") for a in approved))
    priorities = ["All", "High", "Medium", "Low"]

    sc1, sc2, sc3 = st.columns([2,1,1])
    with sc1:
        search_q = st.text_input("🔍 Search actions", placeholder="Type keyword...")
    with sc2:
        dept_filter = st.selectbox("Department", ["All"] + depts)
    with sc3:
        pri_filter  = st.selectbox("Priority", priorities)

    # Apply filters
    filtered = []
    for a in approved:
        if search_q and search_q.lower() not in a.get("action","").lower():
            continue
        if dept_filter != "All" and a.get("department","") != dept_filter:
            continue
        if pri_filter  != "All" and a.get("priority","")   != pri_filter:
            continue
        filtered.append(a)

    st.caption(f"Showing {len(filtered)} of {len(approved)} verified actions")

    if filtered:
        rows = []
        for a in filtered:
            emoji, label, _ = deadline_status(a.get("deadline",""))
            rows.append({
                "Priority":   f"{priority_emoji(a.get('priority',''))} {a.get('priority','')}",
                "Action":     a.get("action","")[:80] + "...",
                "Department": a.get("department","—"),
                "Deadline":   a.get("deadline","—"),
                "Deadline Status": f"{emoji} {label}",
                "Verified As": a.get("status","").upper(),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.warning("No actions match your filters.")


# ─────────────────────────────────────────────
# SECTION 5 — ANALYTICS
# ─────────────────────────────────────────────

def render_analytics(verified_actions: dict):
    """Simple native Streamlit charts — no external chart libs needed."""
    st.subheader("📊 Analytics")

    all_items = list(verified_actions.values())
    approved  = [v for v in all_items if v.get("status") in ("approved","edited")]

    if not all_items:
        st.info("No data yet.")
        return

    ch1, ch2, ch3 = st.columns(3)

    # Chart 1 — Actions by Department
    with ch1:
        st.markdown("**Actions by Department**")
        dept_counts = {}
        for a in approved:
            d = a.get("department","Not Specified") or "Not Specified"
            dept_counts[d] = dept_counts.get(d, 0) + 1
        if dept_counts:
            df_dept = pd.DataFrame(
                dept_counts.items(), columns=["Department","Count"]
            ).set_index("Department")
            st.bar_chart(df_dept)
        else:
            st.info("No approved actions.")

    # Chart 2 — Priority Distribution
    with ch2:
        st.markdown("**Priority Distribution**")
        pri_counts = {"High":0, "Medium":0, "Low":0}
        for a in approved:
            p = a.get("priority","Medium")
            pri_counts[p] = pri_counts.get(p,0) + 1
        df_pri = pd.DataFrame(
            pri_counts.items(), columns=["Priority","Count"]
        ).set_index("Priority")
        st.bar_chart(df_pri)

    # Chart 3 — Approval Status
    with ch3:
        st.markdown("**Verification Status**")
        status_counts = {"Approved":0, "Edited":0, "Pending":0, "Rejected":0}
        for a in all_items:
            s = a.get("status","pending").capitalize()
            status_counts[s] = status_counts.get(s,0) + 1
        df_status = pd.DataFrame(
            status_counts.items(), columns=["Status","Count"]
        ).set_index("Status")
        st.bar_chart(df_status)


# ─────────────────────────────────────────────
# SECTION 6 — EXPORT (PDF + CSV)
# ─────────────────────────────────────────────

def render_export(metadata: dict, approved: list):
    """Export verified report as PDF and CSV."""
    from src.pdf_exporter import generate_pdf_report

    st.subheader("💾 Export Verified Report")

    if not approved:
        st.warning("Approve at least one action before exporting.")
        return

    ec1, ec2 = st.columns(2)

    # PDF Export
    with ec1:
        # ADDED KEY HERE ⬇️
        if st.button("📥 Generate PDF Report", type="primary", use_container_width=True, key="btn_generate_pdf_report"):
            with st.spinner("Building PDF..."):
                try:
                    pdf_bytes = generate_pdf_report(
                        metadata=metadata,
                        verified_actions=approved
                    )
                    st.session_state["dashboard_pdf"] = pdf_bytes
                    st.success("PDF ready!")
                except Exception as e:
                    st.error(f"PDF error: {str(e)}")

        if st.session_state.get("dashboard_pdf"):
            st.download_button(
                "⬇️ Download PDF",
                data=st.session_state["dashboard_pdf"],
                file_name="NyayPath_Final_Report.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="btn_download_pdf_final" # ADDED KEY HERE TOO
            )

    # CSV Export
    with ec2:
        rows = []
        for a in approved:
            rows.append({
                "Action":      a.get("action",""),
                "Department":  a.get("department",""),
                "Deadline":    a.get("deadline",""),
                "Priority":    a.get("priority",""),
                "Confidence":  a.get("confidence",""),
                "Status":      a.get("status",""),
                "Source Text": a.get("source_text",""),
            })
        csv_str = pd.DataFrame(rows).to_csv(index=False)
        st.download_button(
            "⬇️ Download CSV Report",
            data=csv_str,
            file_name="NyayPath_Verified_Actions.csv",
            mime="text/csv",
            use_container_width=True,
            key="btn_download_csv_final" # ADDED KEY HERE TOO
        )
        st.caption("CSV includes all verified action details.")
# ─────────────────────────────────────────────
# MASTER RENDER — called from app.py
# ─────────────────────────────────────────────

def render_dashboard(verified_actions: dict, metadata: dict):
    """
    Master entry point for the dashboard tab.
    Call this from app.py with:
        render_dashboard(st.session_state.verified_actions, result["metadata"])
    """
    approved = [
        v for v in verified_actions.values()
        if v.get("status") in ("approved","edited")
    ]

    st.subheader("📊 Final Compliance Dashboard")
    st.caption("Shows only approved and verified actions. Pending and rejected items are excluded.")
    st.divider()

    # ── KPI Metrics ──
    render_summary(verified_actions)
    st.divider()

    # ── Inner tabs ──
    d1, d2, d3, d4, d5 = st.tabs([
        "🏛️ By Department",
        "📅 Deadlines",
        "🔎 Search",
        "📊 Analytics",
        "💾 Export",
    ])

    with d1: render_department_view(approved)
    with d2: render_deadline_tracker(approved)
    with d3: render_search_filter(approved)
    with d4: render_analytics(verified_actions)
    with d5: render_export(metadata, approved)
