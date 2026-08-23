import streamlit as st
from database import (
    add_distribution,
    get_distributions,
    create_tables,
    add_beneficiary,
    get_beneficiaries,
    update_beneficiary,
    deactivate_beneficiary,
    add_project,
    get_projects,
    add_resource,
    get_resources
)

st.set_page_config(
    page_title="Community & NGO Resource Management System",
    page_icon="🌍",
    layout="wide"
)

create_tables()

st.title("Community & NGO Resource Management System")

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

    st.header("Dashboard")

    beneficiaries = get_beneficiaries()
    projects = get_projects()
    resources = get_resources()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Beneficiaries", len(beneficiaries))
    col2.metric("Total Projects", len(projects))
    col3.metric("Resource Types", len(resources))


# =========================
# Beneficiaries
# =========================

elif page == "Beneficiaries":

    st.header("Beneficiary Management")

    tab1, tab2, tab3 = st.tabs([
        "Register",
        "View Beneficiaries",
        "Manage"
    ])

    with tab1:

        with st.form("beneficiary_form"):

            name = st.text_input("Full Name")

            col1, col2 = st.columns(2)

            with col1:
                age = st.number_input(
                    "Age",
                    min_value=0,
                    max_value=120,
                    value=18
                )

                gender = st.selectbox(
                    "Gender",
                    ["Male", "Female", "Other"]
                )

                phone = st.text_input("Phone")

            with col2:
                address = st.text_area("Address")

                vulnerability_category = st.selectbox(
                    "Vulnerability Category",
                    [
                        "Flood Affected",
                        "Low Income",
                        "Disability",
                        "Elderly",
                        "Child",
                        "Other"
                    ]
                )

            submit = st.form_submit_button(
                "Register Beneficiary"
            )

            if submit:

                if not name.strip():

                    st.error("Name is required.")

                else:

                    beneficiary_id = add_beneficiary(
                        name.strip(),
                        age,
                        gender,
                        phone,
                        address,
                        vulnerability_category
                    )

                    st.success(
                        f"Beneficiary registered! ID: {beneficiary_id}"
                    )

    with tab2:

        beneficiaries = get_beneficiaries()

        search = st.text_input(
            "Search by name or phone"
        )

        status_filter = st.selectbox(
            "Status",
            ["All", "Active", "Inactive"]
        )

        filtered = beneficiaries

        if search:

            search = search.lower()

            filtered = [
                b for b in filtered
                if search in str(b[1]).lower()
                or search in str(b[4]).lower()
            ]

        if status_filter != "All":

            filtered = [
                b for b in filtered
                if b[8] == status_filter
            ]

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
                for b in filtered
            ],
            use_container_width=True
        )

    with tab3:

        beneficiaries = get_beneficiaries()

        if beneficiaries:

            options = {
                f"{b[0]} - {b[1]}": b
                for b in beneficiaries
            }

            selected = st.selectbox(
                "Select Beneficiary",
                list(options.keys())
            )

            b = options[selected]

            with st.form("update_beneficiary"):

                name = st.text_input(
                    "Name",
                    value=b[1]
                )

                age = st.number_input(
                    "Age",
                    min_value=0,
                    max_value=120,
                    value=b[2] or 18
                )

                gender = st.selectbox(
                    "Gender",
                    ["Male", "Female", "Other"],
                    index=(
                        ["Male", "Female", "Other"].index(b[3])
                        if b[3] in ["Male", "Female", "Other"]
                        else 0
                    )
                )

                phone = st.text_input(
                    "Phone",
                    value=b[4] or ""
                )

                address = st.text_area(
                    "Address",
                    value=b[5] or ""
                )

                categories = [
                    "Flood Affected",
                    "Low Income",
                    "Disability",
                    "Elderly",
                    "Child",
                    "Other"
                ]

                category = st.selectbox(
                    "Vulnerability Category",
                    categories,
                    index=(
                        categories.index(b[6])
                        if b[6] in categories
                        else 0
                    )
                )

                status = st.selectbox(
                    "Status",
                    ["Active", "Inactive"],
                    index=0 if b[8] == "Active" else 1
                )

                update = st.form_submit_button(
                    "Update Beneficiary"
                )

                if update:

                    update_beneficiary(
                        b[0],
                        name,
                        age,
                        gender,
                        phone,
                        address,
                        category,
                        status
                    )

                    st.success("Updated successfully!")

                    st.rerun()

            if b[8] == "Active":

                if st.button("Deactivate Beneficiary"):

                    deactivate_beneficiary(b[0])

                    st.success(
                        "Beneficiary deactivated!"
                    )

                    st.rerun()


# =========================
# Projects
# =========================

