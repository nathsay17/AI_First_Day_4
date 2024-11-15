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

tint = """
    <style>
        .streamlit-expanderHeader {
            font-size: 16px;
            color: white;
        }
        .dataframe tbody tr th, .dataframe tbody tr td {
            background-color: rgba(255, 255, 255, 0.3);  /* White background with 30% opacity */
            color: white;  /* Set text color to white for better contrast */
        }
        .dataframe thead {
            background-color: rgba(255, 255, 255, 0.5);  /* Header background with 50% opacity */
        }
        .dataframe {
            border: 2px solid rgba(255, 255, 255, 0.3); /* Transparent border */
            border-radius: 10px;
        }
    </style>
"""
