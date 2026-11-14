#!/usr/bin/env python3
"""Builds the static site for The Sleep Diagnostic & Treatment Centre into ./site.

Every page shares one header, footer and SEO head. Edit the content and the
CLINIC settings below, run `python3 build.py`, and commit the generated files.
"""
import json, shutil, datetime
from pathlib import Path
from html import escape

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "site"
DOMAIN = "https://www.nairobisleepcenter.com"
ASSET_V = "4"  # bump when CSS/JS change so browsers fetch the new file
TODAY = datetime.date.today().isoformat()

# --------------------------------------------------------------- clinic facts
# Contact details from the clinic's company profile (June 2026). Opening hours
# are not in the profile: CONFIRM them (see README).
CLINIC = {
    "name": "The Sleep Diagnostic & Treatment Centre",
    "short": "The Sleep Centre",
    "abbr": "SDTC",
    "street": "10 Mbaazi Avenue",
    "area": "Lavington",
    "city": "Nairobi",
    "country": "KE",
    "phone": "+254 780 587 851",
    "tel": "+254780587851",
    "phone2": "+254 768 824 184",
    "tel2": "+254768824184",
    "whatsapp": "254780587851",
    "email": "admin@nairobisleepcenter.com",
    "pobox": "P.O. Box 29740 – 00202, Nairobi, Kenya",
    "licence": "016750",
    "tagline": "Better Sleep for Better Health",
    "maps": "https://www.google.com/maps/search/?api=1&query=Sleep+Diagnostic+and+Treatment+Centre+Mbaazi+Avenue+Lavington+Nairobi",
    "map_embed": "https://www.google.com/maps?q=Mbaazi+Avenue+Lavington+Nairobi&output=embed",
    "founded": "2018",
}
HOURS = [("Monday to Saturday", "8:00 am – 5:00 pm"), ("Sunday & public holidays", "Closed")]
HOURS_SCHEMA = [{"@type": "OpeningHoursSpecification",
                 "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                 "opens": "08:00", "closes": "17:00"}]
STUDY_HOURS = "Overnight sleep studies run by appointment: you check in in the evening and go home the next morning."
SOCIALS = [  # (label, url) — add the real profile links; empty list hides the icons
]
FAMILY = [("Nairobi ENT Clinic", "https://nairobientclinic.com", "ear, nose & throat"),
          ("Klear Hearing & Balance Centre", "https://klearhbc.com", "hearing & balance")]

# --------------------------------------------------------------- icons
def ic(body, sw="1.8"):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>'

I = {
    "arrow": ic('<path d="M5 12h14M13 6l6 6-6 6"/>', "2.2"),
    "phone": ic('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>'),
    "cal": ic('<rect x="3" y="4.5" width="18" height="17" rx="3"/><path d="M16 2.5v4M8 2.5v4M3 10h18"/>'),
    "pin": ic('<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>'),
    "clock": ic('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
    "mail": ic('<rect x="3" y="5" width="18" height="14" rx="3"/><path d="m4 7 8 6 8-6"/>'),
    "moon": ic('<path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a7 7 0 0 0 10.5 10.5z"/>'),
    "snore": ic('<path d="M4 15c2-3 4-3 6 0s4 3 6 0 3-3 4-1"/><path d="M7 9h4l-4 4h4M14 5h3l-3 3h3"/>'),
    "eye": ic('<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>'),
    "bolt": ic('<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>'),
    "jerk": ic('<path d="M2 16h3l2-8 3 12 2-6 2 4 2-10 2 8h4"/>'),
    "legs": ic('<path d="M9 3v7l-2 11M15 3v7l2 11M9 10h6"/><path d="M3 18c1.2-.8 2-.8 3 0M18 18c1.2-.8 2-.8 3 0"/>'),
    "pulse": ic('<path d="M3 12h4l2-5 4 10 2-5h6"/>'),
    "lab": ic('<path d="M3 18V8M21 18v-4a3 3 0 0 0-3-3h-8v7"/><path d="M3 14h18M7 11.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z"/>'),
    "mask": ic('<path d="M12 4c-4 0-7 3.5-7 8 0 3 2 6 7 6s7-3 7-6c0-4.5-3-8-7-8z"/><path d="M12 18v3M8 21h8M9 11h6"/>'),
    "brain": ic('<path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 2 5 3 3 0 0 0 6 1V6a2 2 0 0 0-3-2zM15 4a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-2 5 3 3 0 0 1-6 1"/>'),
    "nose": ic('<path d="M12 3c-1 4-4 8-4 12a4 4 0 0 0 8 0c0-4-3-8-4-12z"/><path d="M9 17h.01M15 17h.01"/>'),
    "team": ic('<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14.2c2.8.3 5 2.6 5 5.8"/>'),
    "shield": ic('<path d="M12 3 4 6v6c0 5 3.4 8.4 8 9 4.6-.6 8-4 8-9V6z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>'),
    "book": ic('<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 21V5M8 7h7"/>'),
    "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.7-.8-2-.9-.3-.1-.5-.1-.7.1-.2.3-.8.9-.9 1.1-.2.2-.3.2-.6.1-.3-.1-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2 3.1 4.9 4.3.7.3 1.2.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.7-.7 1.9-1.4.2-.7.2-1.2.2-1.4-.1-.1-.3-.2-.6-.3zM12 21.5c-1.7 0-3.4-.5-4.8-1.3l-.3-.2-3.6.9 1-3.5-.2-.4A9.4 9.4 0 0 1 2.6 12C2.6 6.8 6.8 2.6 12 2.6S21.4 6.8 21.4 12 17.2 21.5 12 21.5zM12 .8C5.8.8.8 5.8.8 12c0 2 .5 3.9 1.5 5.6L.7 23.3l5.9-1.5c1.6.9 3.5 1.4 5.4 1.4 6.2 0 11.2-5 11.2-11.2S18.2.8 12 .8z"/></svg>',
}


def wa_link(text="Hello, I'd like to ask about a sleep assessment."):
    from urllib.parse import quote
    return f"https://wa.me/{CLINIC['whatsapp']}?text={quote(text)}"

# --------------------------------------------------------------- content
CONDITIONS = [
    {"slug": "obstructive-sleep-apnoea", "name": "Obstructive sleep apnoea", "icon": "pulse",
     "short": "Breathing that stops and starts through the night, leaving you exhausted and straining your heart.",
     "title": "Obstructive Sleep Apnoea Diagnosis & Treatment in Nairobi",
     "desc": "Loud snoring, gasping and daytime exhaustion can mean sleep apnoea. Get an overnight sleep study and CPAP treatment in Nairobi. Book today.",
     "h1": "Obstructive sleep apnoea: <em>diagnosis and treatment</em>",
     "lead": "Sleep apnoea is one of the most common sleep disorders we see, and one of the most treatable once it has been properly measured.",
     "body": """
<h2>What is obstructive sleep apnoea?</h2>
<p>In obstructive sleep apnoea (OSA) the soft tissues at the back of the throat relax and narrow the airway while you sleep. Breathing becomes shallow (a <strong>hypopnoea</strong>) or stops altogether for ten seconds or more (an <strong>apnoea</strong>). Each time, oxygen levels dip and the brain briefly wakes you to restart breathing. Most people never remember these arousals, but they can happen dozens of times an hour, all night.</p>
<h2>Symptoms</h2>
<ul>
<li>Loud, habitual snoring, often with pauses, snorts or gasps</li>
<li>A partner noticing that you stop breathing</li>
<li>Waking unrefreshed, however long you slept</li>
<li>Falling asleep in meetings, in traffic or in front of the TV</li>
<li>Morning headaches, a dry mouth or sore throat</li>
<li>Waking at night to pass urine</li>
<li>Poor concentration, irritability or low mood</li>
</ul>
<h2>Who is at risk?</h2>
<p>OSA is more common in men, after middle age, and in people carrying extra weight around the neck and middle, but slim and young people get it too. Large tonsils, a narrow jaw, nasal blockage, alcohol or sedatives at night and a family history all raise the risk. In children, enlarged tonsils and adenoids are the usual cause.</p>
<div class="callout warn"><p><b>Why it matters.</b> Untreated sleep apnoea is linked to high blood pressure, heart rhythm problems, heart attack, stroke and type 2 diabetes, and drowsy driving is a serious road risk. If you are falling asleep at the wheel, please do not drive until you have been assessed.</p></div>
<h2>How we diagnose it</h2>
<p>The gold-standard test is an overnight <a href="/sleep-study-polysomnography/">sleep study (polysomnography)</a> in our sleep laboratory. Sensors record your breathing, oxygen levels, heart rhythm, brain activity and body position while you sleep, and a sleep technician watches over you all night. The result is your <strong>apnoea–hypopnoea index (AHI)</strong>: the number of breathing events per hour of sleep.</p>
<table><thead><tr><th>AHI (events per hour)</th><th>Severity in adults</th></tr></thead><tbody>
<tr><td>Fewer than 5</td><td>Within the normal range</td></tr><tr><td>5 to 14</td><td>Mild</td></tr><tr><td>15 to 29</td><td>Moderate</td></tr><tr><td>30 or more</td><td>Severe</td></tr></tbody></table>
<h2>Treatment</h2>
<p>Your treatment plan depends on the severity and the cause. It may include:</p>
<ul>
<li><strong>CPAP therapy</strong>, the first-line treatment for moderate and severe OSA. A quiet machine delivers gentle air pressure through a mask to hold the airway open. We help you choose the right <a href="/cpap-equipment/">machine and mask</a>, and follow up until it feels comfortable.</li>
<li><strong>Airway and ENT treatment</strong> where a blockage is the cause, such as nasal obstruction or enlarged tonsils, with our colleagues at Nairobi ENT Clinic.</li>
<li><strong>Positional therapy</strong> if your apnoea happens mainly when you sleep on your back.</li>
<li><strong>Weight management</strong>, reducing alcohol near bedtime, and reviewing sedating medicines.</li>
<li><strong>Oral appliances</strong> that bring the lower jaw forward, for some people with mild to moderate OSA.</li>
</ul>
""",
     "faqs": [("Is snoring always sleep apnoea?", "No. Many people snore without apnoea. But snoring with pauses, gasping or daytime sleepiness should be checked with a sleep study."),
              ("Will I have to use CPAP forever?", "CPAP controls sleep apnoea rather than curing it, so most people use it long term. If the cause changes, for example after significant weight loss or airway surgery, a repeat sleep study can show whether you still need it."),
              ("Can children have sleep apnoea?", "Yes. Children who snore most nights, breathe through their mouth or sleep restlessly should be assessed. Enlarged tonsils and adenoids are a common, treatable cause.")]},
    {"slug": "snoring", "name": "Snoring", "icon": "snore",
     "short": "More than a noise problem. We find out where it comes from and whether it is hiding sleep apnoea.",
     "title": "Snoring Treatment in Nairobi | Find the Cause",
     "desc": "Find out why you snore and whether it is sleep apnoea. Specialist snoring assessment, sleep studies and treatment in Nairobi. Book an appointment.",
     "h1": "Snoring: <em>find the cause,</em> then fix it",
     "lead": "Snoring keeps partners awake and is sometimes the first sign of sleep apnoea. A proper assessment tells you which kind you have.",
     "body": """
<h2>Why do people snore?</h2>
<p>Snoring is the sound of soft tissue vibrating as air squeezes through a narrowed airway during sleep. The narrowing can come from the nose (a deviated septum, allergies or polyps), the throat (large tonsils, a long soft palate or a bulky tongue), or simply from muscles relaxing more during deep sleep, after alcohol or with weight gain.</p>
<h2>Simple snoring or sleep apnoea?</h2>
<p>Many people snore without any harm to their health. The concern is when snoring comes with breathing pauses. Book an assessment if your snoring comes with any of these:</p>
<ul>
<li>Pauses in breathing, choking or gasping, noticed by a partner</li>
<li>Daytime sleepiness, or nodding off when driving</li>
<li>Morning headaches or waking unrefreshed</li>
<li>High blood pressure that is hard to control</li>
<li>Snoring in a child, especially with mouth breathing or restless sleep</li>
</ul>
<h2>How we assess snoring</h2>
<p>We start with a consultation and an examination of the nose and throat to see where the narrowing is. If there is any suggestion of <a href="/obstructive-sleep-apnoea/">sleep apnoea</a>, an overnight <a href="/sleep-study-polysomnography/">sleep study</a> measures exactly what happens to your breathing and oxygen levels while you sleep.</p>
<h2>Treatment options</h2>
<ul>
<li><strong>Lifestyle changes:</strong> weight loss, avoiding alcohol in the evening, and sleeping on your side often make a real difference.</li>
<li><strong>Treating the nose:</strong> managing allergies or nasal blockage, or ENT surgery where there is a structural cause.</li>
<li><strong>Oral appliances</strong> that hold the jaw forward during sleep.</li>
<li><strong>CPAP</strong> if snoring turns out to be sleep apnoea.</li>
</ul>
<p>Be wary of anti-snoring sprays and gadgets bought before you know the cause: they can quieten the noise while a breathing problem carries on underneath.</p>
""",
     "faqs": [("My partner says I snore but I feel fine. Should I worry?", "Not necessarily, but ask your partner whether you stop breathing or gasp. If you do, or if you are often tired in the day, get assessed."),
              ("Can snoring be cured?", "Often it can be greatly reduced once the cause is clear, whether that is nasal blockage, weight, sleeping position or the shape of the airway.")]},
    {"slug": "insomnia", "name": "Insomnia", "icon": "eye",
     "short": "Lying awake, waking at 3 am, or never feeling rested. Treatment that works without relying on sleeping pills.",
     "title": "Insomnia Treatment in Nairobi | CBT-I & Sleep Specialists",
     "desc": "Trouble falling or staying asleep? Specialist insomnia assessment and treatment in Nairobi, including CBT for insomnia. Book an appointment today.",
     "h1": "Insomnia: <em>sleep again,</em> without depending on pills",
     "lead": "Insomnia is the most common reason people come to our centre. It is real, it is exhausting, and it responds well to the right treatment.",
     "body": """
<h2>What counts as insomnia?</h2>
<p>Insomnia means having trouble falling asleep, staying asleep, or waking too early and being unable to get back to sleep, even though you have the chance to sleep, and feeling the effects during the day. A few bad nights during a stressful week is normal. When it happens at least three nights a week for three months or more, it is called <strong>chronic insomnia</strong>.</p>
<h2>Common signs</h2>
<ul>
<li>Taking more than half an hour to fall asleep</li>
<li>Waking in the night and lying awake for long periods</li>
<li>Waking much earlier than you want to</li>
<li>Daytime tiredness, poor concentration, irritability or low mood</li>
<li>Worrying about sleep, and dreading bedtime</li>
</ul>
<h2>What causes it?</h2>
<p>Insomnia often starts with a trigger such as stress, bereavement, illness, shift work, a new baby or travel, and then carries on because of habits and worry that build up around sleep. It can also be linked to anxiety and depression, pain, menopause, some medicines, caffeine and alcohol, or another sleep disorder such as <a href="/obstructive-sleep-apnoea/">sleep apnoea</a> or <a href="/restless-leg-syndrome/">restless legs</a>. Finding these contributors is part of your assessment.</p>
<h2>How we help</h2>
<ul>
<li><strong>A full sleep assessment</strong> covering your sleep pattern, health, medicines and mood. You may be asked to keep a sleep diary for one to two weeks.</li>
<li><strong>Cognitive behavioural therapy for insomnia (CBT-I)</strong>, the recommended first treatment for chronic insomnia. It is a structured programme with our psychology team that resets your sleep pattern and the thoughts that keep you awake.</li>
<li><strong>Psychology and psychiatry support</strong> where anxiety, depression or trauma are part of the picture.</li>
<li><strong>Careful use of medicines</strong> where appropriate, usually for the short term and alongside CBT-I rather than instead of it.</li>
<li><strong>A sleep study</strong> if we suspect another sleep disorder is breaking up your sleep.</li>
</ul>
<div class="callout"><p><b>Tonight:</b> keep a fixed wake-up time, even after a bad night; get out of bed if you have been awake for a long time and return when sleepy; and keep caffeine to the morning. These habits support treatment, but persistent insomnia deserves a proper assessment.</p></div>
""",
     "faqs": [("Do I need a sleep study for insomnia?", "Not always. Insomnia is usually diagnosed from your history and a sleep diary. We recommend a sleep study when another condition, such as sleep apnoea or limb movements, may be disturbing your sleep."),
              ("How long does CBT-I take?", "Most programmes run over about four to eight sessions. Many people notice their sleep improving within the first few weeks."),
              ("Are sleeping pills a good long-term answer?", "For most people, no. They can help in the short term, but CBT-I gives longer-lasting results without the risk of dependence.")]},
    {"slug": "narcolepsy", "name": "Narcolepsy", "icon": "bolt",
     "short": "Overwhelming daytime sleepiness and sudden sleep attacks, properly investigated and managed.",
     "title": "Narcolepsy Diagnosis in Nairobi | Sleep Specialists",
     "desc": "Overwhelming daytime sleepiness, sleep attacks or cataplexy? Specialist narcolepsy assessment and sleep testing in Nairobi. Book an appointment.",
     "h1": "Narcolepsy: <em>when sleep</em> takes over the day",
     "lead": "Narcolepsy is a lifelong neurological condition that is often missed for years. The right tests give a clear answer and a way forward.",
     "body": """
<h2>What is narcolepsy?</h2>
<p>Narcolepsy is a disorder of the brain's control of sleep and wakefulness. The boundaries between being awake, deep sleep and dreaming (REM) sleep become blurred, so sleep can break into the day and dream-like experiences can happen while you are awake. It often begins in the teens or twenties, and is frequently mistaken for laziness, depression or simply being tired.</p>
<h2>Symptoms</h2>
<ul>
<li><strong>Excessive daytime sleepiness:</strong> a constant, overwhelming need to sleep, with sudden "sleep attacks" even in the middle of activities</li>
<li><strong>Cataplexy:</strong> sudden, brief muscle weakness triggered by strong emotion such as laughter, from drooping eyelids or a sagging jaw to buckling knees (this occurs in type 1 narcolepsy)</li>
<li><strong>Sleep paralysis:</strong> being briefly unable to move or speak when falling asleep or waking</li>
<li><strong>Vivid hallucinations</strong> as you fall asleep or wake up</li>
<li><strong>Broken night-time sleep</strong>, despite the daytime sleepiness</li>
</ul>
<h2>How it is diagnosed</h2>
<p>Diagnosis needs a careful history and specialist sleep testing. This usually means an overnight <a href="/sleep-study-polysomnography/">sleep study</a> to rule out other causes of sleepiness, such as sleep apnoea, followed by a daytime nap test (the multiple sleep latency test, or MSLT) that measures how quickly you fall asleep and whether you go straight into REM sleep. We will explain which tests you need and how to prepare, including any medicines to pause beforehand.</p>
<h2>Living with narcolepsy</h2>
<p>There is no cure yet, but treatment controls symptoms well for most people. It usually combines medicines that improve alertness or reduce cataplexy with planned short naps, regular sleep times, and practical support for work, study and driving safety.</p>
""",
     "faqs": [("Is narcolepsy the same as being very tired?", "No. Many conditions cause tiredness. Narcolepsy is a specific neurological disorder, diagnosed with sleep testing."),
              ("Can I drive if I have narcolepsy?", "Not while your sleepiness is uncontrolled. Talk to your specialist about when driving is safe once treatment is working.")]},
    {"slug": "restless-leg-syndrome", "name": "Restless legs syndrome", "icon": "legs",
     "short": "An irresistible urge to move your legs in the evening that keeps you from falling asleep.",
     "title": "Restless Legs Syndrome Treatment in Nairobi",
     "desc": "An urge to move your legs at night that stops you sleeping? Get restless legs syndrome assessed and treated by sleep specialists in Nairobi.",
     "h1": "Restless legs syndrome: <em>calm legs,</em> better sleep",
     "lead": "Restless legs syndrome (RLS), also called Willis–Ekbom disease, is common, under-recognised and very treatable.",
     "body": """
<h2>What does it feel like?</h2>
<p>People describe crawling, pulling, tingling, aching or "fizzy" feelings deep in the legs, with an urge to move them that is hard to resist. The four features that define RLS are:</p>
<ol>
<li>An urge to move the legs, usually with uncomfortable sensations</li>
<li>It starts or gets worse when you are resting, sitting or lying down</li>
<li>Moving, stretching or walking relieves it, at least while you keep moving</li>
<li>It is worse in the evening and at night</li>
</ol>
<p>Because it peaks at bedtime, RLS often makes it hard to fall asleep, and many people with RLS also have <a href="/periodic-limb-movement-disorder/">periodic limb movements</a> during sleep.</p>
<h2>What causes it?</h2>
<p>Often there is no single cause and it runs in families. It is linked to <strong>low iron stores</strong>, pregnancy, kidney disease and nerve damage, and can be triggered or worsened by some antidepressants, antihistamines and anti-sickness medicines, as well as caffeine, alcohol and nicotine.</p>
<h2>Assessment and treatment</h2>
<ul>
<li>A consultation to confirm the diagnosis and rule out conditions that feel similar, such as cramps or nerve pain</li>
<li><strong>Blood tests</strong>, including iron stores (ferritin), since iron replacement alone can ease symptoms when levels are low</li>
<li>A review of your medicines and habits</li>
<li>Stretching, warm baths, massage and a regular sleep routine</li>
<li>Prescription treatment for moderate to severe symptoms, chosen carefully and monitored over time</li>
<li>A <a href="/sleep-study-polysomnography/">sleep study</a> if we need to measure limb movements or check for another sleep disorder</li>
</ul>
""",
     "faqs": [("Is restless legs syndrome serious?", "It is not dangerous in itself, but the sleep loss it causes affects mood, concentration and quality of life, so it is worth treating."),
              ("I'm pregnant and have restless legs. Is that common?", "Yes, it is common in later pregnancy and usually settles after delivery. Talk to us or your obstetrician before taking any treatment, including iron.")]},
    {"slug": "periodic-limb-movement-disorder", "name": "Periodic limb movement disorder", "icon": "jerk",
     "short": "Repeated jerks of the legs during sleep that break up your rest, often without you knowing.",
     "title": "Periodic Limb Movement Disorder (PLMD) | Nairobi Sleep Centre",
     "desc": "Repetitive leg jerks during sleep can leave you exhausted. PLMD is diagnosed with an overnight sleep study. Specialist assessment in Nairobi.",
     "h1": "Periodic limb movement disorder <em>(PLMD)</em>",
     "lead": "Repeated leg movements during sleep can fragment your rest without you ever knowing. A sleep study is the only way to see them.",
     "body": """
<h2>What is PLMD?</h2>
<p>Periodic limb movements are repetitive twitches or jerks, usually of the legs, that happen every 20 to 40 seconds during sleep, often in clusters lasting minutes to hours. The big toe may extend, and the ankle, knee and hip may bend. When these movements are frequent and they disturb sleep or cause daytime problems that nothing else explains, this is <strong>periodic limb movement disorder</strong>.</p>
<h2>Signs to look out for</h2>
<ul>
<li>Unrefreshing sleep and daytime tiredness with no obvious reason</li>
<li>A bed partner complaining of being kicked</li>
<li>Tangled or kicked-off bedclothes in the morning</li>
<li>Waking often in the night</li>
</ul>
<p>Most people with PLMD are unaware of the movements. They are common in people with <a href="/restless-leg-syndrome/">restless legs syndrome</a>, and are also seen with sleep apnoea, narcolepsy, low iron, kidney disease and some antidepressants.</p>
<h2>Diagnosis</h2>
<p>PLMD can only be diagnosed with an overnight <a href="/sleep-study-polysomnography/">sleep study</a>. Sensors on the shins count the movements per hour and show whether they wake the brain. The study also checks for sleep apnoea, which can trigger similar leg movements, since treating the apnoea often settles them.</p>
<h2>Treatment</h2>
<ul>
<li>Checking and correcting iron levels</li>
<li>Reviewing medicines that can make movements worse</li>
<li>Treating any underlying sleep disorder, such as sleep apnoea</li>
<li>Good sleep habits, and less caffeine and alcohol</li>
<li>Medication when movements clearly disturb sleep and other steps have not helped</li>
</ul>
""",
     "faqs": [("How is PLMD different from restless legs?", "Restless legs is an urge to move felt while you are awake, mostly in the evening. PLMD is movement that happens while you are asleep. Many people have both."),
              ("Do I need treatment if I have the movements but feel fine?", "Not usually. Treatment is for movements that disrupt your sleep or your daytime functioning.")]},
]

STUDY_FAQS = [
    ("Does a sleep study hurt?", "No. The sensors are stuck to the skin with gentle tape or paste, with a soft band around the chest and a small sensor on a fingertip. Nothing pierces the skin."),
    ("What if I can't sleep with the sensors on?", "Almost everyone sleeps enough for a useful result. We need a few hours of sleep, not a perfect night. The room is private and quiet, and you can use the bathroom during the night."),
    ("How much does a sleep study cost, and does insurance cover it?", "Call or WhatsApp us for the current price. Many medical insurers cover sleep studies with a doctor's referral, and we can help you check your cover and get pre-authorisation before your night."),
    ("Do I need a referral?", "You can book a consultation directly. Some insurers ask for a doctor's referral for the sleep study itself, so check with your insurer or ask us."),
    ("Can my child have a sleep study?", "Children who snore, stop breathing or sleep very restlessly can be assessed. Call us to arrange the right appointment for your child's age; a parent stays with the child overnight."),
    ("When will I get my results?", "Several hours of recording have to be analysed and reported by a specialist, so results are not ready the same morning. We will book a review appointment to go through the report and your treatment options with you."),
]

GENERAL_FAQS = [
    ("Do I need a doctor's referral to book?", "No. You can book a consultation or sleep assessment with us directly. If you have a referral letter or earlier test results, please bring them."),
    ("Where are you located?", f"We are at {CLINIC['street']}, {CLINIC['area']}, {CLINIC['city']}. Call us on {CLINIC['phone']} if you need directions."),
    ("What are your opening hours?", f"The clinic is open {HOURS[0][0].lower()}, {HOURS[0][1]}. {STUDY_HOURS}"),
    ("Do you accept medical insurance?", "Many insurers cover consultations and sleep studies. Contact us with your insurer's name and we will help you check your cover and any pre-authorisation needed."),
    ("Do you see children?", "Yes. Snoring, breathing pauses and restless sleep in children should always be assessed. Call us so we can book the right appointment for your child's age."),
    ("Do you sell or rent CPAP machines?", "We supply CPAP machines, masks and accessories, and set them up and follow you up after fitting. Ask us about current models, prices and rental options."),
]
GENERAL_FAQS = STUDY_FAQS[:3] + GENERAL_FAQS

FOUNDERS = [
    {"name": "Prof. Muthure Macharia", "role": "Co-founder · ENT surgeon", "init": "MM",
     "bio": "Ear, nose and throat surgeon and co-founder of the centre."},
    {"name": "Dr Chimmy Omamo-Olende", "role": "Co-founder · ENT surgeon", "init": "CO",
     "bio": "Ear, nose and throat surgeon and co-founder of the centre."},
    {"name": "Dr Samuel M. Nyagah", "role": "Co-founder · ENT surgeon", "init": "SN",
     "bio": "Ear, nose and throat surgeon who treats sleep disorders, with a focus on snoring, sleep apnoea and the airway."},
]
TEAM = FOUNDERS + [
    {"name": "Dr Caroline Muturi", "role": "Specialist doctor", "init": "CM",
     "bio": "Part of the medical team assessing patients with sleep problems and planning their treatment."},
    {"name": "Margaret Karani", "role": "Clinical psychologist", "init": "MK",
     "bio": "Leads psychological care for insomnia and the emotional side of poor sleep, including CBT for insomnia."},
    {"name": "Peter Kamau", "role": "Sleep technologist", "init": "PK",
     "bio": "Sets up and monitors overnight sleep studies, and makes sure every patient is comfortable through the night."},
]

EQUIPMENT = [
    ("CPAP machines", "mask", "Fixed-pressure machines for sleep apnoea, set to the pressure your sleep study shows you need."),
    ("Auto-adjusting CPAP (APAP)", "pulse", "Machines that adjust the pressure breath by breath through the night, often more comfortable to start on."),
    ("BiPAP machines", "lab", "Two-level pressure for people who need more support or find CPAP hard to breathe out against."),
    ("Masks and cushions", "mask", "Nasal, pillow and full-face masks. Fit matters more than anything else, so we fit them in person."),
    ("Humidifiers and tubing", "moon", "Heated humidifiers and tubing to stop dryness and a blocked nose."),
    ("Filters and spares", "shield", "Replacement filters, cushions and headgear to keep your therapy clean and comfortable."),
]

# --------------------------------------------------------------- hypnogram
def hypnogram():
    seq = [(0,10),(2,8),(3,20),(4,35),(3,12),(1,10),(0,3),(2,5),(3,25),(4,25),(3,15),(1,18),
           (2,5),(3,30),(4,12),(3,18),(1,25),(0,4),(2,6),(3,40),(1,30),(0,3),(2,5),(3,35),(1,28),(0,6)]
    total = sum(m for _, m in seq)
    x0, w, ys = 48, 512, [20, 50, 80, 110, 140]
    def X(t): return round(x0 + t / total * w, 1)
    t, d, rem = 0, [], []
    for i, (s, m) in enumerate(seq):
        d.append(("M" if i == 0 else "L") + f"{X(t)},{ys[s]}")
        d.append(f"L{X(t+m)},{ys[s]}")
        if s == 1: rem.append(f'<rect class="rem" x="{X(t)}" y="38" width="{round(X(t+m)-X(t),1)}" height="24" rx="4"/>')
        t += m
    labels = "".join(f'<text class="lbl" x="0" y="{y+3.5}">{n}</text>' for n, y in zip(["WAKE", "REM", "N1", "N2", "N3"], ys))
    grid = "".join(f'<line x1="{x0}" x2="{x0+w}" y1="{y}" y2="{y}"/>' for y in ys)
    hrs = "".join(f'<text class="lbl" x="{X(i*total/4)-12}" y="208">{h}</text>' for i, h in enumerate(["22:30", "00:20", "02:10", "04:00", "05:50"]))
    import math
    pts = []
    for k in range(0, 121):
        tt = k / 120
        dip = sum(6 * math.exp(-((tt - c) ** 2) / 0.00025) for c in [.12, .3, .33, .55, .58, .74, .9])
        pts.append(f"{round(x0 + tt*w,1)},{round(172 + dip - 4*math.sin(k*1.7)*0.2,1)}")
    spo2 = '<polyline class="spo2" points="' + " ".join(pts) + '"/>'
    return f'''<svg class="hypno" viewBox="0 0 570 214" role="img" aria-label="Illustration of a hypnogram: sleep stages moving through about five cycles across one night, with an oxygen trace below.">
<defs><linearGradient id="hg" x1="0" x2="1"><stop offset="0" stop-color="#d6c3e8"/><stop offset=".55" stop-color="#ffffff"/><stop offset="1" stop-color="#74d9a6"/></linearGradient></defs>
<g class="grid">{grid}</g>{"".join(rem)}{labels}
<path class="trace" d="{"".join(d)}"/>
<text class="lbl" x="0" y="178">SpO₂</text>{spo2}{hrs}</svg>'''

# --------------------------------------------------------------- layout
NAV = [("/conditions/", "Conditions"), ("/sleep-study-polysomnography/", "Sleep study"),
       ("/cpap-equipment/", "CPAP & equipment"), ("/about-us/", "About"), ("/faqs/", "FAQs"), ("/contact-us/", "Contact")]


def org_schema():
    s = {"@context": "https://schema.org", "@type": ["MedicalClinic", "MedicalBusiness"], "@id": DOMAIN + "/#clinic",
         "name": CLINIC["name"], "alternateName": [CLINIC["short"], "Nairobi Sleep Center", CLINIC["abbr"]],
         "url": DOMAIN + "/", "logo": DOMAIN + "/assets/img/logo.png", "image": DOMAIN + "/assets/img/og.png",
         "telephone": CLINIC["tel"], "foundingDate": CLINIC["founded"], "priceRange": "KES", "slogan": CLINIC["tagline"],
         "founder": [{"@type": "Person", "name": f["name"], "jobTitle": "ENT surgeon"} for f in FOUNDERS],
         "contactPoint": [{"@type": "ContactPoint", "telephone": t, "contactType": "appointments", "areaServed": "KE"} for t in (CLINIC["tel"], CLINIC["tel2"])],
         "medicalSpecialty": ["SleepMedicine", "Otolaryngologic", "Psychiatric"],
         "address": {"@type": "PostalAddress", "streetAddress": CLINIC["street"], "addressLocality": f"{CLINIC['area']}, {CLINIC['city']}",
                     "addressRegion": "Nairobi", "addressCountry": CLINIC["country"]},
         "openingHoursSpecification": HOURS_SCHEMA, "hasMap": CLINIC["maps"],
         "availableService": [{"@type": "MedicalTest", "name": "Polysomnography (overnight sleep study)"},
                              {"@type": "MedicalTherapy", "name": "CPAP therapy"},
                              {"@type": "MedicalTherapy", "name": "Cognitive behavioural therapy for insomnia (CBT-I)"}],
         "parentOrganization": {"@type": "MedicalOrganization", "name": "Nairobi ENT Clinic", "url": "https://nairobientclinic.com"}}
    if CLINIC["email"]: s["email"] = CLINIC["email"]
    if SOCIALS: s["sameAs"] = [u for _, u in SOCIALS]
    return s


def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def crumbs_schema(crumbs):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + u} for i, (n, u) in enumerate(crumbs)]}


