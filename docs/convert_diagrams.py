import re
import os

filepath = r"c:\Users\ASUS\savannakhet-project\docs\SEQUENCE_DIAGRAMS_ALL.md"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Split into blocks of text inside ```text and ```
def process_mermaid_block(match):
    block = match.group(1)
    
    lines = block.strip().split('\n')
    new_lines = ["sequenceDiagram", "    autonumber"]
    
    participants = []
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            new_lines.append("")
            continue
            
        if line_stripped.startswith("title "):
            new_lines.append(f"    %% {line_stripped}")
            continue
            
        if line_stripped.startswith("actor "):
            name = line_stripped[6:].strip()
            participants.append(name)
            new_lines.append(f'    actor "{name}"')
            continue
            
        if line_stripped.startswith("participant "):
            name = line_stripped[12:].strip()
            participants.append(name)
            new_lines.append(f'    participant "{name}"')
            continue
            
        if line_stripped.startswith("activate "):
            name = line_stripped[9:].strip()
            new_lines.append(f'    activate "{name}"')
            continue
            
        if line_stripped.startswith("deactivate "):
            name = line_stripped[11:].strip()
            new_lines.append(f'    deactivate "{name}"')
            continue
            
        # Message matching: A->B: msg or A-->B: msg
        # Note: sequencediagram.org might use -> for everything.
        m = re.match(r'^(.*?)(->|-->)(.*?):(.*)$', line_stripped)
        if m:
            sender = m.group(1).strip()
            arrow = m.group(2)
            receiver = m.group(3).strip()
            msg = m.group(4).strip()
            
            # replace newlines \n with <br/> for mermaid
            msg = msg.replace("\\n", "<br/>")
            
            mermaid_arrow = "->>" if arrow == "->" else "-->>"
            new_lines.append(f'    "{sender}"{mermaid_arrow}"{receiver}": {msg}')
            continue
            
        # Fallback
        new_lines.append(f'    {line_stripped}')

    return "```mermaid\n" + "\n".join(new_lines) + "\n```"

# Replace all ```text ... ``` blocks
new_content = re.sub(r'```text\s*(.*?)\s*```', process_mermaid_block, content, flags=re.DOTALL)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Conversion complete.")
