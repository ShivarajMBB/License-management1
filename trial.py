import streamlit as st
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go
import base64
import requests
import json
# =============================================================================
# from streamlit_echarts import st_echarts
# from streamlit_extras.switch_page_button import switch_page
# =============================================================================

# Set Page Title
st.set_page_config(page_title="License Management System", layout="wide")

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = "login"  # Default page is Login
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False
if "loading_complete" not in st.session_state:
    st.session_state.loading_complete = False
if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = "license_data.xlsx"  # Default filename for testing

# Function to switch pages instantly
def switch_page(page_name):
    st.session_state.page = page_name
    st.rerun()  # Forces Streamlit to refresh the UI instantly

main_container = st.empty()

# Function to fetch and load credentials from GitHub
@st.cache_data
def load_credentials():
    url = "https://raw.githubusercontent.com/ShivarajMBB/Streamlit-repo/master/Security.txt"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            credentials = json.loads(response.text)  # Parse JSON content
            return {list(user.keys())[0]: list(user.values())[0] for user in credentials}  # Convert to dictionary
        else:
            st.error("Failed to load credentials. Please check your connection.")
            return {}
    except Exception as e:
        st.error(f"Error loading credentials: {str(e)}")
        return {}

# Load credentials
VALID_CREDENTIALS = load_credentials()

# ---------------------------- PAGE 1: LOGIN ---------------------------------
if st.session_state.page == "login":
    with main_container.container():
        st.markdown(
            """
            <style>
                .sign-in-title { text-align: center; font-weight: bold; margin-bottom: -10px; }
                .sign-in-subtext { text-align: center; font-size: 14px; color: #6c757d; margin-top: -10px; }
                .stButton > button { width: 100%; padding: 12px; font-size: 18px; font-weight: bold;
                                     background-color: #007BFF; color: white; border: none; border-radius: 8px; cursor: pointer; }
                .stButton > button:hover { background-color: #0056b3; }
            </style>
            <h2 class='sign-in-title'>Sign In</h2>
            <p class='sign-in-subtext'>Enter your email and password to sign in</p>
            """,
            unsafe_allow_html=True
        )
    
        # Initialize spacing for logo
        if "logo_spacing" not in st.session_state:
            st.session_state.logo_spacing = 200

        st.session_state.logo_spacing = 200
        
        # Create columns for centered layout
        col1, col2, col3 = st.columns([1, 2, 1])  
        with col2:  
            inner_col1, inner_col2, inner_col3 = st.columns([0.8, 2, 0.8])
            with inner_col2:
                email = st.text_input("Email*", placeholder="mail@simmmple.com")
                password = st.text_input("Password*", placeholder="Min. 8 characters", type="password")
    
                # Functional Sign In Button
                if st.button("Sign In"):  
                    if email in VALID_CREDENTIALS and VALID_CREDENTIALS[email] == password:
                        st.session_state.authenticated = True
                        switch_page("upload")  # Move to Upload Page Immediately
                    else:
                        st.error("Invalid email or password!")
                        st.session_state.logo_spacing = 128  # Reduce spacing when error appears

            # Footer text
            st.markdown(
                """
                <style>
                    .rights-text { text-align: center; font-size: 12px; color: #6c757d; margin-top: 20px; }
                </style>
                <p class='rights-text'>© 2024 All Rights Reserved. Made with love by Technoboost !</p>
                """,
                unsafe_allow_html=True
            )

        # Centering the logo
        with col2:
            inner_col1, inner_col2, inner_col3 = st.columns([0.85, 0.5, 0.85])  
            with inner_col2:
                st.markdown(f"<div style='height: {st.session_state.logo_spacing}px;'></div>", unsafe_allow_html=True)
                st.image("https://raw.githubusercontent.com/ShivarajMBB/Streamlit-repo/master/Logo.png", width=150)


# -------------------------- PAGE 2: FILE UPLOAD ------------------------------
elif st.session_state.page == "upload":
    
    if not st.session_state.authenticated:
        switch_page("login")  # Redirect to login if not authenticated
        
    with main_container.container():

        st.markdown(
            """
            <style>
                .sign-in-title {
                    text-align: center;
                    font-weight: bold;
                    margin-bottom: -10px;
                }
                .sign-in-subtext {
                    text-align: center;
                    font-size: 14px;
                    color: #6c757d;
                    margin-top: -10px;
                }
                .stButton > button {
                    width: 100%; /* Make button full width */
                    padding: 12px; /* Increase button height */
                    font-size: 18px; /* Increase font size */
                    font-weight: bold;
                    background-color: #007BFF; /* Blue background */
                    color: white;
                    border: none;
                    border-radius: 8px; /* Rounded corners */
                    cursor: pointer;
                }
                .stButton > button:hover {
                    background-color: #0056b3; /* Darker blue on hover */
                }
            </style>
            <h2 class='sign-in-title'>Upload Documents</h2>
            <p class='sign-in-subtext'>Upload documents to process the report</p>
            """,
            unsafe_allow_html=True
        )
    
        # Initialize logo spacing if not already set
        if "logo_spacing" not in st.session_state:
            st.session_state.logo_spacing = 300  # Default spacing
        
        st.session_state.logo_spacing = 300
        
        # Centering file uploader
        col1, col2, col3 = st.columns([1.5, 2, 1.5])  
        with col2:
            uploaded_file = st.file_uploader("", type=["csv", "xls", "xlsx"])  
            
            if uploaded_file:
                st.success("File uploaded successfully!")    
                st.session_state.file_uploaded = True
                st.session_state.uploaded_file = uploaded_file  # Store actual file object
                st.session_state.uploaded_filename = uploaded_file.name
                st.session_state.logo_spacing = 115
            
                if st.button("Continue"):  
                    switch_page("loading") # Ensures smooth transition after button click
            
            # Footer text
            st.markdown(
                """
                <style>
                    .rights-text {
                        text-align: center;
                        font-size: 12px;
                        color: #6c757d;
                        margin-top: 20px;
                    }
                </style>
                <p class='rights-text'>© 2024 All Rights Reserved. Made with love by Technoboost !</p>
                """,
                unsafe_allow_html=True
            )
    
        with col2:  
            inner_col1, inner_col2, inner_col3 = st.columns([0.85, 0.5, 0.85])  
            with inner_col2:
                st.markdown(f"<div style='height: {st.session_state.logo_spacing}px;'></div>", unsafe_allow_html=True)  
                st.image("https://raw.githubusercontent.com/ShivarajMBB/Streamlit-repo/master/Logo.png", width=150, use_container_width=False)

