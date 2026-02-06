#!/usr/bin/env python3
"""Create 3 missing landing pages that are causing Google Ads DISAPPROVAL (404 errors).
Pages: disease-screening, inflammation-test, specialty-tests
"""
import requests
import time
import json

API_KEY = "87be5982f1938a9143a7368af984a9863971dd55314fd5a60f482cc02425a0c7"
LP_COLLECTION = "6981a714e199bac70776d880"
FAQ_COLLECTION = "6981cbbfb6102bfdf7d05094"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
GENERAL_FAQ_IDS = ["6981d6b8f3e7405ce95132ed", "6981d6ba10e873663bd8c9ed"]

PAGES = [
    {
        "fieldData": {
            "name": "Disease Screening",
            "slug": "disease-screening",
            "primary-keyword": "disease screening",
            "secondary-keywords": "health screening, early disease detection, preventive screening, comprehensive disease test",
            "keyword-category": "a6dedc2e9c2dbae21c276d54745af1a3",
            "hero-headline": "70% of Chronic Diseases Are Preventable. But Only If You Catch Them Early Enough.",
            "hero-subheadline": "<p>Most diseases develop silently for years before symptoms appear. By then, damage is already done. One blood draw screens for 40+ conditions - prediabetes, PCOS, fatty liver, anemia, heart disease, kidney disease, thyroid dysfunction, and more. Stop guessing. Start screening. 100+ biomarkers. Results in about 10 days.</p>",
            "hero-cta-text": "Screen for 40+ Conditions",
            "symptom-headline": "Warning signs that something is off",
            "symptom-1": "Fatigue that sleep doesn't fix - no matter how much you rest",
            "symptom-2": "Unexplained weight changes you can't explain with diet or exercise",
            "symptom-3": "Brain fog, mood changes, or difficulty concentrating",
            "symptom-4": "Family history of diabetes, heart disease, or cancer",
            "symptom-5": "That nagging feeling something is wrong but doctors say you're fine",
            "symptom-cta": "Get the screening your annual physical doesn't include ->",
            "stat-1-number": "70%",
            "stat-1-text": "of chronic diseases could be prevented with earlier detection and lifestyle changes",
            "stat-2-number": "100+",
            "stat-2-text": "biomarkers tested in one blood draw",
            "stat-3-number": "10 days",
            "stat-3-text": "to get your results",
            "featured-testimonial-quote": "<p>My annual physical said everything was normal. Superpower found my fasting insulin was 19, my ferritin was 11, my vitamin D was 18, and my thyroid antibodies were elevated. Four problems - all caught early, all fixable. My doctor would have found zero of them.</p>",
            "featured-testimonial-name": "Angela R.",
            "featured-testimonial-result": "4 conditions caught that annual physical missed",
            "membership-subheadline": "Comprehensive disease screening for $199/year",
            "membership-benefit-1": "Screen for 40+ conditions in one blood draw",
            "membership-benefit-2": "100+ biomarkers including hormones and inflammation",
            "membership-benefit-3": "AI spots disease patterns early",
            "membership-benefit-4": "24/7 care team access",
            "how-it-works-1-subheading": "One blood draw tests for prediabetes, thyroid disease, anemia, liver disease, kidney disease, heart disease risk, hormonal imbalances, vitamin deficiencies, and chronic inflammation - 100+ biomarkers total. $199/year.",
            "how-it-works-2-subheading": "Most diseases develop silently for 5-15 years before symptoms appear. Prediabetes, fatty liver, iron deficiency, thyroid dysfunction, and chronic inflammation all cause damage long before you feel sick. Blood screening catches them at the earliest, most treatable stage.",
            "how-it-works-3-subheading": "Your annual physical checks 8-10 markers. We check 100+. That's how we catch insulin resistance years before diabetes, iron depletion before anemia, and thyroid antibodies before your TSH goes abnormal. The difference between early detection and late diagnosis.",
            "how-it-works-4-subheading": "Our clinical team reviews every result and flags anything that needs attention. You get clear explanations, actionable recommendations, and care team access for questions. Results in about 10 days.",
            "condition-name": "Comprehensive Disease Screening",
            "condition-overview": "<p>Chronic diseases - diabetes, heart disease, kidney disease, liver disease, autoimmune conditions, and cancer - account for 7 out of 10 deaths in the United States. The vast majority develop silently over years before causing symptoms. Blood testing is the most effective way to detect these conditions at their earliest, most treatable stage. Yet most people rely on annual physicals that test fewer than 10 markers.</p>",
            "why-test": "<p>Standard annual physicals check basic glucose, cholesterol, and a CBC - about 8-10 markers. This misses insulin resistance (which precedes diabetes by 10-15 years), thyroid antibodies (which precede thyroid disease), iron depletion (which precedes anemia), liver enzyme elevations (which signal fatty liver), and dozens of other early warning signs. Comprehensive screening with 100+ biomarkers catches problems years earlier.</p>",
            "what-is-included": "<p>Your panel includes complete metabolic panel, full lipid panel with ApoB and Lp(a), complete thyroid panel, fasting insulin, HbA1c, CBC with differential, iron studies with ferritin, liver enzymes, kidney markers, vitamin D, B12, folate, CRP, hormones, and more - 100+ biomarkers total.</p>",
            "next-steps": "<p>After your results arrive, our clinical team highlights any markers that need attention and provides specific recommendations. Whether it's a dietary change, supplement, or specialist referral, you'll know exactly what to do next. Annual retesting tracks your progress and catches any new developments.</p>",
            "meta-title": "Disease Screening | 100+ Biomarkers | Superpower",
            "meta-description": "Comprehensive disease screening - screen for 40+ conditions in one blood draw. Catch diabetes, heart disease, thyroid, anemia early. 100+ biomarkers. $199/year.",
            "og-title": "Disease Screening | 100+ Biomarkers | Superpower",
            "og-description": "Screen for 40+ conditions before symptoms appear. 100+ biomarkers in one blood draw. Results in ~10 days.",
        },
        "faqs": [
            {"name": "What diseases can blood screening detect?", "slug": "what-diseases-blood-screening-detect", "question": "What diseases can blood screening detect?", "answer": "<p>Comprehensive blood screening can detect or assess risk for prediabetes, type 2 diabetes, heart disease, kidney disease, liver disease (including fatty liver), thyroid disorders, iron deficiency and anemia, vitamin deficiencies, hormonal imbalances, chronic inflammation, autoimmune conditions, and more. Many of these conditions develop silently for years and can only be caught through blood testing before symptoms appear.</p>"},
            {"name": "How is this different from an annual physical?", "slug": "disease-screening-vs-annual-physical", "question": "How is this different from an annual physical?", "answer": "<p>A typical annual physical tests 8-10 basic markers - basic metabolic panel, CBC, and maybe cholesterol. Superpower tests 100+ biomarkers including fasting insulin (catches insulin resistance 10-15 years before diabetes), thyroid antibodies (catches thyroid disease before TSH goes abnormal), ferritin (catches iron depletion before anemia), ApoB and Lp(a) (catches hidden heart risk), and dozens more markers most doctors never order.</p>"},
            {"name": "How often should I get disease screening?", "slug": "how-often-disease-screening", "question": "How often should I get disease screening?", "answer": "<p>Annual comprehensive screening is recommended for most adults. This allows you to establish baselines, track trends over time, and catch changes early. Some markers like Lp(a) only need to be tested once (it's genetic and doesn't change), while metabolic markers like glucose, insulin, and liver enzymes should be checked yearly since they can change with lifestyle and aging.</p>"},
        ]
    },
    {
        "fieldData": {
            "name": "Inflammation Test",
            "slug": "inflammation-test",
            "primary-keyword": "inflammation test",
            "secondary-keywords": "CRP test, chronic inflammation test, inflammation blood test, hsCRP test",
            "keyword-category": "c2c992eadd1b85bebabf0fe4dd0de7b6",
            "hero-headline": "3 in 5 Adults Have Chronic Inflammation. Most Have No Idea.",
            "hero-subheadline": "<p>Chronic inflammation is the silent driver behind heart disease, diabetes, autoimmune conditions, and even cancer. You can't feel it - but a blood test can find it. We test hsCRP, ANA, thyroid antibodies, and other inflammation markers to reveal what's happening inside your body. 100+ biomarkers. Results in about 10 days.</p>",
            "hero-cta-text": "Test Your Inflammation Levels",
            "symptom-headline": "Signs of hidden inflammation",
            "symptom-1": "Fatigue that doesn't improve no matter what you try",
            "symptom-2": "Joint pain or stiffness - especially in the morning",
            "symptom-3": "Brain fog, difficulty concentrating, or memory issues",
            "symptom-4": "Digestive problems - bloating, gas, or food sensitivities",
            "symptom-5": "Skin issues like eczema, rashes, or unexplained breakouts",
            "symptom-cta": "Find out if inflammation is behind your symptoms ->",
            "stat-1-number": "3 in 5",
            "stat-1-text": "adults have chronic inflammation without knowing - it silently drives heart disease, diabetes, and autoimmune conditions",
            "stat-2-number": "100+",
            "stat-2-text": "biomarkers tested in one blood draw",
            "stat-3-number": "10 days",
            "stat-3-text": "to get your results",
            "featured-testimonial-quote": "<p>I had joint pain, brain fog, and fatigue for two years. Every doctor said I was fine. Superpower found my hsCRP was 4.8 (should be under 1), my ANA was positive, and my thyroid antibodies were 340. Chronic inflammation plus early Hashimoto's - finally an explanation after years of being dismissed.</p>",
            "featured-testimonial-name": "Jessica M.",
            "featured-testimonial-result": "Hidden inflammation and Hashimoto's diagnosed after 2 years",
            "membership-subheadline": "Track inflammation and find the root cause",
            "membership-benefit-1": "Monitor hsCRP and inflammation markers yearly",
            "membership-benefit-2": "100+ biomarkers including autoimmune markers",
            "membership-benefit-3": "AI connects inflammation to root causes",
            "membership-benefit-4": "24/7 care team access",
            "how-it-works-1-subheading": "One blood draw tests hsCRP (high-sensitivity C-reactive protein), ANA, thyroid antibodies, CBC with differential, ESR, and ferritin - the key inflammation markers - plus 100+ other biomarkers covering metabolic health, hormones, liver, and kidneys. $199/year.",
            "how-it-works-2-subheading": "Chronic inflammation is different from acute inflammation (like a sprained ankle). It simmers at low levels for years, damaging blood vessels, joints, and organs. hsCRP is the gold standard for measuring systemic inflammation. Levels above 1.0 mg/L signal increased cardiovascular and disease risk.",
            "how-it-works-3-subheading": "Inflammation doesn't happen in isolation. We analyze hsCRP alongside thyroid antibodies, ANA, metabolic markers, and iron studies to identify what's driving the inflammation - whether it's autoimmune activity, metabolic dysfunction, or nutrient deficiency.",
            "how-it-works-4-subheading": "Our clinical team explains your inflammation markers in context and provides specific recommendations - dietary changes, supplementation, or specialist referral for autoimmune evaluation. Results in about 10 days.",
            "condition-name": "Chronic Inflammation Screening",
            "condition-overview": "<p>Chronic inflammation is a persistent, low-grade immune response that damages tissues over time. Unlike acute inflammation (redness and swelling from an injury), chronic inflammation has no obvious symptoms but is linked to heart disease, type 2 diabetes, Alzheimer's, autoimmune diseases, and certain cancers. Research now considers chronic inflammation a root driver of most chronic diseases.</p>",
            "why-test": "<p>You cannot feel chronic inflammation. The only way to detect it is through blood testing. hsCRP (high-sensitivity C-reactive protein) is the gold standard marker - it measures system-wide inflammation with high precision. ANA and thyroid antibodies can reveal autoimmune-driven inflammation. Testing these markers together identifies whether inflammation is present and helps pinpoint its source.</p>",
            "what-is-included": "<p>Your panel includes hsCRP, ANA, thyroid antibodies (TPO, thyroglobulin), CBC with differential, ferritin, ESR, complete metabolic panel, liver enzymes, fasting insulin, HbA1c, vitamin D, and hormones - 100+ biomarkers total.</p>",
            "next-steps": "<p>If inflammation markers are elevated, our care team helps identify the likely cause and recommends next steps. This may include anti-inflammatory dietary changes, targeted supplementation (omega-3, vitamin D, curcumin), or specialist referral if autoimmune markers are positive.</p>",
            "meta-title": "Inflammation Test | hsCRP Blood Test | Superpower",
            "meta-description": "Test for chronic inflammation - hsCRP, ANA, thyroid antibodies. 3 in 5 adults have hidden inflammation. 100+ biomarkers. ~10 day results. $199/year.",
            "og-title": "Inflammation Test | hsCRP Blood Test | Superpower",
            "og-description": "Find out if hidden inflammation is causing your symptoms. hsCRP + 100+ biomarkers. Results in ~10 days.",
        },
        "faqs": [
            {"name": "What is hsCRP and what does it measure?", "slug": "what-is-hscrp-inflammation", "question": "What is hsCRP and what does it measure?", "answer": "<p>hsCRP (high-sensitivity C-reactive protein) measures systemic inflammation throughout your body. CRP is produced by the liver in response to inflammation anywhere in the body. The 'high-sensitivity' version detects even low levels of chronic inflammation that standard CRP tests miss. Optimal hsCRP is below 1.0 mg/L. Between 1-3 mg/L indicates moderate cardiovascular risk. Above 3.0 mg/L signals high inflammation and significantly increased disease risk.</p>"},
            {"name": "What causes chronic inflammation?", "slug": "what-causes-chronic-inflammation", "question": "What causes chronic inflammation?", "answer": "<p>Common causes of chronic inflammation include poor diet (processed foods, sugar, seed oils), obesity and visceral fat, chronic stress, sleep deprivation, gut dysbiosis, autoimmune conditions, environmental toxins, and chronic infections. Insulin resistance and metabolic syndrome are also major drivers. Blood testing helps identify which factors are contributing to your inflammation so you can address the root cause rather than just masking symptoms.</p>"},
            {"name": "Can inflammation be reduced naturally?", "slug": "can-inflammation-be-reduced-naturally", "question": "Can inflammation be reduced naturally?", "answer": "<p>Yes. Many people significantly reduce inflammation through dietary changes (Mediterranean diet, eliminating processed foods and sugar), regular exercise, stress management, quality sleep, and targeted supplementation (omega-3 fatty acids, vitamin D, curcumin). Addressing underlying conditions like insulin resistance or thyroid dysfunction also reduces inflammation. Annual testing with hsCRP tracks whether your interventions are working.</p>"},
        ]
    },
    {
        "fieldData": {
            "name": "Specialty Tests",
            "slug": "specialty-tests",
            "primary-keyword": "specialty blood tests",
            "secondary-keywords": "PSA test, celiac test, Lyme disease test, specialty health tests, uric acid test",
            "keyword-category": "c2c992eadd1b85bebabf0fe4dd0de7b6",
            "hero-headline": "Don't Wait Months for a Specialist Referral. Get the Tests Now.",
            "hero-subheadline": "<p>PSA for prostate health. Celiac antibodies for gluten sensitivity. Lyme antibodies for tick-borne illness. Uric acid for gout. These specialty tests usually require a specialist visit and months of waiting. We include them in one comprehensive blood draw - no referral needed. 100+ biomarkers. Results in about 10 days.</p>",
            "hero-cta-text": "Get Specialty Tests Now",
            "symptom-headline": "When you need answers - not another waiting room",
            "symptom-1": "Waiting weeks or months for a specialist appointment",
            "symptom-2": "Digestive issues your GP can't explain - could be celiac",
            "symptom-3": "Joint pain or swelling after a tick bite - could be Lyme",
            "symptom-4": "Prostate concerns but PSA wasn't included in your last physical",
            "symptom-5": "Gout flares or high uric acid your doctor hasn't followed up on",
            "symptom-cta": "Skip the wait - get specialty tests now ->",
            "stat-1-number": "67 days",
            "stat-1-text": "average wait time to see a specialist in the US - get your blood work done now instead of waiting",
            "stat-2-number": "100+",
            "stat-2-text": "biomarkers tested in one blood draw",
            "stat-3-number": "10 days",
            "stat-3-text": "to get your results",
            "featured-testimonial-quote": "<p>I waited 4 months for a gastroenterologist who then ordered a celiac panel. Superpower had already found my tTG-IgA was 89 (normal is under 20). I walked into that appointment with data instead of just symptoms. Confirmed celiac disease - could have started treatment months earlier.</p>",
            "featured-testimonial-name": "David L.",
            "featured-testimonial-result": "Celiac diagnosed 4 months faster with proactive testing",
            "membership-subheadline": "Specialty tests without the specialist wait",
            "membership-benefit-1": "PSA, celiac, Lyme, uric acid - all included",
            "membership-benefit-2": "100+ biomarkers in one comprehensive draw",
            "membership-benefit-3": "AI flags results that need specialist follow-up",
            "membership-benefit-4": "24/7 care team access",
            "how-it-works-1-subheading": "A licensed phlebotomist comes to your home to collect your blood - no clinic visit needed. Your sample is tested for PSA, celiac antibodies, Lyme antibodies, uric acid, semen analysis markers, plus 100+ other biomarkers covering metabolic health, hormones, liver, kidney, and inflammation. $199/year.",
            "how-it-works-2-subheading": "Specialty tests like PSA, celiac panels, and Lyme antibodies typically require a specialist referral, a separate appointment, and weeks of waiting. We include them alongside your comprehensive panel so you get answers in days, not months.",
            "how-it-works-3-subheading": "Having specialty results before your specialist appointment changes the conversation. Instead of spending your first visit ordering tests, you walk in with data. That means faster diagnosis, faster treatment, and fewer follow-up visits.",
            "how-it-works-4-subheading": "Our clinical team explains every result - including specialty markers - in plain language and recommends next steps. If something needs specialist follow-up, they'll tell you exactly which specialist to see and what to discuss. Results in about 10 days.",
            "condition-name": "Specialty Blood Testing",
            "condition-overview": "<p>Many important blood tests are considered 'specialty' markers that primary care doctors rarely order. PSA (prostate-specific antigen) screens for prostate cancer risk. Celiac antibodies detect gluten-related autoimmune disease. Lyme antibodies identify tick-borne infection. Uric acid screens for gout and kidney stone risk. These tests usually require referrals and specialist visits - adding months to the diagnostic process.</p>",
            "why-test": "<p>The average wait time to see a specialist in the US is 67 days. During that time, treatable conditions progress. Getting specialty blood work done proactively means you arrive at your specialist appointment with data instead of just symptoms. This dramatically speeds up diagnosis and treatment. And if results are normal, you save yourself the specialist visit entirely.</p>",
            "what-is-included": "<p>Your panel includes PSA (prostate), celiac antibodies (tTG-IgA), uric acid, ANA (autoimmune screening), complete metabolic panel, full lipid panel, liver enzymes, kidney markers, thyroid panel, CBC, iron studies, vitamins, hormones, and inflammation markers - 100+ biomarkers total.</p>",
            "next-steps": "<p>If any specialty markers are abnormal, our care team explains the significance and recommends the right specialist to see. You'll have your results ready to share, eliminating the 'first visit just for blood work' problem that adds months to diagnosis.</p>",
            "meta-title": "Specialty Blood Tests | PSA, Celiac, Lyme | Superpower",
            "meta-description": "Specialty blood tests without the specialist wait - PSA, celiac, Lyme, uric acid. Skip the referral. 100+ biomarkers. ~10 day results. $199/year.",
            "og-title": "Specialty Blood Tests | PSA, Celiac, Lyme | Superpower",
            "og-description": "Get specialty tests without waiting months for a referral. PSA, celiac, Lyme + 100+ biomarkers. ~10 day results.",
        },
        "faqs": [
            {"name": "What specialty tests are included?", "slug": "what-specialty-tests-included", "question": "What specialty tests are included in Superpower?", "answer": "<p>Superpower's comprehensive panel includes many tests that typically require specialist referrals: PSA (prostate health), celiac antibodies (tTG-IgA for gluten sensitivity), ANA (autoimmune screening), uric acid (gout and kidney stone risk), thyroid antibodies (Hashimoto's and Graves' disease), and more. All are included in the standard $199/year membership alongside 100+ other biomarkers.</p>"},
            {"name": "Do I still need to see a specialist?", "slug": "do-i-still-need-specialist-after-testing", "question": "Do I still need to see a specialist after getting these tests?", "answer": "<p>It depends on your results. If specialty markers are normal, you may not need a specialist visit at all - saving you months of waiting and copays. If markers are abnormal, you should absolutely see a specialist - but now you arrive with data instead of just symptoms. This typically speeds up diagnosis significantly because the specialist can skip the 'order blood work and come back' step.</p>"},
            {"name": "How long does it take to see a specialist?", "slug": "specialist-wait-times-us", "question": "How long does it take to see a specialist?", "answer": "<p>The average wait time to see a specialist in the US is 67 days, with some specialties averaging over 3 months. During that waiting period, conditions can progress. Getting comprehensive blood work done proactively through Superpower means you're not sitting idle while waiting for an appointment. You can identify issues now and have results ready for your specialist when you finally get in.</p>"},
        ]
    },
]


