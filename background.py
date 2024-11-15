tint = """
    <style>
        .streamlit-expanderHeader {
            font-size: 16px;
            color: white;
        }
        .custom-table tbody tr th, .custom-table tbody tr td {
            background-color: rgba(255, 255, 255, 0.3) !important;  /* White background with 30% opacity */
            color: white !important;  /* Set text color to white for better contrast */
        }
        .custom-table thead {
            background-color: rgba(255, 255, 255, 0.5) !important;  /* Header background with 50% opacity */
        }
        .custom-table {
            border: 2px solid rgba(255, 255, 255, 0.3) !important; /* Transparent border */
            border-radius: 10px !important;
        }
    </style>
"""



def apply_background(image_base64):
    return f'''
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{image_base64}"); 
        background-size: contain;
        background-position: right;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .outlined-text {{
        color: #3b718f;
        text-shadow: 
            -1px -1px 0 #ffffff,  
            1px -1px 0 #ffffff,
            -1px 1px 0 #ffffff,
            1px 1px 0 #ffffff; 
        font-size: 32px;
    }}
    </style>
    '''

