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
            -1px -1px 0 #000,  
            1px -1px 0 #000,
            -1px 1px 0 #000,
            1px 1px 0 #000; 
        font-size: 32px;
    }}
    .outlined-text p {{
        font-size: 32px !important;  /* Force font size change for paragraphs */
        color: white;
        text-shadow: 
            -1px -1px 0 #000,  
            1px -1px 0 #000,
            -1px 1px 0 #000,
            1px 1px 0 #000; 
    }}
    .outlined-text ul, .outlined-text li {{
        font-size: 32px !important;  /* Force font size change for list items */
        color: white;
        text-shadow: 
            -1px -1px 0 #000,  
            1px -1px 0 #000,
            -1px 1px 0 #000,
            1px 1px 0 #000;        
    }}
    </style>
    '''
