#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试飞书各块类型"""
import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

r = requests.post('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
    json={'app_id':'cli_a95f68fe27389bd3','app_secret':'ATWmHpI8KePLpMoSmAxhBeX561ZHXyOt'})
TOKEN = r.json()['tenant_access_token']
DOC_ID = 'GZw2dw173oSTxYxekFecUC1mnPf'
headers = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json; charset=utf-8'}
BASE = f'https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_ID}/blocks/{DOC_ID}/children'

tests = {
    'heading2': {'block_type':4, 'heading2': {'elements':[{'text_run':{'content':'test heading'}}]}},
    'bullet': {'block_type':12, 'bullet': {'elements':[{'text_run':{'content':'test bullet'}}]}},
    'ordered': {'block_type':13, 'ordered': {'elements':[{'text_run':{'content':'test ordered'}}]}},
    'divider': {'block_type':21},
    'code': {'block_type':14, 'code': {'elements':[{'text_run':{'content':'print(1)'}}], 'style':{'language':1,'wrap':True}}},
    'callout': {'block_type':17, 'callout': {'emoji':'💡','background_color':1,'border_color':1,'children':[{'block_type':2,'text':{'elements':[{'text_run':{'content':'test callout'}}]}}]}},
    'quote': {'block_type':15, 'quote_container': {'children':[{'block_type':2,'text':{'elements':[{'text_run':{'content':'test quote'}}]}}]}},
    'bold_text': {'block_type':2, 'text': {'elements':[{'text_run':{'content':'bold text','text_element_style':{'bold':True}}}]}},
    'inline_code': {'block_type':2, 'text': {'elements':[{'text_run':{'content':'inline code','text_element_style':{'inline_code':True}}}]}},
    'link_text': {'block_type':2, 'text': {'elements':[{'text_run':{'content':'click me','text_element_style':{'link':{'url':'https://example.com'}}}}]}},
}

for name, block in tests.items():
    r = requests.post(BASE, headers=headers, json={'children':[block]})
    result = r.json()
    if result.get('code') == 0:
        print(f'{name}: OK')
    else:
        print(f'{name}: FAIL - {result.get("msg","?")}')
        print(f'  Detail: {json.dumps(result, ensure_ascii=False)[:500]}')