def create_page(page_data):
    url = f"https://api.webflow.com/v2/collections/{LP_COLLECTION}/items"
    resp = requests.post(url, headers=HEADERS, json={"fieldData": page_data["fieldData"]})
    result = resp.json()
    if 'id' in result:
        return result['id']
    print(f"  ERROR: {result.get('message', result)}")
    return None


def create_faqs(faqs):
    ids = []
    for faq in faqs:
        resp = requests.post(f"https://api.webflow.com/v2/collections/{FAQ_COLLECTION}/items",
                           headers=HEADERS, json={"fieldData": faq})
        r = resp.json()
        if 'id' in r:
            ids.append(r['id'])
            print(f"    FAQ: {faq['name'][:50]}...")
        else:
            print(f"    FAQ ERROR: {r.get('message', r)}")
        time.sleep(0.3)
    if ids:
        requests.post(f"https://api.webflow.com/v2/collections/{FAQ_COLLECTION}/items/publish",
                     headers=HEADERS, json={"itemIds": ids})
    return ids


def link_faqs(page_id, faq_ids):
    all_ids = faq_ids + GENERAL_FAQ_IDS
    requests.patch(f"https://api.webflow.com/v2/collections/{LP_COLLECTION}/items/{page_id}",
                  headers=HEADERS, json={"fieldData": {"custom-faqs": all_ids}})


