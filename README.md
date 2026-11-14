# The Sleep Diagnostic & Treatment Centre — new website

A new static website for [nairobisleepcenter.com](https://www.nairobisleepcenter.com) that replaces the WordPress build. It is plain HTML, CSS and a little JavaScript, with no plugins, no database and nothing to patch.

**Design direction:** "Better nights start with answers." The site uses the official logo purple `#764C8C` and green `#007647`, with brand green as the button colour. The full-colour logo sits on a white header, and a reversed white-and-green version is used on the deep-purple footer. Dark sections use deeper shades of the brand purple. The full-colour version is at `src/assets/img/logo.svg`. The signature visual is an animated hypnogram (a sleep-stage chart from a sleep study), so the first thing a visitor sees is what the clinic actually measures. Headings are set in Fraunces and body text in Manrope, both self-hosted.

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
- One set of contact details everywhere, taken from the company profile (main line 0780 **587** 851, so the old footer's 537 was the typo) and stored once in `CLINIC` in `build.py`.
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

## Source of facts

Contact details, founders, mission, vision, values, services and licence number come from the clinic's **Company Profile** (last saved June 2026):
- Phones: 0780 587 851 (main and WhatsApp) and 0768 824 184
- Email: admin@nairobisleepcenter.com · P.O. Box 29740 – 00202 Nairobi
- Address: Mbaazi Avenue No. 10, Lavington
- Founded in 2018 by ENT surgeons Prof. Muthure Macharia, Dr Chimmy Omamo-Olende and Dr Samuel M. Nyagah
- Licence: Medical Practitioners and Dentists Board No. 016750 (shown in the footer). The KRA PIN and incorporation number are deliberately **not** published.

## Confirm before launch

1. **Hours:** these are not in the profile. The new site uses **Mon–Sat 8:00–5:00**, plus a line saying sleep studies run overnight by appointment (the old site also showed Mon–Fri 9–5).
2. **WhatsApp:** the site uses 0780 587 851. Confirm it is on WhatsApp Business, or switch `CLINIC["whatsapp"]` to the 0768 line.
3. **"First and only sleep lab in Sub-Saharan Africa outside South Africa":** this claim is in the profile but has been left off the site, as the audit recommended. It is hard to prove and risky for a medical provider. Add it back only if the clinic can substantiate it.
4. **Team:** send photos, full titles, qualifications and short bios. Say whether Dr Caroline Muturi, Margaret Karani (clinical psychologist) and Peter Kamau (sleep technologist) should be listed; their names came from 2024 press coverage. Also list any other specialists (neurologist, psychiatrist, paediatrician).
5. **Stats:** the "4 in 10" insomnia figures are the centre's data as reported by Nation and The Standard. Confirm the clinic is happy to publish them.
6. **Old URLs:** confirm the old condition and blog slugs, and add redirects in `vercel.json` / `src/.htaccess` for any that differ.
7. **Reviews:** add real, consented Google reviews. **Social links:** add them to `SOCIALS` in `build.py`.
8. **Privacy policy:** have the clinic or its data protection officer review the template.
9. **Analytics:** paste the GA4 snippet at the marked spot in `<head>`, verify Search Console and submit `sitemap.xml`.
10. **Medical review:** a clinician should review the condition pages before go-live.
11. **Google Business Profile:** make sure it matches the name, address and phones above.