def head(path, title, desc, schema):
    url = DOMAIN + path
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schema)
    return f'''<!doctype html>
<html lang="en-KE" class="js-off">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#764c8c">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/assets/img/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/fraunces-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/manrope-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_V}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{escape(CLINIC['name'])}">
<meta property="og:locale" content="en_KE">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/assets/img/og.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<!-- GA4: paste the measurement snippet here before launch -->
{ld}
</head>'''


def header(path):
    items = "".join(f'<li><a href="{u}"{" aria-current=\"page\"" if path.startswith(u) else ""}>{n}</a></li>' for u, n in NAV)
    return f'''<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
 <div class="wrap nav">
  <a class="brand" href="/"><img src="/assets/img/logo.svg" width="126" height="66" alt="The Sleep Diagnostic and Treatment Center, home"></a>
  <nav aria-label="Main"><ul class="menu" id="menu">{items}<li class="menu-book"><a href="/book-appointment/">Book a sleep study</a></li></ul></nav>
  <div class="nav-cta">
   <a class="nav-phone" href="tel:{CLINIC['tel']}">{I['phone']}{CLINIC['phone']}</a>
   <a class="btn moon sm" href="/book-appointment/">Book a sleep study</a>
   <button class="menu-btn" aria-controls="menu" aria-expanded="false" aria-label="Menu"><span></span></button>
  </div>
 </div>
</header>
<main id="main">'''


