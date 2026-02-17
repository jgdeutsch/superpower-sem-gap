#!/usr/bin/env python3
"""
Rebuild GTM personalization tags from personalization_data.json.

Reads the master personalization_data.json (153 entries), sorts alphabetically,
splits roughly in half, and generates two self-contained GTM Custom HTML tags:
  - register_personalization_tag_part1.html (with Labcorp regex fallback)
  - register_personalization_tag_part2.html (simple return on no match)

Each file must be under 102,400 characters (GTM tag limit).
"""

import json
import math
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, '..', 'data', 'personalization_data.json')
GTM_DIR = os.path.join(SCRIPT_DIR, '..', 'gtm')

GTM_LIMIT = 102_400

# Labcorp regex fallback block (only in Part 1)
LABCORP_FALLBACK = (
    'var LC=/^([a-z]{2})-(.+?)-(labcorp|lab-corp|lab-corporation|laboratory-corporation|lab-draw|lablinc|clinical-labs|diagnostic|quest-diag|paml|sanford|ur-medicine|walmart|xero-labs|accupro|accurate-screen|any-lab|avera|baycare|drugtek|institute-diag|jbhf|mng-labcorp|my-forever|wake-diag|covid-19)/;\n'
    '    var lcMatch=LC.exec(variant);\n'
    '    if (!lcMatch) return;\n'
    '    var stAbbr=lcMatch[1].toUpperCase();\n'
    '    var cityRaw=lcMatch[2].replace(/-/g,\' \').replace(/\\b\\w/g,function(c){return c.toUpperCase();});\n'
    '    var locLabel=cityRaw+\', \'+stAbbr;\n'
    '    var isNY=/^(ny|nj)-/.test(variant);\n'
    '    if(isNY){page={"headline":"90+ Blood Tests in "+locLabel+". One Draw. $399.","ctaText":"Start Testing","subtitleOverride":"90+ biomarkers in one blood draw at a lab near you in "+locLabel+". $399/year, HSA/FSA eligible.","testimonialQuote":"Annual physical said everything was \\u2018normal.\\u2019 Superpower found prediabetes, vitamin D at 18, and early thyroid dysfunction. Same lab I always go to - just 90+ markers instead of 20. Three things my doctor completely missed.","testimonialName":"David W.","testimonialResult":"Found 3 issues at his regular lab","benefit1":"Walk into a lab near you in "+locLabel,"benefit2":"90+ biomarkers vs the ~20 your doctor orders","benefit3":"AI analysis spots patterns across all markers","benefit4":"$399/year, HSA/FSA eligible","stat1Number":"90+","stat1Text":"biomarkers in one blood draw at your local lab"};}\n'
    '    else{page={"headline":"100+ Blood Tests in "+locLabel+". One Draw. $199.","ctaText":"Start Testing","subtitleOverride":"100+ biomarkers in one blood draw at a lab near you in "+locLabel+". $199/year, HSA/FSA eligible.","testimonialQuote":"Annual physical said everything was \\u2018normal.\\u2019 Superpower found prediabetes, vitamin D at 18, and early thyroid dysfunction. Same lab I always go to - just 100+ markers instead of 20. Three things my doctor completely missed.","testimonialName":"David W.","testimonialResult":"Found 3 issues at his regular lab","benefit1":"Walk into a lab near you in "+locLabel,"benefit2":"100+ biomarkers vs the ~20 your doctor orders","benefit3":"AI analysis spots patterns across all markers","benefit4":"$199/year, HSA/FSA eligible","stat1Number":"100+","stat1Text":"biomarkers in one blood draw at your local lab"};}'
)

SIMPLE_RETURN = 'return;'


