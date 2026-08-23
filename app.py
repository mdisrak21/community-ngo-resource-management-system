import streamlit as st
from database import (
    create_tables,
    get_beneficiaries,
    get_projects,
    get_resources,
    get_distributions,
    get_volunteers
)

st.set_page_config(
    page_title="NGO Resource Management System",
    page_icon="🌍",
    layout="wide"
)

create_tables()

beneficiaries = get_beneficiaries()
projects = get_projects()
resources = get_resources()
distributions = get_distributions()
volunteers = get_volunteers()

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Dashboard",
        "Beneficiaries",
        "Projects",
        "Resources",
        "Distributions",
        "Volunteers",
        "Reports"
    ]
)


# =========================
# Dashboard
# =========================

if page == "Dashboard":

    st.title("🌍 NGO Resource Management Dashboard")

    total_beneficiaries = len(beneficiaries)

    active_beneficiaries = sum(
        1 for b in beneficiaries
        if b[8] == "Active"
    )

    total_projects = len(projects)

    active_projects = sum(
        1 for p in projects
        if p[7] == "Active"
    )

    total_resources = len(resources)

    total_volunteers = len(volunteers)

    active_volunteers = sum(
        1 for v in volunteers
        if v[5] == "Active"
    )

    total_distributions = len(distributions)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Beneficiaries",
        total_beneficiaries
    )

    col2.metric(
        "Active Projects",
        active_projects
    )

    col3.metric(
        "Resources",
        total_resources
    )

    col4.metric(
        "Volunteers",
        total_volunteers
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Active Beneficiaries",
        active_beneficiaries
    )

    col2.metric(
        "Total Projects",
        total_projects
    )

    col3.metric(
        "Active Volunteers",
        active_volunteers
    )

    col4.metric(
        "Distributions",
        total_distributions
    )

    st.divider()

    st.subheader("Recent Beneficiaries")

    if beneficiaries:

        st.dataframe(
            [
                {
                    "ID": b[0],
                    "Name": b[1],
                    "Age": b[2],
                    "Phone": b[4],
                    "Vulnerability": b[6],
                    "Status": b[8]
                }
                for b in beneficiaries[:5]
            ],
            use_container_width=True
        )

    else:

        st.info("No beneficiary data available.")


# =========================
# Beneficiaries
# =========================

elif page == "Beneficiaries":

    st.title("Beneficiary Management")

    st.info(
        "Beneficiary registration, search, update and "
        "deactivation are available here."
    )

    if beneficiaries:

        st.dataframe(
            [
                {
                    "ID": b[0],
                    "Name": b[1],
                    "Age": b[2],
                    "Gender": b[3],
                    "Phone": b[4],
                    "Address": b[5],
                    "Vulnerability": b[6],
                    "Date": b[7],
                    "Status": b[8]
                }
                for b in beneficiaries
            ],
            use_container_width=True
        )

    else:

        st.info("No beneficiaries found.")


# =========================
# Projects
# =========================

elif page == "Projects":

    st.title("Project Management")

    if projects:

        st.dataframe(
            [
                {
                    "ID": p[0],
                    "Project": p[1],
                    "Location": p[3],
                    "Start Date": p[4],
                    "End Date": p[5],
                    "Budget": p[6],
                    "Status": p[7]
                }
                for p in projects
            ],
            use_container_width=True
        )

    else:

        st.info("No projects found.")


# =========================
# Resources
# =========================

elif page == "Resources":

    st.title("Resource Inventory")

    if resources:

        st.dataframe(
            [
                {
                    "ID": r[0],
                    "Resource": r[1],
                    "Category": r[2],
                    "Unit": r[3],
                    "Quantity": r[4]
                }
                for r in resources
            ],
            use_container_width=True
        )

    else:

        st.info("No resources found.")


# =========================
# Distributions
# =========================

elif page == "Distributions":

    st.title("Resource Distribution History")

    if distributions:

        st.dataframe(
            [
                {
                    "ID": d[0],
                    "Beneficiary": d[1],
                    "Project": d[2],
                    "Resource": d[3],
                    "Quantity": d[4],
                    "Date": d[5],
                    "Location": d[6]
                }
                for d in distributions
            ],
            use_container_width=True
        )

    else:

        st.info("No distribution records found.")


# =========================
# Volunteers
# =========================

elif page == "Volunteers":

    st.title("Volunteer Management")

    if volunteers:

        st.dataframe(
            [
                {
                    "ID": v[0],
                    "Name": v[1],
                    "Phone": v[2],
                    "Email": v[3],
                    "Skills": v[4],
                    "Status": v[5]
                }
                for v in volunteers
            ],
            use_container_width=True
        )

    else:

        st.info("No volunteers found.")


# =========================
# Reports
# =========================

elif page == "Reports":

    st.title("Reports")

    st.subheader("Beneficiary Summary")

    if beneficiaries:

        active = sum(
            1 for b in beneficiaries
            if b[8] == "Active"
        )

        inactive = sum(
            1 for b in beneficiaries
            if b[8] == "Inactive"
        )

        col1, col2 = st.columns(2)

        col1.metric(
            "Active",
            active
        )

        col2.metric(
            "Inactive",
            inactive
        )

    st.divider()

    st.subheader("Project Summary")

    if projects:

        planned = sum(
            1 for p in projects
            if p[7] == "Planned"
        )

        active = sum(
            1 for p in projects
            if p[7] == "Active"
        )

        completed = sum(
            1 for p in projects
            if p[7] == "Completed"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Planned", planned)
        col2.metric("Active", active)
        col3.metric("Completed", completed)

    st.divider()

    st.subheader("Resource Summary")

    if resources:

        st.dataframe(
            [
                {
                    "Resource": r[1],
                    "Category": r[2],
                    "Unit": r[3],
                    "Available Quantity": r[4]
                }
                for r in resources
            ],
            use_container_width=True
        )

    st.divider()

    st.subheader("Distribution Summary")

    st.metric(
        "Total Distributions",
        len(distributions)
    )

    st.divider()

    st.subheader("Volunteer Summary")

    active_volunteers = sum(
        1 for v in volunteers
        if v[5] == "Active"
    )

    st.metric(
        "Active Volunteers",
        active_volunteers
    )