def footer():
    hours = "".join(f"<li>{d}: <span style='color:#fff'>{h}</span></li>" for d, h in HOURS)
    socials = ""
    if SOCIALS:
        socials = '<div class="socials">' + "".join(f'<a href="{u}" rel="noopener" target="_blank" aria-label="{l}">{I["arrow"]}</a>' for l, u in SOCIALS) + "</div>"
    fam = " · ".join(f'<a href="{u}" rel="noopener">{n}</a>' for n, u, _ in FAMILY)
    email = f'<li><a href="mailto:{CLINIC["email"]}">{CLINIC["email"]}</a></li>' if CLINIC["email"] else ""
    conds = "".join(f'<li><a href="/{c["slug"]}/">{c["name"]}</a></li>' for c in CONDITIONS)
    return f'''</main>
<footer class="site-footer">
 <div class="wrap foot-grid">
  <div>
   <a class="brand brand-foot" href="/"><img src="/assets/img/logo-reverse.svg" width="210" height="110" alt="The Sleep Diagnostic and Treatment Center: Better Sleep for Better Health" loading="lazy"></a>
   <p>A specialist sleep laboratory and clinic in Nairobi, diagnosing and treating sleep apnoea, snoring, insomnia and other sleep disorders since {CLINIC['founded']}. Founded by ENT surgeons.</p>
   <p class="licence">Licensed by the Medical Practitioners and Dentists Board · Licence No. {CLINIC['licence']}</p>
   {socials}
   <p class="family">Part of the Nairobi ENT family: {fam}</p>
  </div>
  <div><h3>Conditions</h3><ul>{conds}<li><a href="/what-is-sleep/">What is sleep?</a></li></ul></div>
  <div><h3>Patients</h3><ul><li><a href="/sleep-study-polysomnography/">Sleep study</a></li><li><a href="/cpap-equipment/">CPAP &amp; equipment</a></li><li><a href="/book-appointment/">Book an appointment</a></li><li><a href="/our-team/">Our team</a></li><li><a href="/about-us/">About us</a></li><li><a href="/faqs/">FAQs</a></li></ul></div>
  <div><h3>Visit &amp; contact</h3><ul>
   <li><a href="{CLINIC['maps']}" rel="noopener" target="_blank">{CLINIC['street']}, {CLINIC['area']}, {CLINIC['city']}</a></li>
   <li><a href="tel:{CLINIC['tel']}">{CLINIC['phone']}</a> · <a href="tel:{CLINIC['tel2']}">{CLINIC['phone2']}</a></li>
   <li><a href="{wa_link()}" rel="noopener" target="_blank">WhatsApp us</a></li>{email}
   {hours}<li>{CLINIC['pobox']}</li></ul></div>
 </div>
 <div class="wrap foot-base"><span>© <span data-year>{datetime.date.today().year}</span> {CLINIC['name']}. Information on this site is general and does not replace a consultation.</span><span><a href="/privacy-policy/">Privacy policy</a> · <a href="/contact-us/">Contact</a></span></div>
</footer>
<a class="wa-float" href="{wa_link()}" target="_blank" rel="noopener" aria-label="Chat with us on WhatsApp">{I['wa']}</a>
<nav class="mbar" aria-label="Quick contact"><a href="tel:{CLINIC['tel']}">{I['phone']}Call</a><a href="{wa_link()}" target="_blank" rel="noopener">{I['wa']}WhatsApp</a><a class="go" href="/book-appointment/">{I['cal']}Book</a></nav>
<script src="/assets/js/site.js?v={ASSET_V}" defer></script>
</body>
</html>'''


