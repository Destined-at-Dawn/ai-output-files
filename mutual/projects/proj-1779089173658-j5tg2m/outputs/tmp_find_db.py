import os
import datetime

search_roots = [r'C:\Users\13975', 'D:/', 'E:/']
for root_path in search_roots:
    if not os.path.exists(root_path):
        continue
    for subdir in ['Documents', 'AppData', 'WeChatData']:
        p = os.path.join(root_path, subdir, 'WeChat Files')
        if os.path.exists(p):
            print('Found:', p)
            for wxid in os.listdir(p):
                wxid_path = os.path.join(p, wxid)
                if not os.path.isdir(wxid_path):
                    continue
                msg_dir = os.path.join(wxid_path, 'Msg')
                multi_dir = os.path.join(wxid_path, 'Msg', 'Multi')
                if os.path.exists(multi_dir):
                    for f in os.listdir(multi_dir):
                        fp = os.path.join(multi_dir, f)
                        if 'Msg' in f and f.endswith('.db'):
                            size = os.path.getsize(fp)
                            mt = datetime.datetime.fromtimestamp(os.path.getmtime(fp)).strftime('%Y-%m-%d %H:%M')
                            print('  %s  %.1fMB  %s' % (mt, size/1024/1024, fp))
                if os.path.exists(msg_dir):
                    for f in os.listdir(msg_dir):
                        fp = os.path.join(msg_dir, f)
                        if 'Msg' in f and f.endswith('.db') and 'fts' not in f and 'multi' not in f.lower():
                            size = os.path.getsize(fp)
                            mt = datetime.datetime.fromtimestamp(os.path.getmtime(fp)).strftime('%Y-%m-%d %H:%M')
                            print('  %s  %.1fMB  %s' % (mt, size/1024/1024, fp))