# ----------------------------- PAGE 3: LOADING --------------------------------
elif st.session_state.page == "loading":
    if not st.session_state.file_uploaded:
        switch_page("upload")  # Redirect to upload if file is missing

    with main_container.container():
        title_subtext_placeholder = st.empty()  # Placeholder for title & subtext

        # Centered progress bar layout
        col1, col2, col3 = st.columns([1.5, 1.5, 1.5])  
        with col2:
            progress_bar = st.progress(0)  # Initialize progress bar in the center
        
        uploaded_file = st.session_state.get("uploaded_file")  # Retrieve uploaded file

        # Function to load data
        @st.cache_data
        def load_data(uploaded_file):
            time.sleep(1)  # Simulate loading time
            try:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith((".xls", ".xlsx")):
                    df = pd.read_excel(uploaded_file)
                else:
                    return None  # Return None for unsupported formats
                return df
            except Exception:
                return None  # Return None if loading fails
        
        # Load data and store in session state
        df = None
        if uploaded_file:
            df = load_data(uploaded_file)
            st.session_state.df = df  # Store loaded dataframe in session state

        # Extract unique email domains
        def extract_email_domains(df):
            email_column = None
            for col in df.columns:
                if "email" in col.lower():  # Identify email column
                    email_column = col
                    break
            
            if email_column:
                df[email_column] = df[email_column].astype(str)  # Ensure string type
                df["domain"] = df[email_column].apply(lambda x: x.split('@')[1] if '@' in x else None)
                unique_domains = df["domain"].dropna().unique().tolist()  # Get unique domains
                return unique_domains, email_column
            return [], None
        
        # Process email domains if dataframe exists
        if df is not None:
            unique_domains, email_column = extract_email_domains(df)
            st.session_state.unique_domains = unique_domains  # Store unique domains

        # Ensure selection flags are set in session state
        if "selection_complete" not in st.session_state:
            st.session_state.selection_complete = False

        if "domain_filtering" not in st.session_state:
            st.session_state.domain_filtering = None  # Track if user wants domain filtering
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Ask user whether they want to filter by email domain
        st.subheader("Do you want to filter Internals by email domain?")
        filter_choice = st.radio("Choose an option:", ["Yes", "No"], key="domain_filtering")

         # If user chooses "Yes", show domain selection
        if filter_choice == "Yes":
            st.subheader("Select Internal Email Domains")
            selected_domains = st.multiselect("Choose Internal domains:", st.session_state.unique_domains, key="selected_domains")
        
            # Continue button appears only when a selection is made
            if selected_domains and st.button("Continue"):
                st.session_state.selection_complete = True  # Mark selection as complete
        
                # Update 'User Domain' based on selection
                if df is not None and email_column:
                    df["User Domain"] = df[email_column].apply(
                        lambda x: "Internal" if "@" in str(x) and x.split('@')[1] in selected_domains else "External"
                    )
        
                    # Remove 'domain' column after processing
                    if "domain" in df.columns:
                        df.drop(columns=["domain"], inplace=True)
        
                    st.session_state.df = df  # Update session state with processed df
                
                # Show progress animation
                for i in range(1, 101):
                    time.sleep(0.01)  # Smoother progress update 
                    title_subtext_placeholder.markdown(
                        f"""
                        <div style="text-align: center;">
                            <h2 style="margin-bottom: -10px;">Processing... {i}%</h2>
                            <p style="font-size: 14px; color: #6c757d; margin-top: 0px; margin-bottom: 10px;">
                            Please wait till we process the report</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    progress_bar.progress(i)  # Update progress inside loop
        
                # Move to dashboard after progress completes
                st.session_state.page = "dashboard"
                st.session_state.loading_complete = True
                st.rerun()
        
        # If user selects "No", move to dashboard without changing 'User Domain'
        elif filter_choice == "No":
            st.session_state.selection_complete = True  # Mark selection as complete
        
            # No changes to df, just proceed to dashboard
            
            # Show progress animation before switching pages
            for i in range(1, 101):
                time.sleep(0.01)
                title_subtext_placeholder.markdown(
                    f"""
                    <div style="text-align: center;">
                        <h2 style="margin-bottom: -10px;">Processing... {i}%</h2>
                        <p style="font-size: 14px; color: #6c757d; margin-top: 0px; margin-bottom: 10px;">
                        Please wait till we process the report</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                progress_bar.progress(i)
        
            st.session_state.page = "dashboard"
            st.session_state.loading_complete = True
            st.rerun()


        # If data fails to load, show error message
        if df is None:
            st.error("Failed to load file. Please check the file format and try again.")


# ----------------------------- PAGE 4: DASHBOARD -----------------------------
# =============================================================================
# elif "page" not in st.session_state:
#     st.session_state.page = "dashboard"
# 
# if "loading_complete" not in st.session_state:
#     st.session_state.loading_complete = True  # Set to False if loading logic is needed
# =============================================================================
elif st.session_state.page == "dashboard":
    if not st.session_state.loading_complete:
        st.session_state.page = "loading"
        st.rerun()

    # Function to filter users
    def filter_users(df, user_types, matching_columns):
        filtered = {user_type: df[df["User Type"] == user_type].copy() for user_type in user_types}
        
        no_access = {
            user_type: filtered[user_type][(filtered[user_type][matching_columns] == 0).all(axis=1)]
            for user_type in user_types
        }

        downgrade = {
            user_type: filtered[user_type][(filtered[user_type][matching_columns[0]] != 0) & 
                                           (filtered[user_type][matching_columns[2]] == 0) & 
                                           (filtered[user_type][matching_columns[3]] == 0)]
            for user_type in user_types if user_type not in ["Viewer", "Guest"]
        }

        return (filtered, no_access, downgrade) if downgrade else (filtered, no_access)
    
# =============================================================================
#     active_licenses = df[df["Status"] == "Active"].shape[0]
#     inactive_licenses = total_licenses - active_licenses
#     savings_per_license = 2.14  # Adjust based on pricing logic
#     potential_monthly_savings = inactive_licenses * savings_per_license
#     potential_annual_savings = potential_monthly_savings * 12
# =============================================================================

    # Set background color and styling
    st.markdown(
        """
        <style>
        /* Set background color for the entire app */
        .stApp {
            background-color: #f7f7f7;  /* Light grey */
        }

        /* White background container */
        .white-background {
            background-color: white;
            padding: 10px;
            border-radius: 40px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            width: 100%;
            min-height: 50px;
            display: flex;
            align-items: center;
            justify-content: space-between; /* Pushes user image to the right */
            position: relative;
        }
        
        /* Logo container (left) */
        .logo-container {
            flex-shrink: 0;
            margin-left: 10px;
            position: absolute;
            left: 10px;
        }
        
        /* Make the logo rounded */
        .logo-container img {
            width: 110px;
            border-radius: 15px; /* Makes the logo circular */
            object-fit: cover;  /* Ensures it fits properly */
        }
        
        /* User image container (right) */
        .user-image {
            flex-shrink: 0;
            margin-right: 10px; /* Push to the extreme right */
            position: absolute;
            right: 10px;
        }
        
        /* Make the user image rounded */
        .user-image img {
            width: 35px; /* Adjust size */
            height: 35px;
            border-radius: 50%; /* Makes it circular */
            object-fit: cover;  /* Prevents stretching */
            border: 2px solid #ccc; /* Optional border */
        }
        
        /* Custom metric container */
        .custom-metric {
            background: white;
            padding: 12px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            text-align: left;
            margin: 6px;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }

        /* Metric image */
        .metric-image {
            flex-shrink: 0;
            width: 35px;
            height: 25px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .metric-image img {
            width: 100%;
            height: auto;
        }

        /* Label and Value */
        .metric-data {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }

        /* Metric label */
        .metric-label {
            font-size: 14px;
            font-weight: bold;
            margin-bottom: -5px;
        }

        /* Metric value */
        .metric-value {
            font-size: 1.3em;
            font-weight: bold;
            color: #007BFF;
        }
        /* Override Streamlit's button styles */
        div.stButton > button {
            width: 110px !important;  /* Set a smaller width */
            height: 5px !important;  /* Set a smaller height */
            font-size: 14px !important; /* Adjust font size */
            font-weight: bold;
            background-color: #2B3674; /* Custom color */
            color: white;
            border: none;
            border-radius: 8px; /* Rounded corners */
            cursor: pointer;
            padding: 0px 0px !important; /* Reduce internal padding */
            line-height: 10px !important; /* Adjust line height */
        }

        /* Optional: Center the button inside the column */
        div.stButton {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .stButton > button:hover {
            background-color: #2B3674; /* Darker blue on hover */
        }
        
        /* File name styling */
        .filename-container {
            text-align: center;
            font-size: 16px;
            font-weight: bold;
            color: #2B3674;
            background-color: #A3AED0; /* Light blue background */
            padding: 7px 16.5px;
            border-radius: 8px;
            white-space: nowrap;
            display: inline-block;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Get the filename from session state or use default if not present
    filename_to_display = st.session_state.uploaded_filename
    
    # Display logo and filename at the top (no movement)
    st.markdown(
        """
        <div class="white-background">
            <div class="logo-container">
                <img src="https://raw.githubusercontent.com/ShivarajMBB/Streamlit-repo/master/Logo.png">
            </div>
            <div class="user-image">
                <img src="https://randomuser.me/api/portraits/men/75.jpg">  <!-- Example user image -->
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Create four columns: col1 for filename, col2 for spacing, col3 for button 1, col4 for button 2
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1.3,1.3, 1.2, 1.2, 3.3, 1, 1])

    with col1:
        # Initialize session state for license cost input
        if "license_cost" not in st.session_state:
            st.session_state.license_cost = "$500.00"  # Default value with "$"
        
        if "license_adjustment" not in st.session_state:
            st.session_state.license_adjustment = 500.00  # Default numeric value
    
        # Function to update session state dynamically
        def format_currency():
            user_input = st.session_state.license_cost.strip()
    
            # Ensure "$" stays in the input
            if not user_input.startswith("$"):
                user_input = "$" + user_input
                st.session_state.license_cost = user_input  # Update UI immediately
    
            # Extract numeric value and store in session state
            try:
                st.session_state.license_adjustment = float(user_input.replace("$", "").replace(",", "").strip())
            except ValueError:
                st.session_state.license_adjustment = 0.0  # Default if input is invalid
    
        # Text input directly bound to session state
        st.text_input(
            "  Enter per license cost:", 
            key="license_cost",
            on_change=format_currency  # Updates both UI and calculation immediately
        )
        
    with col2:
        # Initialize session state for total licenses
        if "total_license" not in st.session_state:
            st.session_state.total_license = 0  # Default value
    
        # Function to update total_license dynamically
        def update_total_license():
            try:
                st.session_state.total_license = int(st.session_state.total_license)
            except ValueError:
                st.session_state.total_license = 0  # Default if input is invalid
    
        # Number input bound to session state
        st.number_input(
            "Total existing licenses:", 
            min_value=0,  # Prevents negative values
            value=st.session_state.total_license,  # Default from session state
            step=1,  # Ensures only whole numbers
            format="%d",  # Integer format (no decimals)
            key="total_license",  # Directly binds session state
            on_change=update_total_license  # Updates session state dynamically
        )
        
    with col3:
        st.session_state.inactive_days_internal = st.session_state.get("inactive_days_internal", 90)  # Default value
        st.selectbox(
            "Internals Inactive days",
            options=[90, 180, 270, 365],
            key="inactive_days_internal"  # Directly binds to session state
        )
    
    # External inactive days selection
    with col4:
        st.session_state.inactive_days_external = st.session_state.get("inactive_days_external", 90)  # Default value
        st.selectbox(
            "Externals Inactive days",
            options=[90, 180, 270, 365],
            key="inactive_days_external"  # Directly binds to session state
        )
        
    # Show the filename in col1 inside a properly styled div
    with col6:
        st.markdown(
            f"<div class='filename-container'>{filename_to_display}</div>",
            unsafe_allow_html=True
        )
    
    # Show "Change File" button in col3
    with col7:
        if st.button("Change File"):
            switch_page("upload")  # Navigate to upload page
        