PAGES = []  # (path, priority)

def write(path, title, desc, body, schema=(), crumbs=None, priority="0.7"):
    schema = list(schema)
    if crumbs: schema.append(crumbs_schema(crumbs))
    html = head(path, title, desc, schema) + "\n" + header(path) + body + footer()
    dest = OUT / path.strip("/") / "index.html" if path != "/" else OUT / "index.html"
    if path == "/404/": dest = OUT / "404.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8")
    assert len(title) <= 65, (path, len(title), title)
    assert len(desc) <= 160, (path, len(desc))
    if path != "/404/": PAGES.append((path, priority))


def page_hero(crumbs, h1, lead, ctas=True, eyebrow=""):
    cl = "".join(f'<li><a href="{u}">{escape(n)}</a></li>' if i < len(crumbs) - 1 else f'<li aria-current="page">{escape(n)}</li>' for i, (n, u) in enumerate(crumbs))
    eb = f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else ""
    c = f'<div class="hero-ctas"><a class="btn moon" href="/book-appointment/">{I["cal"]}Book an appointment</a><a class="btn ghost" href="{wa_link()}" target="_blank" rel="noopener">{I["wa"]}WhatsApp us</a></div>' if ctas else ""
    return f'''<section class="night page-hero"><div class="stars"></div><div class="moon-orb"></div><div class="wrap">
<nav aria-label="Breadcrumb"><ol class="crumbs">{cl}</ol></nav>{eb}<h1>{h1}</h1><p class="lead">{lead}</p>{c}</div></section>'''


