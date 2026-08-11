def populate_seed_data(conn):
    """Insert initial seed data for government schemes and health camps into SQLite database."""
    cursor = conn.cursor()

    schemes = [
        (
            "PM Kisan Samman Nidhi",
            "Farmers",
            "18-60",
            "Direct income support of ₹6,000 per year in three equal installments to small and marginal farmer families across India.",
            "Financial support of ₹6,000/year transferred directly into bank accounts via DBT in 3 installments of ₹2,000 every 4 months.",
            "Small and marginal farmers holding cultivable land up to 2 hectares in their name.",
            "Aadhaar Card, Land ownership documents (Khatauni/Patta), Bank account linked with Aadhaar, Mobile Number.",
            "1. Visit pmkisan.gov.in\n2. Click on 'New Farmer Registration'\n3. Enter Aadhaar number and land details\n4. Submit and track status online.",
            "https://pmkisan.gov.in",
            "bi-person-badge-fill",
            1
        ),
        (
            "Ayushman Bharat (PM-JAY)",
            "Health",
            "All Ages",
            "World's largest health insurance scheme offering health cover of ₹5 Lakh per family per year for secondary and tertiary care hospitalization.",
            "Cashless & paperless treatment up to ₹5,000,000 per family per year in empanelled public and private hospitals across India.",
            "Families listed under SECC 2011 data, low-income households, unorganized sector workers, and rural vulnerable families.",
            "Aadhaar Card, Ration Card, Ayushman Golden Card (generated at kiosk/hospital).",
            "1. Visit nearest empanelled hospital or Common Service Center (CSC)\n2. Check eligibility using Mobile/Aadhaar\n3. Generate E-Card\n4. Avail cashless treatment.",
            "https://pmjay.gov.in",
            "bi-heart-pulse-fill",
            1
        ),
        (
            "Beti Bachao Beti Padhao",
            "Women",
            "0-18",
            "National initiative aimed at ensuring the survival, protection, and education of girl children with financial incentive schemes like Sukanya Samriddhi Yojana.",
            "Promotes girl child education, protects rights, and provides high interest rate savings accounts for future higher education/marriage.",
            "Girl children below 10 years of age (for linked savings account) residing in India.",
            "Birth Certificate of Girl Child, Parents' Aadhaar Card, Address Proof, Recent Passport Photos.",
            "1. Visit nearest Post Office or authorized Commercial Bank\n2. Fill Sukanya Samriddhi Account form\n3. Deposit minimum initial amount of ₹250.",
            "https://wcd.nic.in/bbbp-schemes",
            "bi-gender-female",
            1
        ),
        (
            "PM Vishwakarma Yojana",
            "Workers",
            "18-60",
            "Comprehensive support scheme for traditional artisans and craftspeople working with hands and tools.",
            "Skill training stipend ₹500/day, toolkit incentive ₹15,000, collateral-free credit support up to ₹3 Lakh at concessionary 5% interest rate.",
            "Artisans and craftspeople working in 18 traditional trades (weavers, carpenters, blacksmiths, potters, cobblers, goldsmiths, etc.).",
            "Aadhaar Card, Bank Account Details, Skill/Trade certificate, Mobile Number linked to Aadhaar.",
            "1. Visit nearest CSC Center or pmvishwakarma.gov.in\n2. Complete biometric verification\n3. Get certified and apply for loan/toolkit.",
            "https://pmvishwakarma.gov.in",
            "bi-tools",
            1
        ),
        (
            "National Overseas & Merit Scholarship",
            "Students",
            "18-40",
            "Financial assistance to low-income students belonging to SC/ST/OBC/EWS categories for pursuing master's and Ph.D. level studies.",
            "Full tuition fee coverage, living allowance of up to $15,000/year, airfare, and annual contingency allowance.",
            "Students securing admission in top foreign or domestic universities with family income below ₹8 Lakh per annum.",
            "Income Certificate, Marksheet/Degree Certificate, Offer Letter from University, Caste/Category Certificate, Passport.",
            "1. Register on NSP (scholarships.gov.in)\n2. Upload income and academic transcripts\n3. Institute verification & final disbursement.",
            "https://scholarships.gov.in",
            "bi-mortarboard-fill",
            1
        ),
        (
            "Indira Gandhi National Old Age Pension Scheme",
            "Senior Citizens",
            "60+",
            "Monthly pension support to senior citizens below poverty line (BPL) to ensure dignified living in old age.",
            "Monthly financial assistance of ₹1,000 to ₹3,000 depending on state top-ups directly deposited into bank accounts.",
            "Indian citizens aged 60 years or above belonging to Below Poverty Line (BPL) households.",
            "BPL Ration Card, Aadhaar Card, Age Proof, Bank Passbook copy, Passport size photos.",
            "1. Apply through local Gram Panchayat or Municipal Corporation office\n2. Submit BPL verification and bank details.",
            "https://nsap.nic.in",
            "bi-person-hearts",
            1
        )
    ]

    cursor.executemany('''
        INSERT INTO schemes (name, category, age_group, description, benefits, eligibility, documents, how_to_apply, official_link, icon, is_demo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', schemes)

    camps = [
        (
            "Mega Health & Multispecialty Camp",
            "Health Checkup",
            "Free general health consultations, ECG, blood pressure checkup, free distribution of essential medicines, and doctor advice.",
            "2026-08-25",
            "09:00 AM - 04:00 PM",
            "District Health Society & Rotary Club",
            "Andhra Pradesh",
            "Visakhapatnam",
            "Community Health Center Grounds, MVP Colony, Visakhapatnam",
            17.7386,
            83.3312,
            "All Ages",
            "+91 891 2345678",
            1
        ),
        (
            "Free Eye Checkup & Cataract Screening Camp",
            "Eye",
            "Comprehensive vision testing, free prescription glasses distribution, and zero-cost surgical referral for cataract patients.",
            "2026-08-28",
            "10:00 AM - 03:00 PM",
            "L.V. Prasad Eye Institute & PrajaConnect Foundation",
            "Andhra Pradesh",
            "Visakhapatnam",
            "Government Junior College Auditorium, Gajuwaka, Visakhapatnam",
            17.6901,
            83.2094,
            "All Ages",
            "+91 891 9876543",
            1
        ),
        (
            "Dental Hygiene & Oral Cancer Screening Camp",
            "Dental",
            "Free dental checkups, cleaning guidance, cavity filling vouchers, and early oral cancer screening.",
            "2026-09-02",
            "09:30 AM - 02:30 PM",
            "Government Dental College Alumni Association",
            "Andhra Pradesh",
            "Visakhapatnam",
            "Municipal Community Hall, Asilmetta, Visakhapatnam",
            17.7245,
            83.3087,
            "All Ages",
            "+91 891 5551234",
            1
        ),
        (
            "LifeSaver Voluntary Blood Donation Camp",
            "Blood Donation",
            "Voluntary blood donation drive organized in association with Indian Red Cross Society. Donor certificate and refreshment provided.",
            "2026-09-05",
            "08:30 AM - 01:30 PM",
            "Indian Red Cross Society & Youth Red Cross",
            "Andhra Pradesh",
            "Visakhapatnam",
            "Red Cross Blood Bank Center, Maharani Peta, Visakhapatnam",
            17.7112,
            83.3150,
            "18-60",
            "+91 891 4443322",
            1
        ),
        (
            "Diabetes & Hypertension Screening Camp",
            "Diabetes",
            "Free HbA1c testing, blood sugar screening, blood pressure monitoring, and nutritionist dietary counseling.",
            "2026-09-10",
            "08:00 AM - 12:00 PM",
            "NCD Cell, Department of Health & Family Welfare",
            "Andhra Pradesh",
            "Guntur",
            "Primary Health Centre, Brodipet, Guntur",
            16.3067,
            80.4365,
            "18-60",
            "+91 863 2221100",
            1
        )
    ]

    cursor.executemany('''
        INSERT INTO camps (name, camp_type, description, date, time, organizer, state, district, location, latitude, longitude, age_group, contact, is_demo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', camps)

    conn.commit()