# =============================================================================
#     if "inactive_days" not in st.session_state:
#         st.session_state.inactive_days = 90  # Default value
#     if "license_cost" not in st.session_state:
#         st.session_state.license_cost = "$20.00"  # Default value
#     if "license_adjustment" not in st.session_state:
#         st.session_state.license_adjustment = 20.00  # Default numeric value
#     if "total_license" not in st.session_state:
#         st.session_state.total_license = 2500  # Default value
# =============================================================================
    
    current_smartsheet_cost =  st.session_state.license_adjustment * st.session_state.total_license
    
    df = st.session_state.get("df")
    
    df_internal = df[df["User Domain"] == "Internal"]
    df_external = df[df["User Domain"] == "External"]
    
    user_counts = {
        "Internal Users": len(df_internal),
        "External Users": len(df_external)
    }
    
    member_counts = (df_internal["User Type"] == "Member").sum() + (df_external["User Type"] == "Member").sum()

    # Define different keywords for internal and external users
    internal_keywords = [str(st.session_state.get("inactive_days_internal", 90))]  # Default to 90 if missing
    external_keywords = [str(st.session_state.get("inactive_days_external", 90))]
    
    # Find matching columns for internal and external users separately
    internal_matching_columns = [col for col in df.columns if any(keyword.lower() in col.lower() for keyword in internal_keywords)]
    external_matching_columns = [col for col in df.columns if any(keyword.lower() in col.lower() for keyword in external_keywords)]

    # Define user types
    user_types = {
        "internal": ["Member", "Provisional Member", "Viewer"],
        "external": ["Guest", "Provisional Member", "Viewer"]
    }

    # Apply filtering for internal users
    result_internal = filter_users(df_internal, user_types["internal"], internal_matching_columns)
    if len(result_internal) == 3:
        df_internal_filtered, df_internal_No_access, df_internal_downgrade = result_internal
    else:
        df_internal_filtered, df_internal_No_access = result_internal
        df_internal_downgrade = {}
    
    # Apply filtering for external users
    result_external = filter_users(df_external, user_types["external"], external_matching_columns)
    if len(result_external) == 3:
        df_external_filtered, df_external_No_access, df_external_downgrade = result_external
    else:
        df_external_filtered, df_external_No_access = result_external
        df_external_downgrade = {}

    # Retrieve the loaded dataframe
    df = st.session_state.get("df")
    total_licenses = len(df)
    active_licenses = (
        (
            df_internal_filtered.get("Member", pd.DataFrame()).shape[0]
            - df_internal_No_access.get("Member", pd.DataFrame()).shape[0]
            - df_internal_downgrade.get("Member", pd.DataFrame()).shape[0]
        ) +
        (
            df_internal_filtered.get("Provisional Member", pd.DataFrame()).shape[0]
            - df_internal_No_access.get("Provisional Member", pd.DataFrame()).shape[0]
            - df_internal_downgrade.get("Provisional Member", pd.DataFrame()).shape[0]
        )
    )
    current_licenses = (
        df_internal_filtered.get("Member", pd.DataFrame()).shape[0]
        - df_internal_No_access.get("Member", pd.DataFrame()).shape[0]
        - df_internal_downgrade.get("Member", pd.DataFrame()).shape[0]
    )
    
