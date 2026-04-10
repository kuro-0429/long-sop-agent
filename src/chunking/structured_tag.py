# src/chunking/structured_tag.py
import re

def split_techniques(filepath: str) -> list[dict]:
    """按 ### 【T-XX】 切分技法库"""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # 按三级标题切分
    sections = re.split(r'\n(?=### 【T-)', text)

    chunks = []
    for section in sections:
        section = section.strip()
        if not section.startswith("### 【T-"):
            continue  # 跳过文件头部说明

        # 提取 ID 和标题
        first_line = section.split('\n')[0]
        match = re.match(r'### 【(T-\d+)】(.+)', first_line)
        if not match:
            continue

        tech_id = match.group(1)       # "T-01"
        tech_name = match.group(2).strip()  # "文字遮罩揭示（Text Clip Reveal）"

        chunks.append({
            "id": tech_id,
            "title": f"{tech_id} {tech_name}",
            "content": section,
            "source": "generator_techniques",
        })

    return chunks

def split_by_h2(filepath: str, source_name: str) -> list[dict]:
    """按 ## 标题切分，适用于 rules.md 和 generator_flow.md"""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    sections = re.split(r'\n(?=## )', text)
    chunks = []
    for i, section in enumerate(sections):
        section = section.strip()
        if not section:
            continue
        first_line = section.split('\n')[0]
        title = first_line.replace('## ', '').strip()
        chunks.append({
            "id": f"{source_name}-{i:03d}",
            "title": title,
            "content": section,
            "source": source_name,
        })
    return chunks

if __name__ == "__main__":
    chunks = split_techniques("configs/prompt_templates/generator_techniques.md")
    print(f"共切出 {len(chunks)} 个技法 chunk")
    print(f"第一个：{chunks[0]['title']}")
    print(f"最后一个：{chunks[-1]['title']}")