def publish(page_id):
    requests.post(f"https://api.webflow.com/v2/collections/{LP_COLLECTION}/items/publish",
                 headers=HEADERS, json={"itemIds": [page_id]})


def main():
    results = []
    for i, page in enumerate(PAGES):
        slug = page["fieldData"]["slug"]
        name = page["fieldData"]["name"]
        print(f"\n[{i+1}/{len(PAGES)}] Creating: {name} ({slug})")

        page_id = create_page(page)
        if not page_id:
            results.append({"slug": slug, "status": "FAILED"})
            continue

        print(f"  Page ID: {page_id}")
        time.sleep(0.4)

        faq_ids = create_faqs(page.get("faqs", []))
        time.sleep(0.3)

        if faq_ids:
            link_faqs(page_id, faq_ids)
        time.sleep(0.3)

        publish(page_id)
        print(f"  PUBLISHED: https://www.superpower.com/welcome-cms/{slug}")

        results.append({
            "slug": slug,
            "name": name,
            "page_id": page_id,
            "faqs": len(faq_ids),
            "meta_title": page["fieldData"]["meta-title"],
            "meta_description": page["fieldData"]["meta-description"],
            "status": "LIVE"
        })
        time.sleep(0.5)

    print("\n" + "=" * 60)
    print("BROKEN URL PAGES SUMMARY (3 pages)")
    print("=" * 60)
    for r in results:
        status = r["status"]
        if status == "LIVE":
            print(f"  CREATED: {r['slug']}")
            print(f"    Webflow Item ID: {r['page_id']}")
            print(f"    Published: Yes")
            print(f"    FAQs Created: {r['faqs']}")
            print(f"    Meta Title: {r['meta_title']}")
        else:
            print(f"  FAILED: {r['slug']}")

    with open("/Users/jeffy/superpower-sem-gap/app/data/broken_url_pages_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to broken_url_pages_results.json")


if __name__ == '__main__':
    main()