# =============================================================================
#     domain_counts = {
#         "Guest": (df_internal_filtered.get("Guest", pd.DataFrame()).shape[0] + df_external_filtered.get("Guest", pd.DataFrame()).shape[0]),
#         "Member": (df_internal_filtered.get("Member", pd.DataFrame()).shape[0] + df_external_filtered.get("Member", pd.DataFrame()).shape[0]),
#         "Provisional Member": (df_internal_filtered.get("Provisional Member", pd.DataFrame()).shape[0] + df_external_filtered.get("Provisional Member", pd.DataFrame()).shape[0]),
#         "Viewer": (df_internal_filtered.get("Viewer", pd.DataFrame()).shape[0] + df_external_filtered.get("Viewer", pd.DataFrame()).shape[0])
#     }
# =============================================================================
    
    domain_counts_external = {
        "Guest": (df_external_filtered.get("Guest", pd.DataFrame()).shape[0]),
        "Member": (df_external_filtered.get("Member", pd.DataFrame()).shape[0]),
        "Provisional Member": (df_external_filtered.get("Provisional Member", pd.DataFrame()).shape[0]),
        "Viewer": (df_external_filtered.get("Viewer", pd.DataFrame()).shape[0])
    }
    
    domain_counts_internal = {
        "Guest": (df_internal_filtered.get("Guest", pd.DataFrame()).shape[0]),
        "Member": (df_internal_filtered.get("Member", pd.DataFrame()).shape[0]),
        "Provisional Member": (df_internal_filtered.get("Provisional Member", pd.DataFrame()).shape[0]),
        "Viewer": (df_internal_filtered.get("Viewer", pd.DataFrame()).shape[0])
    }
    
    inactive_counts = {
        "Guest": (df_internal_No_access.get("Guest", pd.DataFrame()).shape[0] + df_external_No_access.get("Guest", pd.DataFrame()).shape[0]),
        "Member": (df_internal_No_access.get("Member", pd.DataFrame()).shape[0] + df_external_No_access.get("Member", pd.DataFrame()).shape[0]),
        "Provisional Member": (df_internal_No_access.get("Provisional Member", pd.DataFrame()).shape[0] + df_external_No_access.get("Provisional Member", pd.DataFrame()).shape[0]),
        "Viewer": (df_internal_No_access.get("Viewer", pd.DataFrame()).shape[0] + df_external_No_access.get("Viewer", pd.DataFrame()).shape[0])
    }

    active_counts = {
        "Guest": ((df_external_filtered.get("Guest", pd.DataFrame()).shape[0] - df_external_No_access.get("Guest", pd.DataFrame()).shape[0]) + 
                  (df_internal_filtered.get("Guest", pd.DataFrame()).shape[0] - df_internal_No_access.get("Guest", pd.DataFrame()).shape[0])),
        "Member": ((df_external_filtered.get("Member", pd.DataFrame()).shape[0] - df_external_No_access.get("Member", pd.DataFrame()).shape[0]) +
                   (df_internal_filtered.get("Member", pd.DataFrame()).shape[0] - df_internal_No_access.get("Member", pd.DataFrame()).shape[0])),
        "Provisional Member": ((df_external_filtered.get("Provisional Member", pd.DataFrame()).shape[0] + df_external_No_access.get("Provisional Member", pd.DataFrame()).shape[0]) +
                               (df_internal_filtered.get("Provisional Member", pd.DataFrame()).shape[0] + df_internal_No_access.get("Provisional Member", pd.DataFrame()).shape[0])),
        "Viewer": ((df_external_filtered.get("Viewer", pd.DataFrame()).shape[0] - df_external_No_access.get("Viewer", pd.DataFrame()).shape[0]) + 
                   (df_internal_filtered.get("Viewer", pd.DataFrame()).shape[0] - df_internal_No_access.get("Viewer", pd.DataFrame()).shape[0]))
    }
    
    cost_after_trueup = st.session_state.license_adjustment * active_licenses
    
    downgrade_after_trueup = (df_external_filtered.get("Provisional Member", pd.DataFrame()).shape[0] +
                             df_internal_downgrade.get("Member", pd.DataFrame()).shape[0] + 
                             df_internal_No_access.get("Member", pd.DataFrame()).shape[0] +
                             df_internal_downgrade.get("Provisional Member", pd.DataFrame()).shape[0] + 
                             df_internal_No_access.get("Provisional Member", pd.DataFrame()).shape[0])
    
    potential_savings =  st.session_state.license_adjustment * downgrade_after_trueup
    
    # Display Key Metrics
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(
            f"""
            <div class="custom-metric">
                <div class="metric-image">
                    <img src="https://raw.githubusercontent.com/ShivarajMBB/Streamlit-repo/master/Icon-1.svg">
                </div>
                <div class="metric-data">
                    <div class="metric-label">Total Users</div>
                    <div class="metric-value">{total_licenses}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="custom-metric">
                <div class="metric-image">
                    <img src="https://raw.githubusercontent.com/ShivarajMBB/Streamlit-repo/master/Icon-2.svg">
                </div>
                <div class="metric-data">
                    <div class="metric-label"># Licenses after True-up</div>
                    <div class="metric-value">{active_licenses}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="custom-metric">
                <div class="metric-image">
                    <img src="https://raw.githubusercontent.com/ShivarajMBB/Streamlit-repo/master/Icon.svg">
                </div>
                <div class="metric-data">
                    <div class="metric-label">Current # Licenses</div>
                    <div class="metric-value">{member_counts}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="custom-metric">
                <div class="metric-image">
                    <img src="https://raw.githubusercontent.com/ShivarajMBB/Streamlit-repo/master/Icon-4.svg">
                </div>
                <div class="metric-data">
                    <div class="metric-label">Current smartsheet cost</div>
                    <div class="metric-value">{current_smartsheet_cost:.2f}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col5:
        st.markdown(
            f"""
            <div class="custom-metric">
                <div class="metric-image">
                    <img src="https://raw.githubusercontent.com/ShivarajMBB/Streamlit-repo/master/Icon-3.svg">
                </div>
                <div class="metric-data">
                    <div class="metric-label">cost after True-up</div>
                    <div class="metric-value">{cost_after_trueup:.2f}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(
            f"""
            <div class="custom-metric">
                <div class="metric-image">
                    <img src="https://raw.githubusercontent.com/ShivarajMBB/Streamlit-repo/master/Icon.svg">
                </div>
                <div class="metric-data">
                    <div class="metric-label">User possible to downgrade</div>
                    <div class="metric-value">{downgrade_after_trueup}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# =============================================================================
#     with col2:
#         st.markdown(
#             f"""
#             <div class="custom-metric">
#                 <div class="metric-image">
#                     <img src="">
#                 </div>
#                 <div class="metric-data">
#                     <div class="metric-label"></div>
#                     <div class="metric-value"></div>
#                 </div>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )
# 
#     with col3:
#         st.markdown(
#             f"""
#             <div class="custom-metric">
#                 <div class="metric-image">
#                     <img src="">
#                 </div>
#                 <div class="metric-data">
#                     <div class="metric-label"></div>
#                     <div class="metric-value"></div>
#                 </div>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )
#         
#     with col4:
#         st.markdown(
#             f"""
#             <div class="custom-metric">
#                 <div class="metric-image">
#                     <img src="">
#                 </div>
#                 <div class="metric-data">
#                     <div class="metric-label"></div>
#                     <div class="metric-value"></div>
#                 </div>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )
# =============================================================================

    with col5:
        st.markdown(
            f"""
            <div class="custom-metric">
                <div class="metric-image">
                    <img src="https://raw.githubusercontent.com/ShivarajMBB/Streamlit-repo/master/Icon-4.svg">
                </div>
                <div class="metric-data">
                    <div class="metric-label">Potential saving</div>
                    <div class="metric-value">{potential_savings:.2f}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
            
    # Display Charts
    col1, col2, col3, col4, col5 = st.columns([0.1,1.8,0.1,1.8,0.1])
    
    with col2:
        # Create pie chart data
        pie_data = pd.DataFrame({
            "User Type": list(user_counts.keys()),
            "Count": list(user_counts.values())
        })
    
        # Generate pie chart
        fig1 = px.pie(
            pie_data,
            values="Count",
            names="User Type",
            hole=0.5,  # Donut chart style
            color_discrete_sequence=["lightpink", "lightblue"]  # Adjust colors
        )
    
        # Customize title
        fig1.update_layout(
            title=dict(
                text="Internal vs External Users",
                font=dict(size=16, color="black"),
                x=0.35,  # Center the title
                y=0.96  
            ),
            legend=dict(
                title=dict(
                    text="User domain",  # Legend title
                    font=dict(size=14, color="black"),
                    side="left"  # Moves title above the legend items
                ),
                orientation="h",  # Horizontal legend
                font=dict(size=12, color="black"),
                yanchor="bottom",
                y=-0.2,  # Move below the chart
                xanchor="center",
                x=0.5  # Center the legend horizontally
            )
        )
    
        # Update percentage label styles
        fig1.update_traces(
            textinfo="percent",  # Show percentage + category labels
            textfont=dict(size=12, color="black", family="Arial Black"),  # Readable font
        )
    
        # Display chart in Streamlit
        st.plotly_chart(fig1, use_container_width=True)
    
    # License Cost by User Level (Donut Chart)
    with col4:
        # Convert data to DataFrame format
        df_external = pd.DataFrame({
            "User Level": list(domain_counts_external.keys()),
            "Cost": list(domain_counts_external.values())
        })
        
        df_internal = pd.DataFrame({
            "User Level": list(domain_counts_internal.keys()),
            "Cost": list(domain_counts_internal.values())
        })
        
        # Create Pie Chart Figure
        fig2 = go.Figure()
        
        # Add traces for both datasets
        fig2.add_trace(go.Pie(
            labels=df_external["User Level"],
            values=df_external["Cost"],
            hole=0.5,
            name="External Users"
        ))
        
        fig2.add_trace(go.Pie(
            labels=df_internal["User Level"],
            values=df_internal["Cost"],
            hole=0.5,
            name="Internal Users",
            visible=False  # Initially hidden
        ))
        
        # Add Dropdown Menu Inside Chart
        fig2.update_layout(
            updatemenus=[{
                "buttons": [
                    {
                        "label": "External Users",
                        "method": "update",
                        "args": [{"visible": [True, False]}]  # No title update
                    },
                    {
                        "label": "Internal Users",
                        "method": "update",
                        "args": [{"visible": [False, True]}]  # No title update
                    }
                ],
                "direction": "down",
                "showactive": True,
                "x": 0.5,
                "xanchor": "center",
                "y": 1.2,
                "yanchor": "top"
            }],
            title=dict(
                text="Guest vs Members vs Provisional vs Viewers",  # Static title
                font=dict(size=16, color="black"),
                x=0.27,  
                y=0.96  
            ),
            legend=dict(
                title=dict(
                    text="User Type",
                    font=dict(size=14, color="black"),
                    side="left"
                ),
                orientation="h",
                font=dict(size=12, color="black"),
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        
        # Update percentage label styles (bold, color, size)
        fig2.update_traces(
            textinfo="percent",
            textfont=dict(size=12, color="black", family="Arial Black")
        )
        
        # Display the Pie Chart in Streamlit
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        # Data
        inactive_data = pd.DataFrame({
            "User Level": list(inactive_counts.keys()),
            "Inactive Licenses": list(inactive_counts.values())
        })
    
        # Plotly Bar Chart
        fig1 = px.bar(
            inactive_data,
            x="User Level",
            y="Inactive Licenses",
            text_auto=True,
            color="User Level"
        )
    
        # Update Layout (No Legend)
        fig1.update_layout(
            title=dict(
                text="Inactive User by Type",
                x=0.06,  # Centers title
                y=0.96,
                font=dict(size=16)
            ),
            xaxis=dict(title=""),  # Remove X-axis title
            yaxis=dict(title=""),  # Remove Y-axis title
            showlegend=False  # Hide legend completely
        )
    
        # Update Label Styles (Bold, Black Color)
        fig1.update_traces(
            texttemplate="%{y}",  # Show values as text
            textfont=dict(size=12, color="black", family="Arial"),  # Bold & Color
        )
    
        # Display in Streamlit with unique key
        st.plotly_chart(fig1, use_container_width=True, key="inactive_chart")

    
    with col4:
        # Data
        active_data = pd.DataFrame({
            "User Level": list(active_counts.keys()),
            "Active Licenses": list(active_counts.values())  # Different dataset for Active Licenses
        })
    
        # Plotly Bar Chart
        fig2 = px.bar(
            active_data,  # Correct dataset
            x="User Level",
            y="Active Licenses",
            text_auto=True,
            color="User Level"
        )
    
        # Update Layout
        fig2.update_layout(
            title=dict(
                text="Active User by Type",
                x=0.06,  # Centers title
                y=0.96,
                font=dict(size=16)
            ),
            xaxis=dict(title=""),  # Remove X-axis title
            yaxis=dict(title=""),  # Remove Y-axis title
            showlegend=False  # Hide legend completely
        )
        
        # Update Label Styles (Bold, Black Color)
        fig2.update_traces(
            texttemplate="%{y}",  # Show values as text
            textfont=dict(size=12, color="black", family="Arial"),  # Bold & Color
        )
    
        # Display in Streamlit with unique key
        st.plotly_chart(fig2, use_container_width=True, key="active_chart")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Collect emails for downgrade to guest
    downgrade_to_guest_emails = []
    
    # For each user type, find emails that should be downgraded to Guest
    # These are users in the filtered list but not in the no access list
    user_types_list = ["Guest", "Member", "Provisional Member", "Viewer"]
    
    for user_type in user_types_list:
        filtered_df = df_external_filtered.get(user_type, pd.DataFrame())
        no_access_df = df_external_No_access.get(user_type, pd.DataFrame())
        
        if not filtered_df.empty and 'Email' in filtered_df.columns:
            # For each user type, get emails that are in filtered but not in no_access
            if not no_access_df.empty and 'Email' in no_access_df.columns:
                emails_to_add = filtered_df[~filtered_df['Email'].isin(no_access_df['Email'])]['Email'].tolist()
            else:
                emails_to_add = filtered_df['Email'].tolist()
            
            downgrade_to_guest_emails.extend(emails_to_add)
    
    # Collect emails for downgrade to no access
    downgrade_to_no_access_emails = []
    
    # For each user type, find emails that should be downgraded to No Access
    # These are users in the no access list
    for user_type in user_types_list:
        no_access_df = df_external_No_access.get(user_type, pd.DataFrame())
        
        if not no_access_df.empty and 'Email' in no_access_df.columns:
            downgrade_to_no_access_emails.extend(no_access_df['Email'].tolist())
    
    # Remove duplicates while preserving order
    downgrade_to_guest_emails = list(dict.fromkeys(downgrade_to_guest_emails))
    downgrade_to_no_access_emails = list(dict.fromkeys(downgrade_to_no_access_emails))
    
    # Create the DataFrame with appropriate lengths
    max_length = max(len(downgrade_to_guest_emails), len(downgrade_to_no_access_emails))
    downgrade_to_guest_emails.extend([None] * (max_length - len(downgrade_to_guest_emails)))
    downgrade_to_no_access_emails.extend([None] * (max_length - len(downgrade_to_no_access_emails)))
    
    # Create the downgrade recommendations DataFrame
    downgrade_df_external = pd.DataFrame({
        'Downgrade to Guest': downgrade_to_guest_emails,
        'Downgrade to No Access': downgrade_to_no_access_emails
    })
    
    int_active_members = (df_internal_filtered.get("Member", pd.DataFrame()).shape[0] - df_internal_No_access.get("Member", pd.DataFrame()).shape[0])
    int_active_prov = (df_internal_filtered.get("Provisional Member", pd.DataFrame()).shape[0] - df_internal_No_access.get("Provisional Member", pd.DataFrame()).shape[0])
    
    data_external = {
        "User Level": ["Guest", "Member", "Provisional Member", "Viewer"],
        "Total Licenses": [
            df_external_filtered.get("Guest", pd.DataFrame()).shape[0],
            df_external_filtered.get("Member", pd.DataFrame()).shape[0],
            df_external_filtered.get("Provisional Member", pd.DataFrame()).shape[0], 
            df_external_filtered.get("Viewer", pd.DataFrame()).shape[0]
        ],
        "Downgrade to Guset": [
            df_external_filtered.get("Guest", pd.DataFrame()).shape[0] - df_external_No_access.get("Guest", pd.DataFrame()).shape[0],
            df_external_filtered.get("Member", pd.DataFrame()).shape[0] - df_external_No_access.get("Member", pd.DataFrame()).shape[0], 
            df_external_filtered.get("Provisional Member", pd.DataFrame()).shape[0] - df_external_No_access.get("Provisional Member", pd.DataFrame()).shape[0], 
            df_external_filtered.get("Viewer", pd.DataFrame()).shape[0] - df_external_No_access.get("Viewer", pd.DataFrame()).shape[0]
        ],
        "Downgrade to No Access": [
            df_external_No_access.get("Guest", pd.DataFrame()).shape[0], 
            df_external_No_access.get("Member", pd.DataFrame()).shape[0], 
            df_external_No_access.get("Provisional Member", pd.DataFrame()).shape[0], 
            df_external_No_access.get("Viewer", pd.DataFrame()).shape[0]
        ],
        "Recommendations": ["Revoke the inactive ID's                                                                                                                              ",
                            "Downgrade all the active licenses to (Guest), Revoke the inactive once",
                            "Downgrade all the active licenses to (Guest), Revoke the inactive once",
                            "Downgrade all the active licenses to (Guest), Revoke the inactive once"]
    }

# =============================================================================
#     provisional_savings_members = (
#         df_internal_No_access.get("Member", pd.DataFrame()).shape[0] +
#         df_internal_downgrade.get("Member", pd.DataFrame()).shape[0]
#     ) * st.session_state.license_adjustment
#     
#     provisional_savings = (
#         df_internal_No_access.get("Provisional Member", pd.DataFrame()).shape[0] +
#         df_internal_downgrade.get("Provisional Member", pd.DataFrame()).shape[0]
#     ) * st.session_state.license_adjustment
# 
# =============================================================================
    
    data_internal = {
        "User Level": [ "Member", "Provisional Member", "Viewer"],
        "Total Licenses": [
            df_internal_filtered.get("Member", pd.DataFrame()).shape[0],
            df_internal_filtered.get("Provisional Member", pd.DataFrame()).shape[0], 
            df_internal_filtered.get("Viewer", pd.DataFrame()).shape[0]
        ],
        "Need to be Member": [
            df_internal_filtered.get("Member", pd.DataFrame()).shape[0] - df_internal_No_access.get("Member", pd.DataFrame()).shape[0]- df_internal_downgrade.get("Member", pd.DataFrame()).shape[0], 
            df_internal_filtered.get("Provisional Member", pd.DataFrame()).shape[0] - df_internal_No_access.get("Provisional Member", pd.DataFrame()).shape[0] - df_internal_downgrade.get("Provisional Member", pd.DataFrame()).shape[0], 
            0
        ],
        "Downgrade to Viewer": [
            df_internal_downgrade.get("Member", pd.DataFrame()).shape[0], 
            df_internal_downgrade.get("Provisional Member", pd.DataFrame()).shape[0], 
            df_internal_filtered.get("Viewer", pd.DataFrame()).shape[0] - df_internal_No_access.get("Viewer", pd.DataFrame()).shape[0] - df_internal_downgrade.get("Viewer", pd.DataFrame()).shape[0]
        ],
        "Downgrade to No Access": [ 
            df_internal_No_access.get("Member", pd.DataFrame()).shape[0], 
            df_internal_No_access.get("Provisional Member", pd.DataFrame()).shape[0], 
            df_internal_No_access.get("Viewer", pd.DataFrame()).shape[0]
        ],
        "Recommendations": [f"Out of {int_active_members} Active Licenses Downgrade {df_internal_downgrade.get('Member', pd.DataFrame()).shape[0]} to Viewers, Revoke the Inactive Licenses",
                            f"Out of {int_active_prov} Active Licenses Downgrade {df_internal_downgrade.get('Provisional Member', pd.DataFrame()).shape[0]} to Viewers, Revoke the inactive licenses",
                            "         Revoke the inactive ID's                                                                                                                              "]
    }
    
    df_report = pd.DataFrame(data_external)
    
    df_report_2 = pd.DataFrame(data_internal)

    # Function to create a download link for a dataframe
    def get_download_link(df_to_download, filename="data.csv"):
        csv = df_to_download.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        return f'data:file/csv;base64,{b64}'
    
    st.markdown("""
        <style>
            .custom-header {
                font-size: 14px;
                font-weight: bold;
                color: black;
                background-color: #e6e9f0;
                padding: 4px;
                border-radius: 5px;
                text-align: center;
            }
        </style>
        <div class="custom-header">Detailed License Report for Externals</div>
    """, unsafe_allow_html=True)
    
    # Add a column for downloads if it doesn't exist
    if "Download" not in df_report.columns:
        df_report["Download"] = "Download"
    
    # Configure the data editor for the external report
    edited_external = st.data_editor(
        df_report,
        column_config={
            "Download": st.column_config.LinkColumn(
                "Download",
                help="Click to download this row",
                display_text="Download",
                validate="^Download$"
            )
        },
        hide_index=True,
        use_container_width=True,
        key="external_table"
    )
    
    # Handle download clicks
    if st.session_state.get("external_table_edited_rows"):
        for idx in st.session_state["external_table_edited_rows"]:
            row_data = df_report.iloc[idx:idx+1]
            st.download_button(
                label=f"Download selected row",
                data=row_data.to_csv(index=False),
                file_name=f"external_data_row_{idx}.csv",
                mime="text/csv",
                key=f"download_ext_{idx}"
            )
    
    st.markdown("""
        <div class="custom-header">Detailed License Report for Internals</div>
    """, unsafe_allow_html=True)
    
    # Add a column for downloads if it doesn't exist
    if "Download" not in df_report_2.columns:
        df_report_2["Download"] = "Download"
    
    # Configure the data editor for the internal report
    edited_internal = st.data_editor(
        df_report_2,
        column_config={
            "Download": st.column_config.LinkColumn(
                "Download",
                help="Click to download this row",
                display_text="Download",
                validate="^Download$"
            )
        },
        hide_index=True,
        use_container_width=True,
        key="internal_table"
    )
    
    # Handle download clicks
    if st.session_state.get("internal_table_edited_rows"):
        for idx in st.session_state["internal_table_edited_rows"]:
            row_data = df_report_2.iloc[idx:idx+1]
            st.download_button(
                label=f"Download selected row",
                data=row_data.to_csv(index=False),
                file_name=f"internal_data_row_{idx}.csv",
                mime="text/csv",
                key=f"download_int_{idx}"
            )
    
# =============================================================================
#     # Alternative approach using buttons
#     st.subheader("Alternative Approach with Buttons")
#     
#     # Create tabs for the two tables
#     tab1, tab2 = st.tabs(["External Licenses", "Internal Licenses"])
#     
#     with tab1:
#         # Display the table
#         st.dataframe(df_report, hide_index=True, use_container_width=True)
#         
#         # Add row selection with standard widgets
#         col1, col2 = st.columns([3, 1])
#         with col1:
#             row_options = [f"Row {i+1}: {df_report.iloc[i].get('Name', '') or df_report.iloc[i].get('ID', i)}" 
#                           for i in range(len(df_report))]
#             selected_rows = st.multiselect("Select rows to download:", row_options, key="ext_select")
#         
#         with col2:
#             if selected_rows:
#                 indices = [int(row.split(":")[0].replace("Row ", "")) - 1 for row in selected_rows]
#                 selected_data = df_report.iloc[indices].copy()
#                 
#                 st.download_button(
#                     label="Download Selected",
#                     data=selected_data.to_csv(index=False),
#                     file_name="selected_external_data.csv",
#                     mime="text/csv",
#                     key="download_ext_multi"
#                 )
#     
#     with tab2:
#         # Display the table
#         st.dataframe(df_report_2, hide_index=True, use_container_width=True)
#         
#         # Add row selection with standard widgets
#         col1, col2 = st.columns([3, 1])
#         with col1:
#             row_options = [f"Row {i+1}: {df_report_2.iloc[i].get('Name', '') or df_report_2.iloc[i].get('ID', i)}" 
#                           for i in range(len(df_report_2))]
#             selected_rows = st.multiselect("Select rows to download:", row_options, key="int_select")
#         
#         with col2:
#             if selected_rows:
#                 indices = [int(row.split(":")[0].replace("Row ", "")) - 1 for row in selected_rows]
#                 selected_data = df_report_2.iloc[indices].copy()
#                 
#                 st.download_button(
#                     label="Download Selected",
#                     data=selected_data.to_csv(index=False),
#                     file_name="selected_internal_data.csv",
#                     mime="text/csv",
#                     key="download_int_multi"
#                 )
# =============================================================================
