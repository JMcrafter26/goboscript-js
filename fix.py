import re

with open('src/parser.rs', 'r', encoding='utf-8') as file:
    content = file.read()

new_content = re.sub(r'\"say (.*?);\"', r'\"say(\1);\"', content)
new_content = string = new_content.replace('\"hide;\"', '\"hide();\"')
new_content = new_content.replace('\"show;\"', '\"show();\"')
new_content = re.sub(r'\"add (.*?) to (.*?);\"', r'\"add(\1, \2);\"', new_content)
new_content = re.sub(r'\"insert (.*?) at (.*?)\[(.*?)\];\"', r'\"insert(\1, \2, \3);\"', new_content)
new_content = re.sub(r'\"delete (.*?);\"', r'\"delete(\1);\"', new_content)
new_content = re.sub(r'\"delete (.*?)\[(.*?)\];\"', r'\"delete(\1[\2]);\"', new_content)

new_content = re.sub(r'\"move (.*?);\"', r'\"move(\1);\"', new_content)
new_content = re.sub(r'\"turn_right (.*?);\"', r'\"turn_right(\1);\"', new_content)

if content != new_content:
    with open('src/parser.rs', 'w', encoding='utf-8') as file:
        file.write(new_content)
    print('Updated src/parser.rs')
else:
    print('No changes needed in src/parser.rs')
