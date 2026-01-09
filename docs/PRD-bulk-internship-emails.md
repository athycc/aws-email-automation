# Product Requirements Document (PRD)
## Bulk Internship Inquiry Email System

---

### Document Information
| Field | Value |
|-------|-------|
| **Project Name** | Bulk Internship Inquiry Email System |
| **Version** | 1.0 |
| **Date** | January 9, 2026 |
| **Status** | Draft |

---

## 1. Overview

### 1.1 Purpose
This document outlines the requirements for implementing a bulk email feature to send internship inquiry emails to multiple companies using the AWS Learning Club Alpha email automation system.

### 1.2 Background
AWS Learning Club Alpha at Rizal Technological University needs to reach out to multiple companies to inquire about internship/OJT opportunities for third-year IT students. The current system supports bulk email sending but requires modifications to:
- Support reading email addresses from `emails.txt` (plain text format)
- Use the `internship-inquiry.html` template
- Dynamically personalize company names in emails

---

## 2. Objectives

| Objective | Description |
|-----------|-------------|
| **Primary** | Enable bulk sending of internship inquiry emails to companies listed in `emails.txt` |
| **Secondary** | Support dynamic company name personalization in the template |
| **Tertiary** | Maintain logging and tracking of sent emails |

---

## 3. Scope

### 3.1 In Scope
- Reading recipient emails from `emails.txt` file
- Sending emails using the `internship-inquiry.html` template
- Basic error handling and send status logging
- Rate limiting to avoid spam filters

### 3.2 Out of Scope
- Email open/click tracking
- Automated follow-up emails
- CRM integration
- Bounce handling automation

---

## 4. Current State Analysis

### 4.1 Existing Assets

**Template File:** `template/internship-inquiry.html`
- Professional HTML email template
- Contains AWS LC Alpha branding (Banner.png, Footer.png)
- Currently hardcoded with "Accenture" as company name
- Includes internship details:
  - Start Date: January 13, 2026
  - End Date: May 2026
  - Required Hours: 300 hours
  - Contact: Dr. Lea Nisperos (Director of Computer Studies)

**Email List:** `emails.txt`
```
emmanuelfabella606@gmail.com
ramchrist20@gmail.com
notadocath@gmail.com
awslc.alpha@gmail.com
```

**Existing Email Sender:** `email_sender.py`
- Uses Gmail SMTP (smtp.gmail.com:465)
- Reads credentials from `.env` file
- Currently reads from CSV format (not TXT)
- Sends HTML emails via MIMEMultipart

### 4.2 Required Modifications

| Component | Current State | Required State |
|-----------|---------------|----------------|
| Email Source | CSV file (`contact.csv`) | TXT file (`emails.txt`) |
| Template | Hardcoded company name | Dynamic `{{company_name}}` placeholder |
| Subject Line | Generic | Customized for internship inquiries |

---

## 5. Functional Requirements

### FR-01: Email List Reader
| Requirement | Details |
|-------------|---------|
| **ID** | FR-01 |
| **Description** | System shall read email addresses from `emails.txt` |
| **Input** | Plain text file with one email per line |
| **Output** | List of valid email addresses |
| **Validation** | Skip empty lines and invalid email formats |

### FR-02: Template Processing
| Requirement | Details |
|-------------|---------|
| **ID** | FR-02 |
| **Description** | System shall use `internship-inquiry.html` as the email template |
| **Placeholders** | Support `{{company_name}}` placeholder (optional for MVP) |
| **Fallback** | Use generic "your company" if no company name provided |

### FR-03: Email Sending
| Requirement | Details |
|-------------|---------|
| **ID** | FR-03 |
| **Description** | System shall send HTML emails via Gmail SMTP |
| **Subject** | "Inquiry on Internship Opportunities – AWS Learning Club Alpha" |
| **From** | Configured via `EMAIL_ADDRESS` in `.env` |
| **Rate Limit** | 1-2 second delay between emails to avoid spam filters |

### FR-04: Logging
| Requirement | Details |
|-------------|---------|
| **ID** | FR-04 |
| **Description** | System shall log the status of each email sent |
| **Success** | Print confirmation with recipient email |
| **Failure** | Print error message with details |

