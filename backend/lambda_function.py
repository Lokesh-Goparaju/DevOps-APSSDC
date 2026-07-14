import json
import base64
import io
import re
from PyPDF2 import PdfReader

# Skills list
SKILLS = [

    # Programming Languages
    "python", "java", "c", "c++", "c#", "javascript", "typescript",
    "php", "ruby", "go", "rust", "kotlin", "swift", "scala", "r",

    # Web Technologies
    "html", "css", "bootstrap", "tailwind", "jquery", "ajax",

    # Frontend Frameworks
    "react", "angular", "vue", "nextjs", "nuxt", "svelte",

    # Backend Frameworks
    "node", "express", "spring", "springboot", "django",
    "flask", "fastapi", "laravel", "asp.net",

    # Mobile Development
    "android", "ios", "flutter", "react native", "xamarin",

    # Databases
    "sql", "mysql", "postgresql", "mongodb", "oracle",
    "sqlite", "redis", "firebase", "dynamodb", "cassandra",

    # Cloud Platforms
    "aws", "azure", "gcp", "amazon web services",

    # AWS Services
    "ec2", "s3", "lambda", "api gateway", "iam",
    "cloudwatch", "cloudformation", "elastic beanstalk",
    "ecs", "eks", "efs", "rds", "route53", "vpc",
    "sns", "sqs", "ses", "cloudfront",

    # DevOps
    "docker", "kubernetes", "terraform", "ansible",
    "jenkins", "gitlab ci", "github actions",
    "ci/cd", "devops",

    # Version Control
    "git", "github", "bitbucket",

    # Operating Systems
    "linux", "ubuntu", "windows", "unix",

    # Networking
    "tcp/ip", "dns", "http", "https", "ftp", "ssh",

    # AI / ML
    "machine learning", "deep learning", "tensorflow",
    "keras", "pytorch", "opencv", "nlp",
    "computer vision", "llm", "generative ai",

    # Data Science
    "numpy", "pandas", "matplotlib", "seaborn",
    "scikit-learn", "power bi", "tableau",

    # Testing
    "selenium", "junit", "pytest", "postman",

    # API
    "rest api", "graphql", "soap",

    # Security
    "cyber security", "oauth", "jwt", "ssl", "tls",

    # Tools
    "visual studio", "vscode", "intellij", "eclipse",
    "docker desktop", "postman", "jira",

    # Soft Skills
    "communication",
    "leadership",
    "teamwork",
    "problem solving",
    "critical thinking",
    "time management",
    "adaptability",
    "creativity",
    "analytical skills",
    "decision making",
    "collaboration",
    "presentation",
    "public speaking",
    "project management",
    "conflict resolution",
    "negotiation",
    "mentoring",
    "attention to detail",
    "organizational skills",
    "self motivated",
    "quick learner",
    "work ethic",
    "multitasking",
    "customer service",
    "emotional intelligence"
]
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9+# ]', ' ', text)
    return text

def extract_pdf_text(pdf_base64):
    pdf_bytes = base64.b64decode(pdf_base64)

    pdf_stream = io.BytesIO(pdf_bytes)

    reader = PdfReader(pdf_stream)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + " "

    return text

def lambda_handler(event, context):

    try:

        body = json.loads(event["body"])

        pdf_base64 = body["resume"]

        jd = body["jd"]

        resume = extract_pdf_text(pdf_base64)

        resume = clean_text(resume)

        jd = clean_text(jd)

        resume_skills = []

        jd_skills = []

        for skill in SKILLS:

            if skill in resume:
                resume_skills.append(skill)

            if skill in jd:
                jd_skills.append(skill)

        matched = sorted(list(set(resume_skills) & set(jd_skills)))

        missing = sorted(list(set(jd_skills) - set(resume_skills)))

        if len(jd_skills) == 0:
            score = 0
        else:
            score = round((len(matched) / len(jd_skills)) * 100)

        suggestions = []

        for skill in missing:
            suggestions.append(f"Add {skill} experience to improve ATS score.")

        result = {
            "score": score,
            "matched": matched,
            "missing": missing,
            "resumeSkills": resume_skills,
            "requiredSkills": jd_skills,
            "suggestions": suggestions,
            "statistics": {
                "matchedCount": len(matched),
                "missingCount": len(missing),
                "resumeSkillCount": len(resume_skills),
                "requiredSkillCount": len(jd_skills)
            }
        }

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "POST"
            },
            "body": json.dumps(result)
        }

    except Exception as e:

        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "error": str(e)
            })
        }
