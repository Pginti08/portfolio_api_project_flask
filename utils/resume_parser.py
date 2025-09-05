import re
from PyPDF2 import PdfReader

def parse_resume(resume_file):
    # Extract text from PDF pages
    text = ""
    reader = PdfReader(resume_file)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    # Remove extra spaces and normalize spacing
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\r+', '\n', text)
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    data = {
        "name": "",
        "bio": "",
        "skills": [],
        "experience": [],
        "education": [],
        "projects": [],
        "contact": ""
    }

    # Name (Assume first line is the name)
    for idx, line in enumerate(lines):
        if re.match(r"^[A-Za-z ]{4,}$", line):
            data["name"] = line
            break

    # Contact Info
    for line in lines:
        if re.search(r"\b\d{10}\b", line):  # Indian phone
            data.setdefault("phone", re.search(r"\b\d{10}\b", line).group())
            data["contact"] += line + " "
        if re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", line):
            data.setdefault("email", re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", line).group())
            data["contact"] += line + " "

    # Bio/About
    for i, line in enumerate(lines):
        if line.startswith("Fullstack Software Developer") or line.startswith("I am a Full Stack Developer"):
            bio_lines = []
            bio_lines.append(line)
            # grab next lines that look like description
            for j in range(i+1, min(i+8, len(lines))):
                if lines[j].startswith("SKILLS") or lines[j].startswith("CERTIFICATION"):
                    break
                bio_lines.append(lines[j])
            data["bio"] = " ".join(bio_lines)
            break

    # Skills
    for i, line in enumerate(lines):
        if "SKILLS" in line:
            skills = []
            for j in range(i+1, len(lines)):
                if lines[j].startswith("CERTIFICATION") or lines[j].startswith("WORK EXPERIENCE"):
                    break
                skills += [s.strip() for s in lines[j].split() if len(s.strip()) > 1]
            data["skills"] = skills
            break

    # Experience
    exp_section = False
    exp_items = []
    for line in lines:
        if "WORK EXPERIENCE" in line or "Responsibilities:" in line:
            exp_section = True
            continue
        if exp_section:
            if "INTERNSHIPS" in line or "PROJECTS" in line:
                exp_section = False
                break
            if line and len(line.split()) > 3:
                exp_items.append(line)
    if exp_items:
        data["experience"].append({
            "role": "Fullstack Software Developer",
            "company": "Vyzion Innovation",
            "desc": " ".join(exp_items)
        })

    # Projects
    proj_section = False
    curr_proj = {}
    for i, line in enumerate(lines):
        if "PROJECTS" in line:
            proj_section = True
            continue
        if proj_section and line.startswith("VRR"):
            curr_proj = {"title": "VRR Towing & Parking App", "desc": ""}
            for j in range(i, len(lines)):
                if lines[j].startswith("AI Chatbot System"):
                    data["projects"].append(curr_proj)
                    break
                curr_proj["desc"] += lines[j] + " "
        if proj_section and line.startswith("AI Chatbot System"):
            curr_proj = {"title": "AI Chatbot System", "desc": ""}
            for j in range(i, len(lines)):
                if lines[j].startswith("Sales Management System"):
                    data["projects"].append(curr_proj)
                    break
                curr_proj["desc"] += lines[j] + " "
        if proj_section and line.startswith("Sales Management System"):
            curr_proj = {"title": "Sales Management System", "desc": ""}
            for j in range(i, len(lines)):
                if lines[j].startswith("Study Gram"):
                    data["projects"].append(curr_proj)
                    break
                curr_proj["desc"] += lines[j] + " "
        if proj_section and line.startswith("Study Gram"):
            curr_proj = {"title": "Study Gram", "desc": ""}
            for j in range(i, len(lines)):
                if lines[j].startswith("EDUCATION"):
                    data["projects"].append(curr_proj)
                    break
                curr_proj["desc"] += lines[j] + " "

    # Education
    for i, line in enumerate(lines):
        if "EDUCATION" in line:
            for j in range(i+1, len(lines)):
                if lines[j].startswith("ADDITIONAL INFORMATION"):
                    break
                if "MCA" in lines[j]:
                    data["education"].append({
                        "degree": "MCA",
                        "institution": "Uttaranchal University",
                        "location": "Dehradun"
                    })

    # Fallback for empty fields
    for k in data:
        if not data[k]:
            data[k] = "" if isinstance(data[k], str) else []

    return data
