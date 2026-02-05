/**
 * Superpower Checkout Page Personalization
 *
 * Self-contained script that personalizes /checkout based on sp_variant URL parameter.
 * Reads personalization data from window.__SP_PERSONALIZATION_DATA (set by GTM variable
 * or inline script) OR fetches it from a hosted JSON file.
 *
 * Deployment options:
 *   1. GTM Custom HTML tag (if GTM is added to the checkout app)
 *   2. <script> tag added directly to the checkout app by engineering
 *   3. Chrome DevTools console paste for testing
 *
 * Target page: superpower.com/checkout?sp_variant={slug}
 *
 * DOM targets (from actual page source):
 *   - h3.typography-heading3 (first) = "Get Actionable Insights in 10 days"
 *   - p.typography-largebody.text-secondary-foreground = subtitle
 *   - button[type="submit"] = "Continue"
 *   - h3.typography-heading3 (second, in Order Summary) = "Superpower Membership"
 *   - p after second h3 = membership description
 */
(function() {
  'use strict';

  // 1. Read sp_variant from URL
  var params = new URLSearchParams(window.location.search);
  var variant = params.get('sp_variant');
  if (!variant) return;

  // 2. Get personalization data
  var data = window.__SP_PERSONALIZATION_DATA;
  if (!data || !data[variant]) {
    console.log('[SP Personalization] No data for variant:', variant);
    return;
  }

  var page = data[variant];
  console.log('[SP Personalization] Applying variant:', variant);

  var MAX_ATTEMPTS = 50;
  var INTERVAL_MS = 100;
  var attempt = 0;

  function applyPersonalization() {
    attempt++;

    // Find the checkout form column - left side of the 2-column grid
    var headings = document.querySelectorAll('h3.typography-heading3');
    var headline = null;
    var membershipHeading = null;

    // First h3 = "Get Actionable Insights..." (in the form column)
    // Second h3 = "Superpower Membership" (in the order summary)
    for (var i = 0; i < headings.length; i++) {
      var text = headings[i].textContent.trim();
      if (text.indexOf('Get Actionable') !== -1 || text.indexOf('Insights') !== -1) {
        headline = headings[i];
      } else if (text.indexOf('Superpower Membership') !== -1) {
        membershipHeading = headings[i];
      }
    }

    // Also try matching any first h3 if the text changed
    if (!headline && headings.length > 0) {
      headline = headings[0];
    }

    // Find subtitle
    var subtitle = headline ? headline.nextElementSibling : null;
    if (subtitle && subtitle.tagName !== 'P') subtitle = null;

    // Find CTA button
    var ctaBtn = document.querySelector('button[type="submit"]');

    // Retry if page hasn't rendered yet
    if (!headline && attempt < MAX_ATTEMPTS) {
      setTimeout(applyPersonalization, INTERVAL_MS);
      return;
    }

    if (!headline) {
      console.log('[SP Personalization] Could not find headline after', attempt, 'attempts');
      return;
    }

    // --- Apply replacements ---

    // Replace headline
    if (page.headline) {
      headline.textContent = page.headline;
      headline.style.opacity = '1';
      headline.style.transform = 'none';
      // Also fix the parent's opacity/transform (SSR animation wrapper)
      var animWrapper = headline.parentElement;
      if (animWrapper && animWrapper.style.opacity === '0') {
        animWrapper.style.opacity = '1';
        animWrapper.style.transform = 'none';
      }
    }

    // Replace subtitle with condition-specific text
    if (subtitle && page.stat1Number && page.stat1Text) {
      subtitle.textContent = page.stat1Number + ' ' + page.stat1Text + '. Find out where you stand.';
    }

    // Replace CTA button text
    if (ctaBtn && page.ctaText) {
      ctaBtn.textContent = page.ctaText;
    }

    // Replace membership description with personalized benefits
    if (membershipHeading && page.benefit1) {
      var membershipDesc = membershipHeading.nextElementSibling;
      if (membershipDesc && membershipDesc.tagName === 'P') {
        var benefits = [page.benefit1, page.benefit2, page.benefit3, page.benefit4]
          .filter(function(b) { return b; });
        membershipDesc.innerHTML = benefits.map(function(b) {
          return '<span style="display:block;padding:2px 0;">\u2713 ' + b + '</span>';
        }).join('');
      }
    }

    // Inject testimonial after the form
    if (page.testimonialQuote && page.testimonialName) {
      if (!document.getElementById('sp-testimonial')) {
        var form = document.querySelector('form');
        if (form && form.parentElement) {
          var testimonialHTML =
            '<div id="sp-testimonial" style="' +
              'margin-top:24px;padding:20px 24px;' +
              'background:white;border-radius:12px;border:1px solid #e5e7eb;' +
              'font-family:inherit;' +
            '">' +
              '<p style="font-size:15px;line-height:1.6;color:#374151;margin:0 0 8px 0;font-style:italic;">' +
                '\u201C' + page.testimonialQuote + '\u201D' +
              '</p>' +
              '<p style="font-size:13px;color:#6b7280;margin:0;font-weight:600;">' +
                page.testimonialName +
                (page.testimonialResult ? ' \u2014 ' + page.testimonialResult : '') +
              '</p>' +
            '</div>';
          form.parentElement.insertAdjacentHTML('beforeend', testimonialHTML);
        }
      }
    }

    // Push analytics event
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      event: 'sp_personalization_applied',
      sp_variant: variant,
      sp_headline: page.headline || '',
      sp_elements_replaced: [headline, ctaBtn, subtitle, membershipHeading].filter(Boolean).length
    });

    console.log('[SP Personalization] Applied successfully. Elements replaced:',
      [headline ? 'headline' : null, ctaBtn ? 'cta' : null, subtitle ? 'subtitle' : null,
       membershipHeading ? 'membership' : null].filter(Boolean).join(', '));
  }

  // Start - wait for DOM ready if needed
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyPersonalization);
  } else {
    applyPersonalization();
  }
})();