elif page == "Projects":

    st.header("Project Management")

    tab1, tab2 = st.tabs([
        "Create Project",
        "Project List"
    ])

    with tab1:

        with st.form("project_form"):

            name = st.text_input(
                "Project Name"
            )

            description = st.text_area(
                "Description"
            )

            location = st.text_input(
                "Location"
            )

            col1, col2 = st.columns(2)

            with col1:

                start_date = st.date_input(
                    "Start Date"
                )

                budget = st.number_input(
                    "Budget",
                    min_value=0.0,
                    step=1000.0
                )

            with col2:

                end_date = st.date_input(
                    "End Date"
                )

                status = st.selectbox(
                    "Status",
                    [
                        "Planned",
                        "Active",
                        "Completed",
                        "Cancelled"
                    ]
                )

            submit = st.form_submit_button(
                "Create Project"
            )

            if submit:

                if not name.strip():

                    st.error(
                        "Project name is required."
                    )

                elif end_date < start_date:

                    st.error(
                        "End date cannot be before start date."
                    )

                else:

                    project_id = add_project(
                        name.strip(),
                        description,
                        location,
                        start_date.isoformat(),
                        end_date.isoformat(),
                        budget,
                        status
                    )

                    st.success(
                        f"Project created! ID: {project_id}"
                    )

    with tab2:

        projects = get_projects()

        st.dataframe(
            [
                {
                    "ID": p[0],
                    "Name": p[1],
                    "Description": p[2],
                    "Location": p[3],
                    "Start": p[4],
                    "End": p[5],
                    "Budget": p[6],
                    "Status": p[7]
                }
                for p in projects
            ],
            use_container_width=True
        )


# =========================
# Resources
# =========================

elif page == "Resources":

    st.header("Resource Management")

    tab1, tab2 = st.tabs([
        "Add Resource",
        "Inventory"
    ])

    with tab1:

        with st.form("resource_form"):

            name = st.text_input(
                "Resource Name"
            )

            category = st.selectbox(
                "Category",
                [
                    "Food",
                    "Water",
                    "Medicine",
                    "Clothing",
                    "Shelter",
                    "Hygiene",
                    "Other"
                ]
            )

            unit = st.selectbox(
                "Unit",
                [
                    "kg",
                    "liter",
                    "piece",
                    "box",
                    "packet"
                ]
            )

            quantity = st.number_input(
                "Quantity",
                min_value=0.0,
                step=1.0
            )

            submit = st.form_submit_button(
                "Add Resource"
            )

            if submit:

                if not name.strip():

                    st.error(
                        "Resource name is required."
                    )

                elif quantity <= 0:

                    st.error(
                        "Quantity must be greater than 0."
                    )

                else:

                    resource_id = add_resource(
                        name.strip(),
                        category,
                        unit,
                        quantity
                    )

                    st.success(
                        f"Resource added! ID: {resource_id}"
                    )

    with tab2:

        resources = get_resources()

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

    st.header("Resource Distribution")

    beneficiaries = [
        b for b in get_beneficiaries()
        if b[8] == "Active"
    ]

    projects = get_projects()
    resources = [
        r for r in get_resources()
        if r[4] > 0
    ]

    if not beneficiaries:

        st.warning("No active beneficiaries available.")

    elif not projects:

        st.warning("No projects available.")

    elif not resources:

        st.warning("No resources with available stock.")

    else:

        with st.form("distribution_form"):

            beneficiary_options = {
                f"{b[0]} - {b[1]}": b[0]
                for b in beneficiaries
            }

            project_options = {
                f"{p[0]} - {p[1]}": p[0]
                for p in projects
            }

            resource_options = {
                f"{r[0]} - {r[1]} ({r[4]} {r[3]} available)": r
                for r in resources
            }

            selected_beneficiary = st.selectbox(
                "Beneficiary",
                list(beneficiary_options.keys())
            )

            selected_project = st.selectbox(
                "Project",
                list(project_options.keys())
            )

            selected_resource = st.selectbox(
                "Resource",
                list(resource_options.keys())
            )

            resource = resource_options[selected_resource]

            quantity = st.number_input(
                f"Quantity ({resource[3]})",
                min_value=0.1,
                max_value=float(resource[4]),
                value=1.0,
                step=1.0
            )

            distribution_date = st.date_input(
                "Distribution Date"
            )

            location = st.text_input(
                "Distribution Location"
            )

            submit = st.form_submit_button(
                "Distribute Resource"
            )

            if submit:

                distribution_id = add_distribution(
                    beneficiary_options[selected_beneficiary],
                    project_options[selected_project],
                    resource[0],
                    quantity,
                    distribution_date.isoformat(),
                    location
                )

                st.success(
                    f"Distribution recorded! ID: {distribution_id}"
                )

    st.divider()

    st.subheader("Distribution History")

    distributions = get_distributions()

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

        st.info("No distributions recorded.")
        
# =========================
# Other Pages
# =========================

else:

    st.header(page)

    st.info(
        f"{page} module will be developed in a future phase."
    )