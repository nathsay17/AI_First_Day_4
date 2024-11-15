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
