import os
import re

dirs_to_check = ['docs', 'cheatsheet', 'README.md', 'src']
changed_files = 0

commands_no_args = [
    'hide', 'show', 'goto_mouse_pointer', 'pen_down', 'pen_up', 
    'erase_all', 'clear', 'delete_this_clone', 'stop_all_sounds',
    'next_costume', 'next_backdrop'
]

known_blocks = [
    'say', 'think', 'set_x', 'set_y', 'change_x', 'change_y', 'ask',
    'go_to', 'goto', 'turn_left', 'turn_right', 'point_in_direction',
    'move', 'set_size', 'change_size', 'play_sound', 'start_sound',
    'set_volume', 'change_volume', 'wait', 'wait_until', 'stop',
    'broadcast', 'broadcast_and_wait', 'go_forward', 'go_backward',
    'go_to_front', 'go_to_back', 'set_drag_mode', 'set_rotation_style',
    'set_pen_color', 'set_pen_size', 'change_pen_size', 'set_tempo', 'change_tempo',
    'play_drum', 'rest', 'play_note', 'set_instrument', 'switch_costume', 'switch_backdrop'
]

def process_code(code):
    for cmd in commands_no_args:
        code = re.sub(rf'\b{cmd}\s*;', rf'{cmd}();', code)
        
    code = re.sub(r'\badd\s+(.*?)\s+to\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*;', r'add(\1, \2);', code)
    code = re.sub(r'\binsert\s+(.*?)\s+at\s+([a-zA-Z_][a-zA-Z0-9_]*)\[(.*?)\]\s*;', r'insert(\1, \2, \3);', code)
    code = re.sub(r'\bdelete\s+([a-zA-Z_][a-zA-Z0-9_]*)\[(.*?)\]\s*;', r'delete(\1[\2]);', code)
    code = re.sub(r'\bdelete\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*;', r'delete(\1);', code)
    
    for cmd in known_blocks:
        code = re.sub(rf'\b{cmd}\s+([^;\(\n]+?)\s*;', rf'{cmd}(\1);', code)
        
    return code

def process_file(path):
    global changed_files
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    orig = content
    
    if path.endswith('.gs'):
        content = process_code(content)
    else:
        def process_code_block(m):
            return '```' + m.group(1) + '\n' + process_code(m.group(2)) + '```'
            
        content = re.sub(r'```([a-zA-Z]*)\n(.*?)```', process_code_block, content, flags=re.DOTALL)
        
        def process_inline_code(m):
            return '`' + process_code(m.group(1)) + '`'
            
        content = re.sub(r'`([^`\n]+)`', process_inline_code, content)
    
    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        changed_files += 1
        print(f"Updated {path}")

for d in dirs_to_check:
    if os.path.isfile(d):
        process_file(d)
        continue
    for root, dirs, files in os.walk(d):
        if 'node_modules' in dirs: dirs.remove('node_modules')
        if 'target' in dirs: dirs.remove('target')
        for file in files:
            if file.endswith('.md') or file.endswith('.gs'):
                process_file(os.path.join(root, file))
                
print(f"Done. Changed {changed_files} files.")
