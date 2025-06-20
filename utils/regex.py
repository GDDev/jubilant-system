# import re

re_f_name = r'^[^\W\d_]+$'
re_name = r'^([^\W\d_](\s)?)+$'
re_username = r'^(?!\d+$)[^\W]+$'
re_search = r'^(?!\d+$)([^\W](\s)?)+$'
re_text = r'^[\w\s,.\'"-:;?@!#$%&*()<>\\\/]+$'
re_email_open = r'\b[A-Za-z0-9._%+-]+@(gmail.com|hotmail.com|outlook.com|umc.br|alunos.umc.br)\b'
re_email_umc = r'\b[A-Za-z0-9._%+-]+@(alunos\.umc\.br|umc\.br)\b'
