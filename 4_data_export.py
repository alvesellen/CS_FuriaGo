import streamlit as st
import pandas as pd
import os
from utils import initialize_session_state, filter_sidebar, apply_filters
from data_processing import export_data_to_csv, export_data_to_json

# Set page config
st.set_page_config(
    page_title="FURIA Fan Data Export",
    page_icon="📤",
    layout="wide"
)

# Initialize session state
initialize_session_state()

# Page title
st.title("FURIA Fan Data Export")
st.markdown("""
    Export fan data for further analysis or integration with other systems. 
    Apply filters to export specific segments of fan data in various formats.
""")

# Sidebar for filters
filter_sidebar()

# Get filtered data
if 'fan_data' in st.session_state and not st.session_state.fan_data.empty:
    filtered_data = apply_filters(st.session_state.fan_data)
    
    # Display number of fans after filtering
    st.info(f"Ready to export data for {len(filtered_data)} fans")
    
    # Preview the data to be exported
    st.subheader("Data Preview")
    st.dataframe(filtered_data.head(10))
    
    # Export options
    st.subheader("Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # CSV Export
        st.markdown("### Export as CSV")
        csv_filename = st.text_input("CSV Filename", "furia_fan_data.csv")
        
        if st.button("Export to CSV"):
            if export_data_to_csv(filtered_data, csv_filename):
                st.success(f"Data successfully exported to {csv_filename}")
                
                # Create download link
                with open(csv_filename, 'rb') as f:
                    csv_data = f.read()
                
                st.download_button(
                    label="Download CSV File",
                    data=csv_data,
                    file_name=csv_filename,
                    mime="text/csv"
                )
            else:
                st.error("Error exporting data. Please try again.")
    
    with col2:
        # JSON Export
        st.markdown("### Export as JSON")
        json_filename = st.text_input("JSON Filename", "furia_fan_data.json")
        
        if st.button("Export to JSON"):
            if export_data_to_json(filtered_data, json_filename):
                st.success(f"Data successfully exported to {json_filename}")
                
                # Create download link
                with open(json_filename, 'rb') as f:
                    json_data = f.read()
                
                st.download_button(
                    label="Download JSON File",
                    data=json_data,
                    file_name=json_filename,
                    mime="application/json"
                )
            else:
                st.error("Error exporting data. Please try again.")
    
    # Advanced export options
    st.subheader("Advanced Export Options")
    
    # Column selection
    st.markdown("### Select Columns to Export")
    if not filtered_data.empty:
        all_columns = filtered_data.columns.tolist()
        selected_columns = st.multiselect("Select columns to include in export", all_columns, default=all_columns)
        
        if selected_columns:
            filtered_data_selected = filtered_data[selected_columns]
            
            st.markdown("### Preview Selected Columns")
            st.dataframe(filtered_data_selected.head(5))
            
            # Export with selected columns
            if st.button("Export Selected Columns to CSV"):
                selected_csv_filename = "furia_fan_data_selected.csv"
                if export_data_to_csv(filtered_data_selected, selected_csv_filename):
                    st.success(f"Selected columns successfully exported to {selected_csv_filename}")
                    
                    # Create download link
                    with open(selected_csv_filename, 'rb') as f:
                        selected_csv_data = f.read()
                    
                    st.download_button(
                        label="Download Selected Columns CSV",
                        data=selected_csv_data,
                        file_name=selected_csv_filename,
                        mime="text/csv"
                    )
                else:
                    st.error("Error exporting selected columns. Please try again.")
    
    # Data integration information
    st.subheader("Data Integration Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("https://images.unsplash.com/photo-1599474924187-334a4ae5bd3c", caption="Data analytics")
    
    with col2:
        st.markdown("""
            ### Using Exported Data
            
            The exported fan data can be used for:
            
            - Integration with CRM systems
            - Advanced analytics in tools like Excel, Power BI, or Tableau
            - Email marketing campaign segmentation
            - Custom reporting and presentations
            - Social media targeting and audience creation
            
            All data is exported in standard formats compatible with most data analysis tools.
        """)
else:
    st.image("https://images.unsplash.com/photo-1612801798930-288967b6d1ef", caption="Esports analytics")
    st.warning("No fan data available yet. Please collect fan information on the home page.")

# Data privacy note
st.markdown("---")
st.subheader("Data Privacy Notice")
st.info("""
    The exported data contains personal information about FURIA fans. 
    Please handle this data in accordance with applicable privacy laws and regulations. 
    Ensure that data is stored securely and used only for authorized purposes.
""")

# Footer
st.markdown("---")
st.markdown("© 2023 FURIA Sports Fan Analytics Platform | Data Export Module")
