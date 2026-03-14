
import streamlit as st
import requests
import socket
import re
import os
import networkx as nx
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime
from groq import Groq

st.set_page_config(page_title="CyberShield OSINT", layout="wide", page_icon="🛡️")
st.title("🛡️ CyberShield OSINT Intelligence Platform")

# =========================
# DOMAIN INTELLIGENCE
# =========================
def domain_info(domain):
    try:
        r = requests.get(f"https://rdap.org/domain/{domain}", timeout=10)
        if r.status_code == 200:
            data = r.json()
            return {
                "domain": data.get("ldhName"),
                "status": data.get("status"),
                "events": data.get("events")
            }
    except:
        pass
    return {"error":"lookup failed"}

# =========================
# DNS RECORDS
# =========================
def dns_lookup(domain):
    records = {}
    try:
        records["ip"] = socket.gethostbyname(domain)
    except:
        records["ip"] = "unknown"
    return records

# =========================
# WEBSITE ANALYSIS
# =========================
def detect_tech(url):
    tech = []
    try:
        r = requests.get(url, timeout=8)
        text = r.text.lower()
        if "wordpress" in text:
            tech.append("WordPress")
        if "react" in text:
            tech.append("React")
        if "jquery" in text:
            tech.append("jQuery")
        if "django" in text:
            tech.append("Django")
    except:
        pass
    return list(set(tech))

# =========================
# HEADER SECURITY CHECK
# =========================
def header_analysis(url):
    try:
        r = requests.get(url, timeout=8)
        h = r.headers
        return {
            "CSP": h.get("Content-Security-Policy","Missing"),
            "X-Frame": h.get("X-Frame-Options","Missing"),
            "X-Content": h.get("X-Content-Type-Options","Missing"),
            "HSTS": h.get("Strict-Transport-Security","Missing")
        }
    except Exception as e:
        return {"error":str(e)}

# =========================
# EMAIL EXTRACTION
# =========================
def extract_emails(url):
    try:
        r = requests.get(url, timeout=8)
        emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", r.text)
        return list(set(emails))
    except:
        return []

# =========================
# SUBDOMAIN SCAN
# =========================
def subdomain_scan(domain):
    subs = ["www","mail","dev","test","api","portal","beta"]
    found = {}
    for s in subs:
        host = f"{s}.{domain}"
        try:
            ip = socket.gethostbyname(host)
            found[host] = ip
        except:
            pass
    return found

# =========================
# USERNAME OSINT
# =========================
def username_search(username):
    sites = {
        "GitHub": f"https://github.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "Pinterest": f"https://www.pinterest.com/{username}",
        "Medium": f"https://medium.com/@{username}"
    }
    found = {}
    for site,url in sites.items():
        try:
            r = requests.get(url)
            if r.status_code == 200:
                found[site] = url
        except:
            pass
    return found

# =========================
# GEOIP LOOKUP
# =========================
def geoip(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}")
        return r.json()
    except:
        return {}

# =========================
# ATTACK SURFACE GRAPH
# =========================
def draw_graph(domain, subs):
    G = nx.Graph()
    G.add_node(domain)
    for s in subs:
        G.add_edge(domain,s)
    plt.figure(figsize=(8,8))
    nx.draw(G,with_labels=True)
    file="surface.png"
    plt.savefig(file)
    return file

# =========================
# AI SECURITY ANALYST
# =========================
def ai_analysis(data):
    key = os.getenv("GROQ_API_KEY")
    if not key:
        return "Add GROQ_API_KEY environment variable"
    client = Groq(api_key=key)
    prompt=f"""
Analyze this OSINT data:

{data}

Give security insights and infrastructure analysis.
"""
    res=client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role":"system","content":"You are a cybersecurity analyst"},
            {"role":"user","content":prompt}
        ]
    )
    return res.choices[0].message.content

# =========================
# PDF REPORT
# =========================
def generate_report(data):
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font("Arial","B",16)
    pdf.cell(0,10,"CyberShield OSINT Report",ln=True)
    pdf.set_font("Arial","",12)
    pdf.cell(0,10,str(datetime.now()),ln=True)
    pdf.ln(5)
    for k,v in data.items():
        pdf.cell(0,8,str(k),ln=True)
        pdf.multi_cell(0,6,str(v))
    file="report.pdf"
    pdf.output(file)
    return file

tabs = st.tabs([
    "Domain Intelligence",
    "Website Analysis",
    "Subdomain Discovery",
    "Username OSINT",
    "GeoIP",
    "Attack Surface",
    "AI Analyst",
    "Reports"
])

with tabs[0]:
    domain = st.text_input("Domain")
    if st.button("Analyze Domain"):
        info = domain_info(domain)
        dns = dns_lookup(domain)
        st.write(info)
        st.write(dns)
        st.session_state["domain"]=info

with tabs[1]:
    url = st.text_input("Target URL")
    if st.button("Scan Website"):
        tech=detect_tech(url)
        headers=header_analysis(url)
        emails=extract_emails(url)
        result={"tech":tech,"headers":headers,"emails":emails}
        st.write(result)
        st.session_state["scan"]=result

with tabs[2]:
    domain = st.text_input("Domain for subdomain scan")
    if st.button("Scan Subdomains"):
        subs=subdomain_scan(domain)
        st.write(subs)
        st.session_state["subs"]=subs

with tabs[3]:
    username=st.text_input("Username")
    if st.button("Search Username"):
        result=username_search(username)
        st.write(result)
        st.session_state["user"]=result

with tabs[4]:
    ip=st.text_input("IP Address")
    if st.button("Lookup IP"):
        data=geoip(ip)
        st.write(data)
        st.session_state["geo"]=data

with tabs[5]:
    if "subs" in st.session_state:
        file=draw_graph(
            list(st.session_state["subs"].keys())[0].split(".",1)[1],
            st.session_state["subs"]
        )
        st.image(file)
    else:
        st.warning("Run subdomain scan first")

with tabs[6]:
    if st.button("Run AI Analysis"):
        data=str(st.session_state)
        result=ai_analysis(data)
        st.write(result)

with tabs[7]:
    if st.button("Generate PDF"):
        file=generate_report(st.session_state)
        with open(file,"rb") as f:
            st.download_button("Download Report", f, file_name=file)
