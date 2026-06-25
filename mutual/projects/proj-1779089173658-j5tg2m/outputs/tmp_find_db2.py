import os
import datetime

# Search all drives for WeChat Files
drives = ['C:/', 'D:/', 'E:/', 'F:/']
for drive in drives:
    if not os.path.exists(drive):
        continue
    for root, dirs, files in os.walk(drive):
        if 'WeChat Files' in root:
            print('Found WeChat path:', root)
            for sub_root, sub_dirs, sub_files in os.walk(root):
                for f in sub_files:
                    if 'Msg' in f and f.endswith('.db'):
                        fp = os.path.join(sub_root, f)
                        try:
                            size = os.path.getsize(fp)
                            mt = datetime.datetime.fromtimestamp(os.path.getmtime(fp)).strftime('%Y-%m-%d %H:%M')
                            print('  %s  %.1fMB  %s' % (mt, size/1024/1024, fp))
                        except:
                            pass
                # Only go 3 levels deep from WeChat Files
                depth = sub_root.count(os.sep) - root.count(os.sep)
                if depth > 3:
                    sub_dirs.clear()
        # Limit depth
        depth = root.count(os.sep)
        if depth > 4:
            dirs.clear()
