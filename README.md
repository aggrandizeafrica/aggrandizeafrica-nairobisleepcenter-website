# The Sleep Diagnostic & Treatment Centre — new website

A new static website for [nairobisleepcenter.com](https://www.nairobisleepcenter.com) that replaces the WordPress build. It is plain HTML, CSS and a little JavaScript, with no plugins, no database and nothing to patch.

**Design direction:** "Better nights start with answers." The site uses midnight indigo and the clinic's purple, with moonlight gold as the accent colour. The signature visual is an animated hypnogram (a sleep-stage chart from a sleep study), so the first thing a visitor sees is what the clinic actually measures. Headings are set in Fraunces and body text in Manrope, both self-hosted.

## What's in the repo

| Path | What it is |
|---|---|
| `site/` | The finished website. Deploy this folder (Vercel reads `vercel.json`; for cPanel, upload the contents to `public_html`). |
| `build.py` | Generates every page from one place: clinic facts, hours, conditions content, FAQs, team, SEO tags and schema. |
| `src/` | Stylesheet, script, fonts, icons, share image, `robots.txt`, `llms.txt`, `.htaccess`. |

To change content, edit `build.py`, run `python3 build.py` and commit. The `site/` folder is rebuilt each time. Bump `ASSET_V` whenever the CSS or JS changes.

## Pages (17)

Home · Conditions hub · Obstructive sleep apnoea · Snoring · Insomnia · Narcolepsy · Restless legs syndrome · Periodic limb movement disorder · What is sleep? · Sleep study (polysomnography) · CPAP & equipment · About · Our team · Book appointment · Contact · FAQs · Privacy policy · 404

## Audit fixes built in (Website Audit, 14 Nov 2026)

**Critical**
- Brivona theme demo content (DNA testing, cardiology, dentistry) is gone. `/services/` 301-redirects to `/conditions/`.
- One phone number, one address and one set of hours across the whole site, stored once in `CLINIC` / `HOURS` in `build.py`. **Confirm these values: see below.**
- The overlapping hero buttons are fixed. The main CTA is "Book a sleep study", with "WhatsApp us" as the secondary button.
- The "Mary Smith" testimonials have been removed. Real reviews will be added once supplied.
- A privacy policy aligned with the Data Protection Act 2019 is now live at `/privacy-policy/`, and the old `/privacy` link redirects to it.
- Every phone number is a tap-to-call link. There is a floating WhatsApp button, and a Call / WhatsApp / Book bar on mobile.
- The mission statement is about sleep, not ENT. The unverifiable "first and only" and "same-day emergency" claims have been removed.
- No WordPress means no plugins, no `readme.html` and no exposed `admin` author page. Dead `web.` subdomain links are gone.

**SEO**
- Each page has one H1 and a unique title (≤65 characters) and meta description (≤160 characters). The build fails if either runs over.
- Language is set to `lang="en-KE"`, every page has a canonical tag, and there is a `sitemap.xml`.
- Schema: MedicalClinic (with address, phone, hours and parent organisation), MedicalWebPage with MedicalCondition, MedicalTest, FAQPage, BreadcrumbList and Person.
- The thin condition pages are now 450–700 words each, with symptoms, causes, diagnosis, treatment, FAQs and a booking CTA.
- Slugs are cleaned up with 301 redirects: `book-appointment-2` → `book-appointment`, `sleep-studypolysomnography` → `sleep-study-polysomnography`, and `equipments` → `cpap-equipment`.
- Open Graph and X card tags use a 1200×630 share image. `/llms.txt` is included for AI search.

**Performance:** the homepage first view is about 150 KB (HTML, CSS, JS and fonts) with zero third-party scripts. The old site was about 3.1 MB across 76 requests and took around 16 s to load.

**Conversion:** every page has booking CTAs. The sleep study page covers preparation, what to bring, cost and insurance, and results. There are FAQs throughout. Each equipment item has a "Request a quote" button that opens WhatsApp. The booking form sends the request by WhatsApp, so no patient data is stored on the web server. There is also an interactive symptom checker on the homepage.

**Accessibility:** pinch-zoom works, every element has a visible focus style, colour contrast meets WCAG AA, the site respects `prefers-reduced-motion`, and the FAQs use native `<details>` elements.

## Confirm before launch

1. **Phone:** the old site showed both 0780 **537** 851 and 0780 **587** 851. The new site uses **537** (the number in the old footer and on the Contact page).
2. **Address:** the old site showed both Gatundu Road, Kileleshwa and Mbaazi Avenue 10, Lavington. The new site uses **Lavington**. Check that the Google Maps link and embed point to the right place, and update the Google Business Profile to match.
3. **Hours:** the new site uses **Mon–Sat 8:00–5:00**, plus a line saying that sleep studies run overnight by appointment. The old site also showed Mon–Fri 9–5.
4. **Email:** set `CLINIC["email"]`. While it is empty, it stays hidden.
5. **Team:** names and roles come from public sources (Nation, 2024). Send photos, full titles, qualifications and short bios, and say which specialists to list (neurologist, psychiatrist, paediatrician and so on).
6. **WhatsApp:** confirm that the number above is on WhatsApp Business.
7. **Social links:** add them to `SOCIALS` in `build.py`.
8. **Stats:** the "4 in 10" insomnia figures are the centre's own data as reported by Nation and The Standard. Confirm the clinic is happy to publish them.
9. **Old URLs:** confirm the old condition and blog slugs. Add redirects in `vercel.json` / `src/.htaccess` for any that differ from the new ones (`/snoring/`, `/insomnia/`, `/narcolepsy/` and so on).
10. **Reviews:** add real, consented Google reviews.
11. **Privacy policy:** have the clinic or its data protection officer review the template text.
12. **Analytics:** paste the GA4 snippet where `build.py` marks the spot in `<head>`, verify Google Search Console and submit `sitemap.xml`.
13. **Medical review:** a clinician should review the condition pages before go-live.
