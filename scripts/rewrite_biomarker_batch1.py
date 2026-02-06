#!/usr/bin/env python3
"""Batch 1: Rewrite 4 unique Tier 1 biomarker-test pages (no SEM overlap).
Depression, Graves' Disease, Rheumatoid Arthritis, Subclinical Hypothyroidism."""
import requests
import time
import json

API_KEY = "87be5982f1938a9143a7368af984a9863971dd55314fd5a60f482cc02425a0c7"
LP_COLLECTION = "6981a714e199bac70776d880"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

REWRITES = {
    "depression-biomarker-test": {
        "name": "Depression Biomarker Test",
        "hero-headline": "Depression Isn't Always 'In Your Head.' Sometimes It's in Your Blood Work.",
        "hero-subheadline": "<p>Low thyroid, vitamin D deficiency, iron depletion, B12 deficiency, and hormonal imbalances all cause depression symptoms. Before assuming it's purely psychological, rule out the treatable physical causes. One blood draw tests all of them. 100+ biomarkers. Results in about 10 days.</p>",
        "hero-cta-text": "Rule Out Physical Causes",
        "primary-keyword": "depression blood test",
        "secondary-keywords": "blood test for depression, depression biomarkers, physical causes of depression",
        "symptom-headline": "When depression might have a physical cause",
        "symptom-1": "Fatigue and low mood that started without a clear trigger",
        "symptom-2": "Antidepressants that helped at first but stopped working",
        "symptom-3": "Brain fog and difficulty concentrating alongside low mood",
        "symptom-4": "Weight gain, cold sensitivity, or hair loss with your depression",
        "symptom-5": "Depression that gets worse in winter months",
        "symptom-cta": "Find out if a treatable deficiency is driving your symptoms ->",
        "stat-1-number": "1 in 3",
        "stat-1-text": "depression cases have an underlying thyroid, vitamin, or hormonal component that blood testing can identify",
        "stat-2-number": "100+",
        "stat-2-text": "biomarkers tested in one blood draw",
        "stat-3-number": "10 days",
        "stat-3-text": "to get your results",
        "featured-testimonial-quote": "<p>I was on antidepressants for 2 years with minimal improvement. Superpower found my vitamin D was 14, my ferritin was 9, and my TSH was 4.8. Three treatable problems that no one had checked. Addressing those changed everything more than medication alone ever did.</p>",
        "featured-testimonial-name": "Lauren K.",
        "featured-testimonial-result": "3 deficiencies found after 2 years on antidepressants",
        "membership-subheadline": "Rule out physical causes of depression",
        "membership-benefit-1": "Test thyroid, vitamins, iron, and hormones",
        "membership-benefit-2": "100+ biomarkers in one blood draw",
        "membership-benefit-3": "AI flags depression-linked deficiencies",
        "membership-benefit-4": "24/7 care team access",
        "how-it-works-1-subheading": "One blood draw tests TSH, Free T4, vitamin D, B12, folate, ferritin, iron, cortisol, DHEA, testosterone, and CRP - all biomarkers linked to depression - plus 100+ other markers. $199/year.",
        "how-it-works-2-subheading": "Hypothyroidism causes depression in up to 60% of cases. Vitamin D below 20 doubles depression risk. Low ferritin causes fatigue and low mood even with normal hemoglobin. These are fixable problems that standard psychiatric evaluations don't test for.",
        "how-it-works-3-subheading": "We test thyroid alongside hormones, vitamins, and inflammation because depression rarely has a single cause. Low testosterone, elevated cortisol, B12 deficiency, and chronic inflammation all contribute - and all show up in blood work.",
        "how-it-works-4-subheading": "Our clinical team explains which biomarkers may be contributing to your symptoms and recommends targeted interventions - supplementation, thyroid treatment, or specialist referral. Results in about 10 days.",
        "condition-name": "Depression-Related Biomarker Screening",
        "condition-overview": "<p>Depression affects over 21 million American adults. While often treated as purely psychological, research shows that thyroid dysfunction, vitamin D deficiency, iron depletion, B12 deficiency, hormonal imbalances, and chronic inflammation can all cause or worsen depressive symptoms. Blood testing identifies these treatable physical factors.</p>",
        "why-test": "<p>Standard psychiatric evaluations rarely include comprehensive blood work. Yet studies show that up to 1 in 3 depression cases have an identifiable physical component - hypothyroidism, nutrient deficiency, or hormonal imbalance. Treating these underlying causes can improve symptoms significantly, sometimes eliminating the need for medication.</p>",
        "what-is-included": "<p>Your panel includes complete thyroid panel (TSH, Free T4, T3), vitamin D, B12, folate, ferritin, iron studies, cortisol, DHEA, testosterone, CRP, CBC, metabolic panel, and more - 100+ biomarkers total.</p>",
        "next-steps": "<p>If depression-linked biomarkers are abnormal, our care team explains the connection and recommends next steps - vitamin supplementation, thyroid treatment, hormonal support, or specialist referral. Blood testing complements psychiatric care, it doesn't replace it.</p>",
        "meta-title": "Depression Blood Test | Biomarker Screening | Superpower",
        "meta-description": "Blood test for depression causes - thyroid, vitamin D, B12, iron, hormones. Rule out treatable physical causes. 100+ biomarkers. ~10 day results. $199/year.",
        "og-title": "Depression Blood Test | Biomarker Screening | Superpower",
        "og-description": "Rule out physical causes of depression. Thyroid, vitamins, hormones + 100+ biomarkers. ~10 day results.",
    },
    "graves-disease-biomarker-test": {
        "name": "Graves' Disease Biomarker Test",
        "hero-headline": "Heart Racing, Losing Weight, Hands Won't Stop Shaking? Get Your Thyroid Checked.",
        "hero-subheadline": "<p>Graves' disease is the most common cause of hyperthyroidism - and blood work is how you find it. TSH, Free T4, and thyroid antibodies reveal whether your immune system is attacking your thyroid and driving it into overdrive. 100+ biomarkers. Results in about 10 days.</p>",
        "hero-cta-text": "Screen for Graves' Disease",
        "primary-keyword": "graves disease test",
        "secondary-keywords": "graves disease blood test, graves disease biomarkers, hyperthyroidism antibody test",
        "symptom-headline": "Signs that could point to Graves' disease",
        "symptom-1": "Unexplained weight loss even though you're eating normally",
        "symptom-2": "Heart pounding or racing - especially at rest",
        "symptom-3": "Trembling hands that make fine tasks difficult",
        "symptom-4": "Feeling anxious, irritable, or wired for no reason",
        "symptom-5": "Heat intolerance - sweating when others are comfortable",
        "symptom-cta": "Find out if Graves' disease is behind your symptoms ->",
        "stat-1-number": "1 in 200",
        "stat-1-text": "Americans have Graves' disease - many are misdiagnosed as anxiety or heart conditions before thyroid is checked",
        "stat-2-number": "100+",
        "stat-2-text": "biomarkers tested in one blood draw",
        "stat-3-number": "10 days",
        "stat-3-text": "to get your results",
        "featured-testimonial-quote": "<p>I went to the ER twice for heart palpitations. They said it was anxiety. Superpower found my TSH was 0.01 and my thyroid antibodies were through the roof. Graves' disease - not anxiety. The right diagnosis changed everything.</p>",
        "featured-testimonial-name": "Nicole W.",
        "featured-testimonial-result": "Graves' disease diagnosed after 2 ER visits for 'anxiety'",
        "membership-subheadline": "Screen for Graves' disease and monitor treatment",
        "membership-benefit-1": "Complete thyroid panel with antibodies",
        "membership-benefit-2": "100+ biomarkers including heart and metabolic",
        "membership-benefit-3": "AI tracks thyroid trends over time",
        "membership-benefit-4": "24/7 care team access",
        "how-it-works-1-subheading": "One blood draw tests TSH, Free T4, T3, and thyroid antibodies (TPO, thyroglobulin) - the key Graves' disease markers - plus 100+ other biomarkers including heart, liver, metabolic, and inflammation markers. $199/year.",
        "how-it-works-2-subheading": "Graves' disease causes the thyroid to produce excess hormone, speeding up your entire metabolism. TSH drops to near zero while T4 and T3 spike. Thyroid antibodies confirm the autoimmune cause. Without blood work, it's often misdiagnosed as anxiety or cardiac problems.",
        "how-it-works-3-subheading": "Untreated Graves' disease damages the heart, bones, and eyes. We test thyroid markers alongside calcium, liver enzymes, and CBC because hyperthyroidism affects multiple organ systems. Catching it early prevents complications.",
        "how-it-works-4-subheading": "Our clinical team explains your thyroid results and recommends next steps - endocrinologist referral for confirmed Graves', or monitoring for borderline cases. Results in about 10 days.",
        "condition-name": "Graves' Disease Screening",
        "condition-overview": "<p>Graves' disease is an autoimmune condition where the immune system attacks the thyroid gland, causing it to produce excess thyroid hormone (hyperthyroidism). It affects about 1 in 200 Americans and is 7-8 times more common in women. Symptoms include weight loss, rapid heartbeat, tremors, anxiety, and heat intolerance. Blood testing is essential for diagnosis.</p>",
        "why-test": "<p>Graves' disease symptoms overlap heavily with anxiety, cardiac conditions, and menopause. Many patients see cardiologists or psychiatrists before anyone checks their thyroid. A simple blood test - TSH plus thyroid antibodies - confirms or rules out Graves' disease definitively. Early detection prevents serious complications including heart damage and bone loss.</p>",
        "what-is-included": "<p>Your panel includes TSH, Free T4, T3, thyroid antibodies (TPO, thyroglobulin), CBC, complete metabolic panel, calcium, liver enzymes, lipid panel, and inflammation markers - 100+ biomarkers total.</p>",
        "next-steps": "<p>If thyroid markers suggest Graves' disease (suppressed TSH, elevated T4/T3, positive antibodies), our care team recommends endocrinologist referral for treatment options including medication, radioactive iodine, or monitoring. Annual retesting tracks treatment response.</p>",
        "meta-title": "Graves' Disease Test | Thyroid Antibodies | Superpower",
        "meta-description": "Screen for Graves' disease - TSH, Free T4, thyroid antibodies. Often misdiagnosed as anxiety. 100+ biomarkers. ~10 day results. $199/year.",
        "og-title": "Graves' Disease Test | Thyroid Antibodies | Superpower",
        "og-description": "Screen for Graves' disease with thyroid antibodies + 100+ biomarkers. Results in ~10 days.",
    },
    "rheumatoid-arthritis-biomarker-test": {
        "name": "Rheumatoid Arthritis Biomarker Test",
        "hero-headline": "Morning Stiffness That Takes Hours to Fade? Your Blood Work Has Answers.",
        "hero-subheadline": "<p>Rheumatoid arthritis causes joint damage years before it shows up on X-rays. Blood markers - ANA, CRP, and CBC - screen for the autoimmune inflammation driving your joint pain. Early detection means early treatment and less permanent damage. 100+ biomarkers. Results in about 10 days.</p>",
        "hero-cta-text": "Screen for RA Biomarkers",
        "primary-keyword": "rheumatoid arthritis blood test",
        "secondary-keywords": "RA blood test, rheumatoid arthritis biomarkers, autoimmune arthritis test",
        "symptom-headline": "Signs that joint pain could be rheumatoid arthritis",
        "symptom-1": "Morning stiffness lasting more than 30 minutes",
        "symptom-2": "Joint pain that's symmetric - both hands, both knees",
        "symptom-3": "Swollen, warm joints that feel worse after rest, not activity",
        "symptom-4": "Fatigue that feels disproportionate to your activity level",
        "symptom-5": "Family history of autoimmune conditions",
        "symptom-cta": "Find out if autoimmune inflammation is the cause ->",
        "stat-1-number": "1.3M",
        "stat-1-text": "Americans have rheumatoid arthritis - early diagnosis within 6 months leads to significantly better outcomes",
        "stat-2-number": "100+",
        "stat-2-text": "biomarkers tested in one blood draw",
        "stat-3-number": "10 days",
        "stat-3-text": "to get your results",
        "featured-testimonial-quote": "<p>My hands hurt for a year before I got tested. X-rays showed nothing. Superpower found my CRP was 8.2, ANA was positive, and my ESR was elevated. Rheumatologist confirmed RA and started treatment immediately. Glad I didn't wait for joint damage to show up on imaging.</p>",
        "featured-testimonial-name": "Sandra P.",
        "featured-testimonial-result": "RA diagnosed 6 months before X-ray changes appeared",
        "membership-subheadline": "Screen for autoimmune inflammation",
        "membership-benefit-1": "ANA, CRP, and CBC - key RA screening markers",
        "membership-benefit-2": "100+ biomarkers including inflammation panel",
        "membership-benefit-3": "AI flags autoimmune and inflammation patterns",
        "membership-benefit-4": "24/7 care team access",
        "how-it-works-1-subheading": "One blood draw tests ANA (antinuclear antibodies), CRP, CBC with differential, ESR, ferritin, and metabolic panel - key rheumatoid arthritis screening markers - plus 100+ other biomarkers. $199/year.",
        "how-it-works-2-subheading": "Rheumatoid arthritis is an autoimmune condition where your immune system attacks joint tissue. ANA screens for autoimmune activity. CRP and ESR measure inflammation levels. CBC can reveal the anemia that often accompanies RA. Blood markers detect the disease before joint damage is visible on imaging.",
        "how-it-works-3-subheading": "Note: Superpower's panel includes ANA, CRP, and CBC - the initial screening markers. A rheumatologist may order additional tests like RF (rheumatoid factor) and anti-CCP antibodies for definitive diagnosis. Our results help determine if that referral is warranted.",
        "how-it-works-4-subheading": "Our clinical team explains your autoimmune and inflammation markers and recommends next steps. If screening markers are positive, they'll recommend rheumatology referral for complete evaluation. Results in about 10 days.",
        "condition-name": "Rheumatoid Arthritis Screening",
        "condition-overview": "<p>Rheumatoid arthritis (RA) is a chronic autoimmune disease that causes joint inflammation, pain, and progressive damage. It affects 1.3 million Americans and is 2-3 times more common in women. Unlike osteoarthritis (wear-and-tear), RA is driven by immune system dysfunction. Early diagnosis and treatment within the first 6 months dramatically improves long-term outcomes.</p>",
        "why-test": "<p>RA causes irreversible joint damage, but early treatment can prevent it. Blood markers like ANA and CRP detect autoimmune inflammation before X-rays show damage. Many people with joint pain dismiss it as normal aging when it's actually treatable autoimmune disease. Screening blood work helps determine if a rheumatology referral is warranted.</p>",
        "what-is-included": "<p>Your panel includes ANA, CRP, CBC with differential, ESR, ferritin, iron studies, complete metabolic panel, liver enzymes, kidney markers, thyroid panel, and vitamin D - 100+ biomarkers total. Note: RF and anti-CCP (definitive RA markers) require specialist testing.</p>",
        "next-steps": "<p>If ANA is positive and/or CRP is elevated with joint symptoms, our care team recommends rheumatology referral for definitive testing (RF, anti-CCP). Early RA treatment with DMARDs can halt disease progression and prevent permanent joint damage.</p>",
        "meta-title": "RA Blood Test | Rheumatoid Arthritis Screening | Superpower",
        "meta-description": "Screen for rheumatoid arthritis - ANA, CRP, CBC. Catch autoimmune inflammation before joint damage. 100+ biomarkers. ~10 day results. $199/year.",
        "og-title": "RA Blood Test | Rheumatoid Arthritis Screening | Superpower",
        "og-description": "Screen for rheumatoid arthritis with ANA + CRP + 100+ biomarkers. Results in ~10 days.",
    },
    "subclinical-hypothyroidism-biomarker-test": {
        "name": "Subclinical Hypothyroidism Biomarker Test",
        "hero-headline": "Your TSH Is 'Borderline.' Your Symptoms Aren't. That Gap Matters.",
        "hero-subheadline": "<p>Subclinical hypothyroidism means your TSH is elevated but your T4 is still normal. Most doctors say 'watch and wait.' Meanwhile you're exhausted, gaining weight, and losing hair. Blood testing shows the full picture - including thyroid antibodies that predict whether it will progress. 100+ biomarkers. Results in about 10 days.</p>",
        "hero-cta-text": "Get Your Full Thyroid Panel",
        "primary-keyword": "subclinical hypothyroidism test",
        "secondary-keywords": "borderline thyroid, subclinical hypothyroidism blood test, high TSH normal T4",
        "symptom-headline": "When 'borderline' thyroid still causes real symptoms",
        "symptom-1": "Fatigue and brain fog that your doctor can't explain",
        "symptom-2": "Weight creeping up despite no changes to diet or exercise",
        "symptom-3": "TSH between 4-10 but told to 'just monitor it'",
        "symptom-4": "Hair thinning or dry skin that started gradually",
        "symptom-5": "Feeling cold when everyone else is comfortable",
        "symptom-cta": "Get the full thyroid picture your doctor isn't testing ->",
        "stat-1-number": "10%",
        "stat-1-text": "of adults have subclinical hypothyroidism - most are told their thyroid is 'fine' because T4 is still normal",
        "stat-2-number": "100+",
        "stat-2-text": "biomarkers tested in one blood draw",
        "stat-3-number": "10 days",
        "stat-3-text": "to get your results",
        "featured-testimonial-quote": "<p>My TSH was 6.2 for three years and my doctor said it was 'borderline - just watch it.' Superpower found my TPO antibodies were 380 - I had Hashimoto's slowly destroying my thyroid. Finally got treatment and the fatigue, weight gain, and brain fog cleared up within weeks.</p>",
        "featured-testimonial-name": "Emily R.",
        "featured-testimonial-result": "Hashimoto's diagnosed after 3 years of 'borderline' TSH",
        "membership-subheadline": "Track your thyroid before it gets worse",
        "membership-benefit-1": "Full thyroid panel with antibodies",
        "membership-benefit-2": "100+ biomarkers including iron and vitamins",
        "membership-benefit-3": "AI tracks TSH trends and progression risk",
        "membership-benefit-4": "24/7 care team access",
        "how-it-works-1-subheading": "One blood draw tests TSH, Free T4, T3, thyroid antibodies (TPO, thyroglobulin), plus ferritin, vitamin D, B12, cortisol, and 90+ other biomarkers that affect thyroid function. $199/year.",
        "how-it-works-2-subheading": "Subclinical hypothyroidism is the gray zone - TSH is elevated (4.5-10) but T4 is still normal. Many doctors dismiss it, but thyroid antibodies determine if it will progress. Positive antibodies mean Hashimoto's is the cause and treatment may be warranted now, not later.",
        "how-it-works-3-subheading": "Iron, vitamin D, and cortisol all affect thyroid function. Low ferritin impairs thyroid hormone conversion. Vitamin D deficiency worsens autoimmune thyroid disease. We test these alongside your thyroid panel to identify all contributing factors.",
        "how-it-works-4-subheading": "Our clinical team explains whether your subclinical hypothyroidism is likely to progress and recommends next steps - endocrinologist referral, supplementation, or monitoring schedule. Results in about 10 days.",
        "condition-name": "Subclinical Hypothyroidism Screening",
        "condition-overview": "<p>Subclinical hypothyroidism affects about 10% of adults. It's defined as elevated TSH (typically 4.5-10 mIU/L) with normal Free T4. While some cases resolve spontaneously, those caused by Hashimoto's thyroiditis (detectable via thyroid antibodies) typically progress to overt hypothyroidism. Many patients experience symptoms even in the subclinical range.</p>",
        "why-test": "<p>Standard thyroid testing (TSH only) identifies the problem but doesn't explain the cause. Thyroid antibodies (TPO and thyroglobulin) determine whether Hashimoto's autoimmune disease is driving the elevated TSH. This distinction matters because Hashimoto's-driven subclinical hypothyroidism is much more likely to progress and may benefit from earlier treatment.</p>",
        "what-is-included": "<p>Your panel includes TSH, Free T4, T3 uptake, thyroid antibodies (TPO, thyroglobulin), ferritin, vitamin D, B12, cortisol, CRP, complete metabolic panel, lipid panel, and CBC - 100+ biomarkers total.</p>",
        "next-steps": "<p>If subclinical hypothyroidism with positive antibodies is detected, our care team recommends endocrinologist consultation. If antibodies are negative, we recommend annual monitoring to track whether TSH is trending up or stabilizing. Addressing iron, vitamin D, and other cofactors can improve thyroid function.</p>",
        "meta-title": "Subclinical Hypothyroidism Test | TSH + Antibodies | Superpower",
        "meta-description": "Test for subclinical hypothyroidism - TSH, Free T4, thyroid antibodies. Borderline thyroid? Find out if it will progress. 100+ biomarkers. $199/year.",
        "og-title": "Subclinical Hypothyroidism Test | Superpower",
        "og-description": "Borderline thyroid? Antibodies show if it will progress. Full thyroid panel + 100+ biomarkers. ~10 day results.",
    },
}