def faq_html(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{escape(q)}</summary><div class="a"><p>{escape(a)}</p></div></details>' for q, a in faqs) + "</div>"


def cta_band(title="Ready for a <em>better night?</em>", text="Book a consultation or an overnight sleep study. Not sure what you need? Send us a WhatsApp and we'll point you in the right direction."):
    return f'''<section class="section tight"><div class="wrap"><div class="night cta-band reveal"><div class="stars"></div>
<div><h2>{title}</h2><p class="lead" style="margin:0">{text}</p></div>
<div class="cta-actions"><a class="btn moon" href="/book-appointment/">{I['cal']}Book an appointment</a><a class="btn ghost" href="tel:{CLINIC['tel']}">{I['phone']}Call {CLINIC['phone']}</a><a class="btn ghost" href="{wa_link()}" target="_blank" rel="noopener">{I['wa']}WhatsApp us</a><p class="cta-meta">{HOURS[0][0]}, {HOURS[0][1]}</p></div></div></div></section>'''


def cond_cards(exclude=None, feature_first=False):
    out = []
    for i, c in enumerate(CONDITIONS):
        if c["slug"] == exclude: continue
        cls = "card feature" if feature_first and i == 0 else "card"
        out.append(f'<a class="{cls} reveal" href="/{c["slug"]}/"><div class="card-icon">{I[c["icon"]]}</div><h3>{c["name"]}</h3><p>{c["short"]}</p><span class="link-arrow">Learn more {I["arrow"]}</span></a>')
    return "".join(out)


def aside(current):
    links = "".join(f'<li><a href="/{c["slug"]}/"{" aria-current=\"page\"" if c["slug"]==current else ""}>{c["name"]}</a></li>' for c in CONDITIONS)
    return f'''<aside class="aside"><div class="book-card"><h3>Book a sleep assessment</h3><p>Talk to a specialist, or go straight to an overnight sleep study.</p>
<a class="btn moon" href="/book-appointment/">{I['cal']}Book now</a><a class="btn ghost" href="tel:{CLINIC['tel']}" style="margin-top:10px">{I['phone']}{CLINIC['phone']}</a><p style="margin:12px 0 0;font-size:.88rem;text-align:center">or {CLINIC['phone2']}</p></div>
<div class="panel"><nav aria-label="Sleep conditions"><h3>Sleep conditions</h3><ul>{links}<li><a href="/what-is-sleep/"{" aria-current=\"page\"" if current=="what-is-sleep" else ""}>What is sleep?</a></li></ul></nav></div></aside>'''

# --------------------------------------------------------------- pages
def home():
    chips = ["Loud snoring", "Gasping or choking at night", "Partner says I stop breathing", "Waking up exhausted",
             "Dozing off while driving", "Morning headaches", "Lying awake for hours", "Waking at 3 am, wide awake",
             "Crawling feelings in my legs", "Sudden sleep attacks in the day"]
    chip_html = "".join(f'<li><button type="button" class="chip" aria-pressed="false">{c}</button></li>' for c in chips)
    body = f'''
<section class="night hero"><div class="stars"></div><div class="moon-orb"></div>
 <div class="wrap hero-grid">
  <div>
   <h1><span class="h1-kicker">Sleep apnoea, snoring &amp; insomnia care in Nairobi</span>Better nights start with <em>answers.</em></h1>
   <p class="lead">A specialist sleep laboratory founded by ENT surgeons, where doctors, psychologists and sleep technologists work out exactly why you are not sleeping well, and then treat it.</p>
   <div class="hero-ctas"><a class="btn moon" href="/book-appointment/">{I['cal']}Book a sleep study</a><a class="btn ghost" href="{wa_link()}" target="_blank" rel="noopener">{I['wa']}WhatsApp us</a></div>
   <ul class="trust"><li>{I['lab']}Overnight lab sleep studies</li><li>{I['team']}Multidisciplinary team</li><li>{I['mask']}CPAP set-up &amp; follow-up</li></ul>
  </div>
  <div class="report reveal" aria-label="Example of what a sleep study measures">
   <div class="report-top"><div><b>One night, fully measured</b><span>Polysomnography · sample report</span></div><span class="tag"><i></i>Monitoring</span></div>
   {hypnogram()}
   <div class="readouts"><div><b>91%</b><span>Sleep efficiency</span></div><div><b>18 /hr</b><span>Breathing pauses (AHI)</span></div><div><b>86%</b><span>Lowest oxygen level</span></div></div>
   <p class="report-note">Illustration for explanation only. Not real patient data.</p>
  </div>
 </div>
</section>

<section class="section"><div class="wrap checker">
 <div class="reveal"><p class="eyebrow">Quick check</p><h2>Does any of this <em>sound familiar?</em></h2>
 <p class="lead">Sleep disorders hide in plain sight. Tap the signs you, or the person you share a bed with, have noticed.</p>
 <div class="verdict" aria-live="polite"><span class="verdict-count" data-count>0</span><p data-verdict>Tap anything that sounds like you.<small>Your answers stay on this page.</small></p></div>
 <p style="margin-top:22px"><a class="link-arrow" href="/book-appointment/">Book an assessment {I['arrow']}</a></p></div>
 <ul class="chips reveal" aria-label="Common signs of a sleep disorder">{chip_html}</ul>
</div></section>

<section class="section mist"><div class="wrap">
 <div class="sec-head"><p class="eyebrow">What we treat</p><h2>Every sleep problem has a cause. <em>We find it.</em></h2><p class="lead">From snoring that keeps the house awake to insomnia that has lasted for years, we diagnose and treat the full range of adult and child sleep disorders.</p></div>
 <div class="grid-3">{cond_cards(feature_first=True)}</div>
 <p style="margin-top:30px"><a class="link-arrow" href="/what-is-sleep/">New to sleep medicine? Read what healthy sleep looks like {I['arrow']}</a></p>
</div></section>

<section class="night section"><div class="stars"></div><div class="wrap">
 <div class="sec-head"><p class="eyebrow">A night in our sleep lab</p><h2>Check in at dusk. <em>Leave with data.</em></h2><p class="lead">An overnight sleep study (polysomnography) is the gold standard for diagnosing sleep apnoea and other sleep disorders. Here is how it works.</p></div>
 <ol class="timeline reveal">
  <li><time>Before</time><h3>Consultation</h3><p>A specialist takes your history, examines your airway and decides which test you need.</p></li>
  <li><time>Evening</time><h3>Check in</h3><p>Arrive in comfortable night clothes. Your private room is designed to feel like your own bedroom.</p></li>
  <li><time>Bedtime</time><h3>Painless sensors</h3><p>Small sensors on the scalp, face, chest, legs and finger record your sleep. Nothing hurts.</p></li>
  <li><time>All night</time><h3>Watched over</h3><p>A sleep technologist monitors breathing, oxygen, heart and brain activity until morning.</p></li>
  <li><time>After</time><h3>Results &amp; plan</h3><p>Your study is scored and reported, then reviewed with you alongside a treatment plan.</p></li>
 </ol>
 <p style="margin-top:44px"><a class="btn moon" href="/sleep-study-polysomnography/">How to prepare for a sleep study {I['arrow']}</a></p>
</div></section>

<section class="section"><div class="wrap stats">
 <div class="reveal"><p class="eyebrow">What we see most</p><div class="big-num">4 in 10</div><h2 style="margin-top:.3em">patients come to us with <em>insomnia.</em></h2>
 <p class="lead">Since opening in {CLINIC['founded']}, our centre has diagnosed and treated patients from across Kenya and the region. Insomnia and sleep apnoea together account for most visits.</p></div>
 <div class="reveal"><ul class="bars" aria-label="Share of patients by sleep disorder">
  <li><span>Insomnia</span><span class="track"><span class="fill" style="--w:40%"></span></span><b>40%</b></li>
  <li><span>Sleep apnoea</span><span class="track"><span class="fill" style="--w:30%"></span></span><b>30%</b></li>
  <li><span>Narcolepsy</span><span class="track"><span class="fill" style="--w:15%"></span></span><b>15%</b></li>
  <li><span>Parasomnias</span><span class="track"><span class="fill" style="--w:15%"></span></span><b>15%</b></li></ul>
 <p class="source">Source: the centre's patient data, as reported by Nation (Healthy Nation) and The Standard.</p></div>
</div></section>

<section class="section mist"><div class="wrap split">
 <div class="reveal"><p class="eyebrow">Treatment</p><h2>A diagnosis is only half the job. <em>We treat it too.</em></h2>
 <p class="lead">Your report comes with a plan, and a team to carry it out under one roof and across the Nairobi ENT family.</p>
 <ul class="ticks"><li><strong>CPAP therapy</strong> for sleep apnoea, with machine and mask fitting, and follow-up until it feels natural.</li>
 <li><strong>Non-surgical and surgical treatment of sleep apnoea</strong> by our founding ENT surgeons, for nasal blockage, large tonsils and other airway causes.</li>
 <li><strong>CBT for insomnia</strong> and psychology support, the recommended first treatment for chronic insomnia.</li>
 <li><strong>Specialist medical management</strong> for narcolepsy, restless legs and limb movement disorders.</li></ul>
 <a class="link-arrow" href="/cpap-equipment/">CPAP machines, masks &amp; supplies {I['arrow']}</a></div>
 <div class="grid-2 reveal">
  <div class="card"><div class="card-icon">{I['mask']}</div><h3>CPAP clinic</h3><p style="margin:0">Fitting, pressure settings, mask troubleshooting and long-term support.</p></div>
  <div class="card"><div class="card-icon">{I['nose']}</div><h3>Airway &amp; ENT</h3><p style="margin:0">Nose and throat causes of snoring and apnoea, with Nairobi ENT Clinic.</p></div>
  <div class="card"><div class="card-icon">{I['brain']}</div><h3>Sleep psychology</h3><p style="margin:0">CBT-I, anxiety and the habits that keep insomnia going.</p></div>
  <div class="card feature"><div class="card-icon">{I['team']}</div><h3>One team</h3><p style="margin:0">Specialists who share your results and plan care together.</p></div>
 </div>
</div></section>

<section class="section"><div class="wrap split" style="align-items:start">
 <div class="reveal"><p class="eyebrow">Questions</p><h2>Before you <em>book</em></h2><p class="lead">The things patients ask us most. Can't see yours? WhatsApp us and we'll answer.</p><a class="btn line" href="/faqs/">All FAQs {I['arrow']}</a></div>
 <div class="reveal">{faq_html(GENERAL_FAQS[:5])}</div>
</div></section>
{cta_band()}'''
    desc = "Diagnose and treat sleep apnoea, snoring and insomnia at Nairobi's specialist sleep lab. Overnight sleep studies, CPAP and expert care. Book today."
    write("/", "Sleep Clinic & Sleep Study in Nairobi | The Sleep Centre", desc, body,
          [org_schema(), {"@context": "https://schema.org", "@type": "WebSite", "name": CLINIC["name"], "url": DOMAIN + "/"}, faq_schema(GENERAL_FAQS[:5])], priority="1.0")


def condition_pages():
    for c in CONDITIONS:
        crumbs = [("Home", "/"), ("Conditions", "/conditions/"), (c["name"], f'/{c["slug"]}/')]
        body = page_hero(crumbs, c["h1"], c["lead"], eyebrow="Sleep conditions") + f'''
<section class="section"><div class="wrap content-grid"><article class="prose">{c["body"]}
<h2>Frequently asked questions</h2>{faq_html(c["faqs"])}
<div class="callout" style="margin-top:28px"><p><b>Ready to find out?</b> <a href="/book-appointment/">Book a consultation or sleep study</a>, call <a href="tel:{CLINIC['tel']}">{CLINIC['phone']}</a> or <a href="{wa_link()}" target="_blank" rel="noopener">WhatsApp us</a>.</p></div>
</article>{aside(c["slug"])}</div></section>{cta_band()}'''
        mwp = {"@context": "https://schema.org", "@type": "MedicalWebPage", "name": c["title"], "url": f'{DOMAIN}/{c["slug"]}/',
               "about": {"@type": "MedicalCondition", "name": c["name"]}, "lastReviewed": TODAY,
               "publisher": {"@id": DOMAIN + "/#clinic"}}
        write(f'/{c["slug"]}/', c["title"], c["desc"], body, [mwp, faq_schema(c["faqs"])], crumbs)


def conditions_hub():
    crumbs = [("Home", "/"), ("Conditions", "/conditions/")]
    body = page_hero(crumbs, "Sleep disorders <em>we diagnose and treat</em>", "Whatever is keeping you, or someone you love, from good sleep, the first step is finding out exactly what is going on.", eyebrow="Conditions") + f'''
<section class="section"><div class="wrap"><div class="grid-3">{cond_cards(feature_first=True)}
<a class="card reveal" href="/what-is-sleep/"><div class="card-icon">{I['moon']}</div><h3>What is sleep?</h3><p>Sleep stages, cycles and how much you really need. A plain-language guide.</p><span class="link-arrow">Read the guide {I['arrow']}</span></a>
<a class="card reveal" href="/sleep-study-polysomnography/"><div class="card-icon">{I['lab']}</div><h3>Sleep study</h3><p>How an overnight polysomnography works, how to prepare and what to bring.</p><span class="link-arrow">Learn more {I['arrow']}</span></a>
<a class="card reveal" href="/cpap-equipment/"><div class="card-icon">{I['mask']}</div><h3>CPAP &amp; equipment</h3><p>Machines, masks and supplies, fitted and followed up by our team.</p><span class="link-arrow">See equipment {I['arrow']}</span></a>
</div></div></section>{cta_band()}'''
    write("/conditions/", "Sleep Disorders We Treat | The Sleep Centre Nairobi",
          "Sleep apnoea, snoring, insomnia, narcolepsy, restless legs and limb movement disorders: specialist diagnosis and treatment in Nairobi.", body, crumbs=crumbs, priority="0.9")


def what_is_sleep():
    crumbs = [("Home", "/"), ("Conditions", "/conditions/"), ("What is sleep?", "/what-is-sleep/")]
    body = page_hero(crumbs, "What is sleep, <em>and how much do you need?</em>", "Sleep is not switching off. It is an active, carefully organised process that restores the body and brain every night.", ctas=False, eyebrow="Sleep guide") + f'''
<section class="section"><div class="wrap content-grid"><article class="prose">
<h2>The stages of sleep</h2>
<p>Through the night you move through two main kinds of sleep, which a sleep study can see clearly in your brain waves:</p>
<table><thead><tr><th>Stage</th><th>What happens</th></tr></thead><tbody>
<tr><td><strong>N1</strong> (light sleep)</td><td>The drift from wakefulness into sleep. Lasts a few minutes; you wake easily.</td></tr>
<tr><td><strong>N2</strong></td><td>Heart rate and temperature fall. Takes up about half of a typical adult's night.</td></tr>
<tr><td><strong>N3</strong> (deep sleep)</td><td>Slow-wave sleep: the most physically restorative stage, and hardest to wake from. More of it early in the night.</td></tr>
<tr><td><strong>REM</strong> (dreaming sleep)</td><td>The brain is very active and most vivid dreams happen, while the body's muscles are temporarily relaxed. Important for memory and mood. More of it towards morning.</td></tr></tbody></table>
<h2>Sleep cycles</h2>
<p>These stages repeat in cycles of roughly 90 minutes, four to six times a night. Early cycles hold more deep sleep and later cycles more REM sleep, which is why cutting the night short costs you mostly dreaming sleep. The chart on our <a href="/">home page</a> shows what this looks like in a real recording.</p>
<h2>How much sleep do you need?</h2>
<ul><li><strong>Adults:</strong> seven hours or more a night, regularly</li><li><strong>Teenagers:</strong> eight to ten hours</li><li><strong>School-age children:</strong> nine to twelve hours</li><li><strong>Younger children and babies:</strong> more, including naps</li></ul>
<p>Quality matters as much as quantity. Eight hours in bed is not restful if your breathing stops dozens of times an hour or your legs keep waking you.</p>
<h2>Why sleep matters</h2>
<p>Good sleep supports memory, concentration, mood, the immune system, blood pressure and blood sugar control. Long-term poor sleep is linked to heart disease, diabetes, weight gain, depression and accidents.</p>
<h2>Simple habits that help</h2>
<ul><li>Get up at the same time every day, weekends included</li><li>Get daylight in the morning, and keep evenings dim</li><li>Keep caffeine to before midday, and limit alcohol near bedtime</li><li>Keep the bedroom cool, dark and quiet, and screens out of bed</li><li>Wind down for an hour before bed</li></ul>
<div class="callout"><p><b>When to see us:</b> if you snore loudly, stop breathing in your sleep, struggle to sleep for weeks at a time, or feel sleepy during the day despite enough time in bed. <a href="/book-appointment/">Book an assessment</a>.</p></div>
</article>{aside("what-is-sleep")}</div></section>{cta_band()}'''
    mwp = {"@context": "https://schema.org", "@type": "MedicalWebPage", "name": "What is sleep?", "url": DOMAIN + "/what-is-sleep/", "lastReviewed": TODAY, "publisher": {"@id": DOMAIN + "/#clinic"}}
    write("/what-is-sleep/", "What Is Sleep? Stages, Cycles & How Much You Need",
          "A plain-language guide to sleep stages, 90-minute sleep cycles, how much sleep adults and children need, and when to see a sleep specialist.", body, [mwp], crumbs, priority="0.6")


def sleep_study():
    crumbs = [("Home", "/"), ("Sleep study", "/sleep-study-polysomnography/")]
    body = page_hero(crumbs, "Overnight sleep study <em>(polysomnography)</em> in Nairobi", "The most complete test of your sleep: one comfortable night in our sleep laboratory, monitored from lights-out until morning.", eyebrow="Diagnostics") + f'''
<section class="section"><div class="wrap content-grid"><article class="prose">
<h2>What is a sleep study?</h2>
<p>Polysomnography records what your body does while you sleep. It is the gold-standard test for <a href="/obstructive-sleep-apnoea/">sleep apnoea</a> and is used to investigate <a href="/narcolepsy/">narcolepsy</a>, <a href="/periodic-limb-movement-disorder/">limb movement disorders</a>, unusual behaviours in sleep and unexplained daytime sleepiness.</p>
<h2>What it measures</h2>
<table><thead><tr><th>Sensor</th><th>What it tells us</th></tr></thead><tbody>
<tr><td>Brain waves (EEG)</td><td>When you are asleep, and in which sleep stage</td></tr>
<tr><td>Eye movements (EOG)</td><td>When you enter REM (dreaming) sleep</td></tr>
<tr><td>Chin and leg muscles (EMG)</td><td>Muscle tone, teeth grinding and leg movements</td></tr>
<tr><td>Airflow and breathing effort</td><td>Pauses and shallow breathing, and whether they are obstructive</td></tr>
<tr><td>Oxygen level (oximetry)</td><td>How far oxygen drops during breathing events</td></tr>
<tr><td>Heart rhythm (ECG)</td><td>Heart rate and rhythm changes during sleep</td></tr>
<tr><td>Body position and snoring</td><td>Whether problems are worse on your back, and how loud you snore</td></tr></tbody></table>
<h2>Who needs one?</h2>
<ul><li>Loud snoring with pauses, gasping or choking</li><li>Daytime sleepiness that does not improve with more sleep</li><li>Suspected narcolepsy or sleep attacks</li><li>Kicking or jerking legs at night</li><li>Unusual behaviour in sleep, such as acting out dreams</li><li>Setting the right pressure for a new CPAP machine</li></ul>
<h2>How to prepare</h2>
<ul><li>Keep to your usual routine on the day, and avoid napping</li><li>No caffeine after midday, and no alcohol on the day of the study</li><li>Wash and dry your hair; skip oils, gels and hair extensions or braids that cover the scalp if you can (tell us if not)</li><li>Remove nail polish from at least one finger for the oxygen sensor</li><li>Take your usual medicines unless we tell you otherwise, and bring a list of them</li></ul>
<h2>What to bring</h2>
<ul><li>Comfortable two-piece night clothes</li><li>Toiletries and anything you need for the morning</li><li>Your medicines and medication list</li><li>Your ID, insurance card and any referral letter or earlier results</li><li>Your own pillow, if it helps you sleep</li></ul>
<h2>On the night</h2>
<p>You arrive in the evening and settle into a private room. A sleep technologist fits the sensors, which takes about 45 minutes and does not hurt, and checks the signals before lights-out. They monitor you through the night from the next room, and can help if you need the bathroom. In the morning the sensors come off, and you can go home or straight to work.</p>
<h2>Results</h2>
<p>A full night produces hours of recording that are scored and reported by a specialist. We book a follow-up appointment to explain your report, including your <strong>apnoea–hypopnoea index (AHI)</strong> where relevant, and agree a treatment plan.</p>
<h2>Cost and insurance</h2>
<p>Call or WhatsApp us for the current price. Many insurers cover sleep studies, sometimes with a doctor's referral. We can help you check your cover and request pre-authorisation before your study.</p>
<h2>Frequently asked questions</h2>{faq_html(STUDY_FAQS)}
</article>{aside("")}</div></section>{cta_band("Book your <em>sleep study</em>", "Tell us your preferred date and we'll confirm availability, preparation and cost.")}'''
    test = {"@context": "https://schema.org", "@type": "MedicalWebPage", "name": "Overnight sleep study (polysomnography)", "url": DOMAIN + "/sleep-study-polysomnography/",
            "lastReviewed": TODAY, "about": {"@type": "MedicalTest", "name": "Polysomnography", "alternateName": "Sleep study", "usedToDiagnose": [{"@type": "MedicalCondition", "name": c["name"]} for c in CONDITIONS if c["slug"] != "insomnia"]},
            "publisher": {"@id": DOMAIN + "/#clinic"}}
    write("/sleep-study-polysomnography/", "Sleep Study (Polysomnography) in Nairobi | How It Works",
          "What an overnight sleep study measures, how to prepare, what to bring, cost and insurance. Book a polysomnography at our Nairobi sleep lab.", body, [test, faq_schema(STUDY_FAQS)], crumbs, priority="0.9")


def equipment():
    crumbs = [("Home", "/"), ("CPAP & equipment", "/cpap-equipment/")]
    cards = "".join(f'''<article class="card reveal"><div class="equip-art">{I[ic_]}</div><div class="equip-body"><h3>{n}</h3><p>{t}</p>
<a class="btn line sm" href="{wa_link(f'Hello, I would like a quote for: {n}.')}" target="_blank" rel="noopener">{I['wa']}Request a quote</a></div></article>''' for n, ic_, t in EQUIPMENT)
    body = page_hero(crumbs, "CPAP machines, masks <em>&amp; sleep equipment</em>", "Equipment only works if it fits and you use it. We supply, set up and support everything we sell.", eyebrow="Equipment") + f'''
<section class="section"><div class="wrap"><div class="equip">{cards}</div></div></section>
<section class="section mist"><div class="wrap split">
<div class="reveal"><p class="eyebrow">Why buy from a sleep centre</p><h2>Set up properly, <em>supported for the long run</em></h2>
<ul class="ticks"><li>Pressure settings based on your own sleep study</li><li>Masks fitted in person, with different styles to try</li><li>Follow-up reviews and data downloads to check that therapy is working</li><li>Help with dryness, leaks, noise and getting used to the mask</li><li>Spares and replacement parts when you need them</li></ul></div>
<div class="panel reveal"><h3>Prices and rental</h3><p>Prices depend on the model and accessories you need. Send us a WhatsApp or call for a quote, and ask about rental options so you can try CPAP before you buy.</p>
<a class="btn" href="{wa_link('Hello, I would like a CPAP quote.')}" target="_blank" rel="noopener">{I['wa']}Ask for a quote</a> <a class="btn line" href="tel:{CLINIC['tel']}" style="margin-top:10px">{I['phone']}{CLINIC['phone']}</a></div>
</div></section>{cta_band()}'''
    write("/cpap-equipment/", "CPAP Machines & Masks in Nairobi | The Sleep Centre",
          "CPAP, APAP and BiPAP machines, masks and supplies in Nairobi, fitted and followed up by sleep specialists. Request a quote on WhatsApp.", body, crumbs=crumbs, priority="0.8")


def about():
    crumbs = [("Home", "/"), ("About us", "/about-us/")]
    body = page_hero(crumbs, "Specialist sleep care, <em>made in Nairobi</em>", f"Since {CLINIC['founded']}, The Sleep Diagnostic &amp; Treatment Centre has given Kenyans a place to get sleep problems properly measured and treated, close to home.", eyebrow="About us") + f'''
<section class="section"><div class="wrap split">
<div class="reveal prose"><h2>Why we exist</h2>
<p>The Sleep Diagnostic and Treatment Centre (SDTC) is a dedicated sleep laboratory for the diagnosis and treatment of sleep disorders. It was founded in {CLINIC['founded']} by three ear, nose and throat surgeons, Prof. Muthure Macharia, Dr Chimmy Omamo-Olende and Dr Samuel M. Nyagah, so that patients in Kenya and the region could have sleep studies close to home.</p>
<p>We are in a quiet, accessible setting on Mbaazi Avenue in Lavington. Our study rooms are designed to feel like your own bedroom, because the more natural your night, the more accurately the results reflect the sleep you get every night.</p></div>
<div class="grid-2 reveal">
 <div class="card"><div class="card-icon">{I['lab']}</div><h3>Sleep laboratory</h3><p style="margin:0">Private, comfortable rooms for overnight polysomnography, monitored by trained technologists.</p></div>
 <div class="card"><div class="card-icon">{I['team']}</div><h3>One team</h3><p style="margin:0">ENT, psychology and sleep technology working from the same results.</p></div>
 <div class="card"><div class="card-icon">{I['shield']}</div><h3>Evidence first</h3><p style="margin:0">Treatment based on your own data and international guidelines.</p></div>
 <div class="card feature"><div class="card-icon">{I['moon']}</div><h3>Since {CLINIC['founded']}</h3><p style="margin:0">Founded by ENT surgeons, serving patients from across Kenya and the region.</p></div>
</div></div></section>
<section class="section night"><div class="stars"></div><div class="wrap">
<div class="sec-head center reveal"><p class="eyebrow">Our vision</p><h2>Better sleep for <em>better health.</em></h2></div>
<div class="grid-2 reveal"><div class="panel"><h3>Our mission</h3><p style="margin:0">To provide high quality, ethical and personalised diagnosis and treatment of sleep-related disorders through timely and cost-effective services, using competent, well-trained staff and state-of-the-art technology.</p></div>
<div class="panel"><h3>Our values</h3><ul class="ticks" style="margin:0"><li>Integrity</li><li>Confidentiality</li><li>Compassion</li><li>Reliability</li><li>Passion</li></ul></div></div>
</div></section>
<section class="section mist"><div class="wrap split">
<div class="reveal"><p class="eyebrow">The Nairobi ENT family</p><h2>Breathe, hear, <em>sleep.</em></h2><p class="lead">We work alongside two sister clinics, so a problem that crosses specialties gets joined-up care.</p></div>
<div class="grid-2 reveal">{"".join(f'<a class="card" href="{u}" rel="noopener"><h3>{n}</h3><p>Specialists in {d}.</p><span class="link-arrow">Visit site {I["arrow"]}</span></a>' for n, u, d in FAMILY)}</div>
</div></section>
<section class="section"><div class="wrap"><div class="sec-head"><p class="eyebrow">Our people</p><h2>Meet the <em>team</em></h2></div><div class="team">{team_cards()}</div>
<p style="margin-top:28px"><a class="link-arrow" href="/our-team/">More about our team {I['arrow']}</a></p></div></section>{cta_band()}'''
    write("/about-us/", "About The Sleep Diagnostic & Treatment Centre, Nairobi",
          f"A specialist sleep laboratory in Lavington, Nairobi, founded by ENT surgeons in {CLINIC['founded']}. Sleep studies and treatment for sleep disorders.", body, crumbs=crumbs)


def team_cards():
    return "".join(f'<article class="person reveal"><div class="avatar" aria-hidden="true">{p["init"]}</div><h3>{p["name"]}</h3><p class="role">{p["role"]}</p><p>{p["bio"]}</p></article>' for p in TEAM)


def team():
    crumbs = [("Home", "/"), ("Our team", "/our-team/")]
    body = page_hero(crumbs, "The people <em>behind your night</em>", "Founded by ENT surgeons and supported by psychology and sleep technology, because sleep problems rarely have a single cause.", eyebrow="Our team") + f'''
<section class="section"><div class="wrap"><div class="team">{team_cards()}</div></div></section>
<section class="section mist"><div class="wrap split"><div class="reveal"><h2>How we <em>work together</em></h2></div>
<div class="reveal"><ul class="ticks"><li>Your consultation, sleep study and review are coordinated by one team</li><li>Results are shared between the specialists involved in your care</li><li>Referrals to ENT, psychology, psychiatry and other specialists are arranged for you when needed</li><li>Your GP or referring doctor receives a report, with your consent</li></ul></div></div></section>{cta_band()}'''
    people = [{"@context": "https://schema.org", "@type": "Person", "name": p["name"], "jobTitle": p["role"], "worksFor": {"@id": DOMAIN + "/#clinic"}} for p in TEAM]
    write("/our-team/", "Our Team | The Sleep Diagnostic & Treatment Centre",
          "Meet the ENT surgeons, psychologist and sleep technologists who diagnose and treat sleep disorders at our Nairobi sleep centre.", body, people, crumbs)


def book():
    crumbs = [("Home", "/"), ("Book an appointment", "/book-appointment/")]
    opts = ["Consultation with a sleep specialist", "Overnight sleep study", "Snoring / sleep apnoea", "Insomnia", "Child's sleep problem", "CPAP fitting or review", "CPAP equipment quote", "Other"]
    body = page_hero(crumbs, "Book an <em>appointment</em>", "Fill in the form and it opens WhatsApp with your request ready to send. Prefer to talk? Call us.", ctas=False, eyebrow="Appointments") + f'''
<section class="section"><div class="wrap content-grid">
<div class="panel"><form class="form" data-book data-wa="{CLINIC['whatsapp']}" novalidate>
 <div class="field"><label for="f-name">Full name</label><input id="f-name" name="name" autocomplete="name" required></div>
 <div class="field"><label for="f-phone">Phone number</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required placeholder="07xx xxx xxx"></div>
 <div class="field"><label for="f-email">Email <small>(optional)</small></label><input id="f-email" name="email" type="email" autocomplete="email"></div>
 <div class="field"><label for="f-service">What is it for?</label><select id="f-service" name="service" required><option value="">Choose one</option>{"".join(f"<option>{o}</option>" for o in opts)}</select></div>
 <div class="field"><label for="f-date">Preferred date</label><input id="f-date" name="date" type="date"></div>
 <div class="field"><label for="f-time">Preferred time</label><select id="f-time" name="time"><option value="">Any time</option><option>Morning</option><option>Afternoon</option><option>Evening (sleep study check-in)</option></select></div>
 <div class="field full"><label for="f-msg">Anything we should know? <small>(optional)</small></label><textarea id="f-msg" name="message" placeholder="For example: insurer, symptoms, or whether this is for a child"></textarea></div>
 <label class="consent"><input type="checkbox" name="consent" required> I agree to the clinic using these details to arrange my appointment, as described in the <a href="/privacy-policy/">privacy policy</a>.</label>
 <div class="form-actions"><button class="btn" type="submit">{I['wa']}Send request on WhatsApp</button><a class="btn line" href="tel:{CLINIC['tel']}">{I['phone']}Call instead</a></div>
 <p class="form-note" data-book-ok tabindex="-1" hidden>WhatsApp should have opened with your request. Press send, and we'll reply to confirm your appointment.</p>
</form></div>
<aside class="aside"><div class="panel"><h3>What happens next</h3><ol class="prose" style="padding-left:1.1em;font-size:.97rem;margin:0">
<li>We reply during clinic hours to confirm a date and time.</li><li>For a sleep study, we send preparation instructions and the price, and help check your insurance.</li><li>You come in for your consultation or overnight study.</li><li>We review your results with you and agree a treatment plan.</li></ol></div>
<div class="book-card"><h3>Opening hours</h3><table class="hours" style="color:#fff">{"".join(f"<tr><td>{d}</td><td style='color:#fff'>{h}</td></tr>" for d, h in HOURS)}</table><p style="margin:14px 0 0;font-size:.9rem">{STUDY_HOURS}</p></div></aside>
</div></section>'''
    write("/book-appointment/", "Book a Sleep Study or Consultation | Nairobi Sleep Centre",
          "Request an appointment or overnight sleep study at our Nairobi sleep centre. Send the form on WhatsApp or call us. We confirm within clinic hours.", body, crumbs=crumbs, priority="0.9")


def contact():
    crumbs = [("Home", "/"), ("Contact us", "/contact-us/")]
    email = f'<li><span class="ci">{I["mail"]}</span><div><b>Email</b><a href="mailto:{CLINIC["email"]}">{CLINIC["email"]}</a></div></li>' if CLINIC["email"] else ""
    body = page_hero(crumbs, "Contact <em>us</em>", "Questions about symptoms, sleep studies, CPAP or insurance? We're happy to help.", eyebrow="Contact") + f'''
<section class="section"><div class="wrap split" style="align-items:stretch">
<div class="panel"><ul class="contact-list">
<li><span class="ci">{I['phone']}</span><div><b>Call</b><a href="tel:{CLINIC['tel']}">{CLINIC['phone']}</a><br><a href="tel:{CLINIC['tel2']}">{CLINIC['phone2']}</a></div></li>
<li><span class="ci">{I['wa']}</span><div><b>WhatsApp</b><a href="{wa_link()}" target="_blank" rel="noopener">Chat with us</a></div></li>{email}
<li><span class="ci">{I['pin']}</span><div><b>Visit</b>{CLINIC['street']}, {CLINIC['area']}, {CLINIC['city']}<br><a href="{CLINIC['maps']}" target="_blank" rel="noopener">Get directions</a><br><span style="font-size:.9rem;color:var(--muted)">Postal: {CLINIC['pobox']}</span></div></li>
<li><span class="ci">{I['clock']}</span><div><b>Hours</b><table class="hours">{"".join(f"<tr><td>{d}</td><td>{h}</td></tr>" for d, h in HOURS)}</table><p style="font-size:.9rem;margin:10px 0 0">{STUDY_HOURS}</p></div></li></ul>
<p style="margin:28px 0 0"><a class="btn" href="/book-appointment/">{I['cal']}Book an appointment</a></p></div>
<iframe class="map" title="Map showing the clinic location in Lavington, Nairobi" src="{CLINIC['map_embed']}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
</div></section>'''
    write("/contact-us/", "Contact The Sleep Centre, Lavington, Nairobi",
          f"Call {CLINIC['phone']}, WhatsApp us or visit us at {CLINIC['street']}, {CLINIC['area']}, Nairobi. Opening hours, directions and booking.", body, [org_schema()], crumbs)


def faqs():
    crumbs = [("Home", "/"), ("FAQs", "/faqs/")]
    allf = GENERAL_FAQS + STUDY_FAQS[3:]
    body = page_hero(crumbs, "Frequently asked <em>questions</em>", "Straight answers about appointments, sleep studies, insurance and treatment.", eyebrow="FAQs") + f'''
<section class="section"><div class="narrow">{faq_html(allf)}</div></section>{cta_band("Still have a <em>question?</em>", "Send us a WhatsApp. A member of our team will reply during clinic hours.")}'''
    write("/faqs/", "Sleep Clinic FAQs: Sleep Studies, Cost & Insurance",
          "Answers about booking, referrals, sleep study preparation, cost, insurance, children and CPAP at our Nairobi sleep centre.", body, [faq_schema(allf)], crumbs, priority="0.6")


def privacy():
    crumbs = [("Home", "/"), ("Privacy policy", "/privacy-policy/")]
    em = CLINIC["email"] or "our clinic email"
    body = page_hero(crumbs, "Privacy <em>policy</em>", f"How {CLINIC['name']} collects, uses and protects your personal and health information.", ctas=False) + f'''
<section class="section"><div class="narrow prose">
<p><em>Last updated: {datetime.date.today().strftime('%d %B %Y')}</em></p>
<h2>Who we are</h2><p>{CLINIC['name']} ("we", "us"), {CLINIC['street']}, {CLINIC['area']}, {CLINIC['city']}, Kenya, is the data controller for personal data collected through this website and at our clinic. We process personal data in line with the Kenya Data Protection Act, 2019 and its regulations.</p>
<h2>What we collect</h2><ul><li><strong>Contact details</strong> you give us, such as your name, phone number and email address</li><li><strong>Appointment details</strong>, such as the service you need and your preferred date</li><li><strong>Health information</strong> you choose to share when booking, and the clinical information gathered during your care</li><li><strong>Website usage data</strong>, such as pages visited and device type, collected through analytics cookies if you allow them</li></ul>
<h2>How we use it</h2><ul><li>To respond to enquiries and arrange appointments</li><li>To provide, record and follow up your care</li><li>To process payments and insurance claims</li><li>To meet our legal and professional obligations</li><li>To understand and improve how our website is used</li></ul>
<p>Health information is sensitive personal data. We process it only to provide your care, with your consent, or where the law allows.</p>
<h2>Booking through WhatsApp</h2><p>Our booking form does not store your details on this website. When you press send, it opens WhatsApp with your message, and the message is handled by WhatsApp (Meta) under their own privacy terms. Please share only what is needed to book. You can always call us instead.</p>
<h2>Who we share it with</h2><p>We share information only when needed for your care or required by law: for example with doctors involved in your treatment, your insurer (for claims you ask us to make), laboratories, or regulators. We never sell your data.</p>
<h2>How long we keep it</h2><p>Medical records are kept for the period required by Kenyan law and professional guidelines. Enquiries that do not lead to an appointment are deleted when no longer needed.</p>
<h2>Your rights</h2><p>You have the right to be informed about how we use your data, to access it, to ask us to correct or delete it, to object to some processing, and to withdraw consent. To use these rights, contact us on <a href="tel:{CLINIC['tel']}">{CLINIC['phone']}</a> or at {escape(em)}. If you are not satisfied, you can complain to the Office of the Data Protection Commissioner (ODPC).</p>
<h2>Cookies</h2><p>We use only the cookies needed for the site to work, plus analytics cookies to understand site usage if they are enabled. You can block cookies in your browser settings.</p>
<h2>Security</h2><p>We use appropriate technical and organisational measures to protect your information, including restricted access to records.</p>
<h2>Changes</h2><p>We may update this policy. The date at the top shows when it last changed.</p>
</div></section>'''
    write("/privacy-policy/", "Privacy Policy | The Sleep Diagnostic & Treatment Centre",
          "How we collect, use and protect your personal and health information under Kenya's Data Protection Act, 2019, and your rights.", body, crumbs=crumbs, priority="0.3")


def not_found():
    body = f'''<section class="night page-hero" style="min-height:80vh;display:flex;align-items:center"><div class="stars"></div><div class="moon-orb"></div><div class="wrap">
<p class="eyebrow">Page not found</p><h1>This page is <em>fast asleep.</em></h1><p class="lead">The page you were looking for has moved or no longer exists.</p>
<div class="hero-ctas" style="margin-top:30px"><a class="btn moon" href="/">Go to the home page</a><a class="btn ghost" href="/book-appointment/">Book an appointment</a></div></div></section>'''
    write("/404/", "Page not found | The Sleep Centre", "The page you were looking for could not be found.", body)

# --------------------------------------------------------------- static files
def statics():
    if OUT.exists(): shutil.rmtree(OUT)
    shutil.copytree(SRC, OUT)


def sitemap():
    urls = "".join(f"<url><loc>{DOMAIN}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>" for p, pr in PAGES)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')


if __name__ == "__main__":
    statics()
    home(); conditions_hub(); condition_pages(); what_is_sleep(); sleep_study(); equipment()
    about(); team(); book(); contact(); faqs(); privacy(); not_found()
    sitemap()
    print(f"Built {len(PAGES)} pages into {OUT}")
