#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试修复后的块类型"""
import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

r = requests.post('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
    json={'app_id':'cli_a95f68fe27389bd3','app_secret':'ATWmHpI8KePLpMoSmAxhBeX561ZHXyOt'})
TOKEN = r.json()['tenant_access_token']
DOC_ID = 'GZw2dw173oSTxYxekFecUC1mnPf'
headers = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json; charset=utf-8'}
BASE = f'https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_ID}/blocks/{DOC_ID}/children'

# divider 不能通过 children 创建，用空行替
# callout: 尝试不同格式
# quote: 尝试不同格式

tests = {
    'divider_empty': {'block_type': 2, 'text': {'elements': [{'text_run': {'content': '---'}}]}},
    'callout_simple': {
        'block_type': 17,
        'callout': {
            'emoji': '1f4a1',  # Unicode code point without U+
            'background_color': 1,
            'border_color': 1,
        }
    },
    'callout_no_emoji': {
        'block_type': 17,
        'callout': {
            'background_color': 1,
        }
    },
    'quote_simple': {
        'block_type': 15,
        'quote': {
            'elements': [{'text_run': {'content': 'test quote'}}]
        }
    },
    'quote_alt': {
        'block_type': 15,
        'quote_container': {
            'elements': [{'text_run': {'content': 'test quote 2'}}]
        }
    },
}

for name, block in tests.items():
    r = requests.post(BASE, headers=headers, json={'children':[block]})
    result = r.json()
    if result.get('code') == 0:
        print(f'{name}: OK - block_id={result["data"]["children"][0]["block_id"]}')
    else:
        print(f'{name}: FAIL - {result.get("msg","?")}')
        if 'error' in result:
            print(f'  helps: {result["error"].get("helps","")}')

# Now test callout with correct children for content
print("\n--- Testing callout with text children ---")
block = {
    'block_type': 17,
    'callout': {
        'background_color': 1,
    },
}
# Add text as children of callout
r = requests.post(BASE, headers=headers, json={'children':[block]})
result = r.json()
if result.get('code') == 0:
    print(f'callout_w_children: OK - block_id={result["data"]["children"][0]["block_id"]}')
    # Try adding text as child of this callout
    callout_id = result["data"]["children"][0]["block_id"]
    text_block = {'block_type': 2, 'text': {'elements': [{'text_run': {'content': 'Callout content here'}}]}}
    CHILD_BASE = f'https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_ID}/blocks/{callout_id}/children'
    r2 = requests.post(CHILD_BASE, headers=headers, json={'children':[text_block]})
    r2j = r2.json()
    if r2j.get('code') == 0:
        print(f'  + text child: OK')
    else:
        print(f'  + text child: FAIL - {r2j.get("msg","?")}')
else:
    print(f'callout_w_children: FAIL - {result.get("msg","?")}')
