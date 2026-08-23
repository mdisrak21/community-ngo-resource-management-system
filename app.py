import streamlit as st
from database import (
    create_tables,
    add_beneficiary,
    get_beneficiaries,
    update_beneficiary,
    deactivate_beneficiary
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

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Beneficiaries",
        len(beneficiaries)
    )

    active_count = sum(
        1 for b in beneficiaries if b[8] == "Active"
    )

    inactive_count = sum(
        1 for b in beneficiaries if b[8] == "Inactive"
    )

    col2.metric(
        "Active Beneficiaries",
        active_count
    )

    col3.metric(
        "Inactive Beneficiaries",
        inactive_count
    )


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


    # -------------------------
    # Register
    # -------------------------

    with tab1:

        st.subheader("Register New Beneficiary")

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

            submitted = st.form_submit_button(
                "Register Beneficiary"
            )

            if submitted:

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
                        f"Beneficiary registered successfully! ID: {beneficiary_id}"
                    )


    # -------------------------
    # View
    # -------------------------

    with tab2:

        st.subheader("Beneficiary List")

        beneficiaries = get_beneficiaries()

        if beneficiaries:

            search = st.text_input(
                "Search by name or phone"
            )

            status_filter = st.selectbox(
                "Filter by Status",
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

            table_data = []

            for b in filtered:

                table_data.append({
                    "ID": b[0],
                    "Name": b[1],
                    "Age": b[2],
                    "Gender": b[3],
                    "Phone": b[4],
                    "Address": b[5],
                    "Vulnerability": b[6],
                    "Registration Date": b[7],
                    "Status": b[8]
                })

            st.dataframe(
                table_data,
                use_container_width=True
            )

        else:

            st.info("No beneficiaries found.")


    # -------------------------
    # Manage
    # -------------------------

    with tab3:

        st.subheader("Manage Beneficiary")

        beneficiaries = get_beneficiaries()

        if beneficiaries:

            beneficiary_options = {
                f"{b[0]} - {b[1]}": b
                for b in beneficiaries
            }

            selected = st.selectbox(
                "Select Beneficiary",
                list(beneficiary_options.keys())
            )

            beneficiary = beneficiary_options[selected]

            st.write(
                f"Current Status: **{beneficiary[8]}**"
            )

            with st.form("update_form"):

                new_name = st.text_input(
                    "Name",
                    value=beneficiary[1]
                )

                col1, col2 = st.columns(2)

                with col1:

                    new_age = st.number_input(
                        "Age",
                        min_value=0,
                        max_value=120,
                        value=beneficiary[2] or 18
                    )

                    new_gender = st.selectbox(
                        "Gender",
                        ["Male", "Female", "Other"],
                        index=(
                            ["Male", "Female", "Other"]
                            .index(beneficiary[3])
                            if beneficiary[3] in ["Male", "Female", "Other"]
                            else 0
                        )
                    )

                    new_phone = st.text_input(
                        "Phone",
                        value=beneficiary[4] or ""
                    )

                with col2:

                    new_address = st.text_area(
                        "Address",
                        value=beneficiary[5] or ""
                    )

                    categories = [
                        "Flood Affected",
                        "Low Income",
                        "Disability",
                        "Elderly",
                        "Child",
                        "Other"
                    ]

                    category_index = (
                        categories.index(beneficiary[6])
                        if beneficiary[6] in categories
                        else 0
                    )

                    new_category = st.selectbox(
                        "Vulnerability Category",
                        categories,
                        index=category_index
                    )

                    new_status = st.selectbox(
                        "Status",
                        ["Active", "Inactive"],
                        index=(
                            0
                            if beneficiary[8] == "Active"
                            else 1
                        )
                    )

                update_button = st.form_submit_button(
                    "Update Beneficiary"
                )

                if update_button:

                    update_beneficiary(
                        beneficiary[0],
                        new_name.strip(),
                        new_age,
                        new_gender,
                        new_phone,
                        new_address,
                        new_category,
                        new_status
                    )

                    st.success(
                        "Beneficiary updated successfully!"
                    )

                    st.rerun()

            if beneficiary[8] == "Active":

                if st.button(
                    "Deactivate Beneficiary",
                    type="secondary"
                ):

                    deactivate_beneficiary(
                        beneficiary[0]
                    )

                    st.success(
                        "Beneficiary deactivated successfully!"
                    )

                    st.rerun()


# =========================
# Other Pages
# =========================

else:

    st.header(page)

    st.info(
        f"{page} module will be developed in the next phases."
    )