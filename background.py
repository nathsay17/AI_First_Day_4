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
        color: white;
        text-shadow: 
            -1px -1px 0 #3b718f,  
            1px -1px 0 #3b718f,
            -1px 1px 0 #3b718f,
            1px 1px 0 #3b718f; 
        font-size: 32px;
    }}
    </style>
    '''
