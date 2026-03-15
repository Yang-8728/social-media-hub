with open('containers/api-gateway/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 修改import行
for i, line in enumerate(lines):
    if line.startswith('from flask import Flask, jsonify, request'):
        lines[i] = 'from flask import Flask, jsonify, request, render_template\n'
    elif line.strip() == 'app = Flask(__name__)':
        lines[i] = 'app = Flask(__name__, \n            template_folder=''templates'',\n            static_folder=''static'')\n'
    elif '"""API Gateway主页"""' in line:
        # 找到home函数，替换整个函数
        j = i + 1
        while j < len(lines) and not lines[j].strip().startswith('@app.route'):
            j += 1
        lines[i:j] = ['    """Web管理界面"""\n', '    return render_template(''index.html'')\n', '\n']

with open('containers/api-gateway/app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('File updated')