def fetch_all_pages():
    all_items = []
    offset = 0
    while True:
        url = f"https://api.webflow.com/v2/collections/{LP_COLLECTION}/items?limit=100&offset={offset}"
        resp = requests.get(url, headers=HEADERS)
        data = resp.json()
        items = data.get("items", [])
        all_items.extend(items)
        total = data.get("pagination", {}).get("total", 0)
        if offset + 100 >= total:
            break
        offset += 100
        time.sleep(0.3)
    return all_items


def main():
    print("=" * 70)
    print("BATCH 1: Rewrite 4 Unique Tier 1 Biomarker-Test Pages")
    print("=" * 70)

    print("\nFetching all pages...")
    all_items = fetch_all_pages()
    slug_map = {}
    for item in all_items:
        slug = item.get("fieldData", {}).get("slug", "")
        if slug:
            slug_map[slug] = item

    results = []
    for slug, fields in REWRITES.items():
        if slug not in slug_map:
            print(f"\n  SKIP: {slug} not found")
            results.append({"slug": slug, "status": "NOT_FOUND"})
            continue

        item_id = slug_map[slug]["id"]
        print(f"\n  REWRITING: {slug} (ID: {item_id})")

        url = f"https://api.webflow.com/v2/collections/{LP_COLLECTION}/items/{item_id}"
        resp = requests.patch(url, headers=HEADERS, json={"fieldData": fields})
        if resp.status_code == 200:
            print(f"    Updated successfully")
            results.append({"slug": slug, "item_id": item_id, "status": "UPDATED", "meta_title": fields["meta-title"]})
        else:
            print(f"    ERROR: {resp.status_code} {resp.text[:200]}")
            results.append({"slug": slug, "item_id": item_id, "status": "ERROR"})
        time.sleep(0.4)

    # Publish all updated pages
    updated_ids = [r["item_id"] for r in results if r["status"] == "UPDATED"]
    if updated_ids:
        print(f"\nPublishing {len(updated_ids)} pages...")
        url = f"https://api.webflow.com/v2/collections/{LP_COLLECTION}/items/publish"
        resp = requests.post(url, headers=HEADERS, json={"itemIds": updated_ids})
        print(f"  Publish: {resp.status_code}")

    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")
    for r in results:
        print(f"  {r['slug']}: {r['status']}")

    with open("/Users/jeffy/superpower-sem-gap/app/data/biomarker_rewrite_batch1.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to biomarker_rewrite_batch1.json")


if __name__ == "__main__":
    main()