def build_tag_html(data_dict, entry_count, no_match_block):
    """Build a complete GTM Custom HTML tag string."""
    minified_data = json.dumps(data_dict, separators=(',', ':'), ensure_ascii=False)

    return (
        '<script>\n'
        '// GTM Custom HTML Tag: Register/Checkout Page Personalization\n'
        f'// Self-contained with baked-in data for {entry_count} landing page variants.\n'
        '// Trigger: DOM Ready, Page Path contains /register or /checkout, sp_variant in URL\n'
        '(function() {\n'
        "  if (document.getElementById('sp-testimonial')) return;\n"
        '  var params = new URLSearchParams(window.location.search);\n'
        "  var variant = params.get('sp_variant');\n"
        '  if (!variant) return;\n'
        '\n'
        f'  var DATA = {minified_data};\n'
        '\n'
        '  var page = DATA[variant];\n'
        '  if (!page) {\n'
        f'{no_match_block}\n'
        '  }\n'
        '\n'
        '  var MAX_ATTEMPTS = 20;\n'
        '  var attempt = 0;\n'
        '\n'
        '  function apply() {\n'
        '    attempt++;\n'
        "    var headings = document.querySelectorAll('h3.typography-heading3, h3');\n"
        '    var headline = null;\n'
        '    var membershipHeading = null;\n'
        '\n'
        '    for (var i = 0; i < headings.length; i++) {\n'
        '      var t = headings[i].textContent.trim();\n'
        "      if (t.indexOf('Get Actionable') !== -1 || t.indexOf('Insights') !== -1) headline = headings[i];\n"
        "      else if (t.indexOf('Superpower Membership') !== -1) membershipHeading = headings[i];\n"
        '    }\n'
        '    if (!headline && headings.length > 0) headline = headings[0];\n'
        '    if (!headline && attempt < MAX_ATTEMPTS) { setTimeout(apply, 100); return; }\n'
        '    if (!headline) return;\n'
        '\n'
        '    var subtitle = headline.nextElementSibling;\n'
        "    if (subtitle && subtitle.tagName !== 'P') subtitle = null;\n"
        "    var ctaBtn = document.querySelector('button[type=\"submit\"]');\n"
        '\n'
        '    if (page.headline) {\n'
        '      headline.textContent = page.headline;\n'
        '      var w = headline.parentElement;\n'
        "      if (w && w.style.opacity === '0') { w.style.opacity = '1'; w.style.transform = 'none'; }\n"
        '    }\n'
        '    if (subtitle) {\n'
        '      if (page.subtitleOverride) {\n'
        '        subtitle.textContent = page.subtitleOverride;\n'
        '      } else if (page.stat1Number && page.stat1Text) {\n'
        "        subtitle.textContent = page.stat1Number + ' ' + page.stat1Text + '. Find out where you stand.';\n"
        '      }\n'
        '    }\n'
        '    if (ctaBtn && page.ctaText) ctaBtn.textContent = page.ctaText;\n'
        '\n'
        '    if (membershipHeading && page.benefit1) {\n'
        '      var desc = membershipHeading.nextElementSibling;\n'
        "      if (desc && desc.tagName === 'P') {\n"
        '        var b = [page.benefit1, page.benefit2, page.benefit3, page.benefit4].filter(Boolean);\n'
        "        desc.innerHTML = b.map(function(x){return '<span style=\"display:block;padding:2px 0;\">&#10003;'+x+'</span>';}).join('');\n"
        '      }\n'
        '    }\n'
        '\n'
        "    if (page.testimonialQuote && page.testimonialName && !document.getElementById('sp-testimonial')) {\n"
        "      var form = document.querySelector('form');\n"
        '      if (form && form.parentElement) {\n'
        "        form.parentElement.insertAdjacentHTML('beforeend',\n"
        """          '<div id="sp-testimonial" style="margin-top:24px;padding:20px 24px;background:white;border-radius:12px;border:1px solid #e5e7eb;font-family:inherit;">' +\n"""
        """          '<p style="font-size:15px;line-height:1.6;color:#374151;margin:0 0 8px;font-style:italic;">"'+page.testimonialQuote+'"</p>' +\n"""
        """          '<p style="font-size:13px;color:#6b7280;margin:0;font-weight:600;">'+page.testimonialName+\n"""
        "          (page.testimonialResult?' &mdash;'+page.testimonialResult:'')+'</p></div>');\n"
        '      }\n'
        '    }\n'
        '\n'
        '    window.dataLayer = window.dataLayer || [];\n'
        "    window.dataLayer.push({ event:'sp_personalization_applied', sp_variant:variant, sp_headline:page.headline||'' });\n"
        '  }\n'
        '  apply();\n'
        '})();\n'
        '</script>\n'
    )