---

## 6. Non-Functional Requirements

### NFR-01: Performance
- Process up to 50 emails per session
- Complete batch within 5 minutes

### NFR-02: Reliability
- Graceful error handling (continue on individual failures)
- No data loss on partial failures

### NFR-03: Security
- Credentials stored in `.env` file (not in code)
- `.env` file excluded from version control

---

## 7. Data Requirements

### 7.1 Input Files

**emails.txt Format:**
```
company1@example.com
company2@example.com
company3@example.com
```

**Optional: companies.csv Format (for personalization):**
```csv
email,company_name
hr@accenture.com,Accenture
careers@ibm.com,IBM Philippines
```

### 7.2 Configuration (.env)
```
EMAIL_ADDRESS=awslc.alpha@gmail.com
EMAIL_PASSWORD=your_app_password
```

---

## 8. User Interface

### 8.1 Command Line Interface
```bash
# Basic usage (simple email list)
python email_sender.py --template internship-inquiry.html --emails emails.txt

# With custom subject
python email_sender.py --template internship-inquiry.html --emails emails.txt --subject "Internship Inquiry"
```

### 8.2 Expected Output
```
Starting bulk email send...
Template: internship-inquiry.html
Recipients: 4
---
[1/4] Sending to emmanuelfabella606@gmail.com... Done
[2/4] Sending to ramchrist20@gmail.com... Done
[3/4] Sending to notadocath@gmail.com... Done
[4/4] Sending to awslc.alpha@gmail.com... Done
---
Summary: 4 sent, 0 failed
```

---

## 9. Test Plan

### 9.1 Test Recipients (from emails.txt)
| Email | Purpose |
|-------|---------|
| emmanuelfabella606@gmail.com | Team member test |
| ramchrist20@gmail.com | Team member test |
| notadocath@gmail.com | Founder verification |
| awslc.alpha@gmail.com | Official account test |

### 9.2 Test Cases

| TC-ID | Test Case | Expected Result |
|-------|-----------|-----------------|
| TC-01 | Send to valid email | Email delivered successfully |
| TC-02 | Send to all 4 test emails | All 4 emails delivered |
| TC-03 | Template renders correctly | HTML displays with Banner and Footer images |
| TC-04 | Invalid email in list | Skip invalid, continue with valid |
| TC-05 | Empty emails.txt | Graceful exit with message |

---

## 10. Implementation Approach

### Phase 1: MVP (Minimum Viable Product)
1. Modify `email_sender.py` to read from TXT file
2. Add function to send internship inquiry emails
3. Use existing template as-is (hardcoded content)
4. Test with `emails.txt` recipients

### Phase 2: Enhancements (Future)
1. Add `{{company_name}}` placeholder support
2. Create companies.csv for personalized emails
3. Add command-line arguments for flexibility
4. Implement detailed logging to file

---

## 11. Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Gmail rate limiting | Emails blocked | Medium | Add delays between sends |
| Spam folder delivery | Emails not seen | Medium | Use professional subject lines, proper HTML |
| Invalid emails causing errors | Script crashes | Low | Add email validation and error handling |
| Template images not loading | Poor presentation | Low | Images hosted on GitHub (already implemented) |

---

## 12. Success Metrics

| Metric | Target |
|--------|--------|
| Delivery Rate | 100% to test recipients |
| Error Rate | < 5% |
| Execution Time | < 30 seconds for 4 emails |

---

## 13. Appendix

### A. Current Template Preview
The `internship-inquiry.html` template includes:
- AWS Learning Club Alpha banner header
- Professional greeting and introduction
- Internship program details (Jan 13 - May 2026, 300 hours)
- Contact information (Dr. Lea Nisperos)
- MOA template offer
- Signature block (Catherine Notado, Founder)
- Branded footer with logo and contact email

### B. Email Subject Line Options
1. "Inquiry on Internship Opportunities – AWS Learning Club Alpha" (Recommended)
2. "RTU IT Student Internship Inquiry – AWS Learning Club Alpha"
3. "Partnership Inquiry: Internship Program for RTU IT Students"

---

**Document Approval**

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Project Owner | | | |
| Technical Lead | | | |
| Stakeholder | | | |