def main():
    with open(DATA_PATH, 'r') as f:
        all_data = json.load(f)

    total = len(all_data)
    print(f"Loaded {total} entries from personalization_data.json")

    if total != 153:
        print(f"WARNING: Expected 153 entries, got {total}")

    sorted_keys = sorted(all_data.keys())

    # Split roughly in half: ceil gives first half the extra entry if odd
    split_point = math.ceil(total / 2)  # 77 in part1, 76 in part2 for 153
    part1_keys = sorted_keys[:split_point]
    part2_keys = sorted_keys[split_point:]

    print(f"Part 1: {len(part1_keys)} entries ({part1_keys[0]!r} ... {part1_keys[-1]!r})")
    print(f"Part 2: {len(part2_keys)} entries ({part2_keys[0]!r} ... {part2_keys[-1]!r})")
    print(f"Total: {len(part1_keys) + len(part2_keys)}")

    part1_data = {k: all_data[k] for k in part1_keys}
    part2_data = {k: all_data[k] for k in part2_keys}

    part1_html = build_tag_html(part1_data, len(part1_keys), LABCORP_FALLBACK)
    part2_html = build_tag_html(part2_data, len(part2_keys), SIMPLE_RETURN)

    part1_size = len(part1_html)
    part2_size = len(part2_html)

    print(f"\nPart 1: {part1_size:,} characters")
    print(f"Part 2: {part2_size:,} characters")
    print(f"GTM limit: {GTM_LIMIT:,} characters")

    if part1_size > GTM_LIMIT:
        print(f"ERROR: Part 1 exceeds GTM limit by {part1_size - GTM_LIMIT:,} characters!")
        print("Attempting rebalance...")
        while part1_size > GTM_LIMIT and len(part1_keys) > len(part2_keys):
            moved_key = part1_keys.pop()
            part2_keys.insert(0, moved_key)
            part1_data = {k: all_data[k] for k in part1_keys}
            part2_data = {k: all_data[k] for k in part2_keys}
            part1_html = build_tag_html(part1_data, len(part1_keys), LABCORP_FALLBACK)
            part2_html = build_tag_html(part2_data, len(part2_keys), SIMPLE_RETURN)
            part1_size = len(part1_html)
            part2_size = len(part2_html)
            print(f"  Rebalanced: Part 1 = {len(part1_keys)} ({part1_size:,}), Part 2 = {len(part2_keys)} ({part2_size:,})")

    if part2_size > GTM_LIMIT:
        print(f"ERROR: Part 2 exceeds GTM limit by {part2_size - GTM_LIMIT:,} characters!")
        sys.exit(1)

    if part1_size > GTM_LIMIT:
        print("ERROR: Could not rebalance to fit within GTM limit!")
        sys.exit(1)

    assert len(part1_keys) + len(part2_keys) == total, \
        f"Entry count mismatch: {len(part1_keys)} + {len(part2_keys)} != {total}"

    part1_path = os.path.join(GTM_DIR, 'register_personalization_tag_part1.html')
    part2_path = os.path.join(GTM_DIR, 'register_personalization_tag_part2.html')

    with open(part1_path, 'w') as f:
        f.write(part1_html)
    print(f"\nWrote: {part1_path}")

    with open(part2_path, 'w') as f:
        f.write(part2_html)
    print(f"Wrote: {part2_path}")

    for path, label in [(part1_path, 'Part 1'), (part2_path, 'Part 2')]:
        file_size = os.path.getsize(path)
        print(f"  {label}: {file_size:,} bytes on disk")

    print(f"\nTotal entries: {len(part1_keys)} + {len(part2_keys)} = {len(part1_keys) + len(part2_keys)}")
    print("Done.")


if __name__ == '__main__':
    main()
