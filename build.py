#!/usr/bin/env python3
"""Static site generator for Fulani Ministries. Run: python3 build.py"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

NAV = [
    ("/", "Home"),
    ("/about/", "About"),
    ("/church-planting/", "Church Planting"),
    ("/education/", "Education"),
    ("/relief/", "Relief"),
    ("/testimony/", "Testimony"),
    ("/contact/", "Contact"),
]

BASE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="https://fulaniministries.org{canonical}">
<link rel="icon" href="/assets/img/logo.png">
<link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>
<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="/">
      <img src="/assets/img/logo.png" alt="Fulani Ministries logo">
      <span>Fulani Ministries</span>
    </a>
    <nav class="main-nav">
      {navlinks}
    </nav>
  </div>
</header>
{body}
<footer class="site-footer">
  <div class="footer-inner">
    <div>
      <strong>Fulani Ministries</strong><br>
      A Fulani response to God's grace &mdash; bringing the Gospel, relieving poverty,
      and promoting education among the Fulani people across Africa.
    </div>
    <div class="footer-links">
      <a href="/about/">About</a>
      <a href="/elim-missions/">Elim Missions</a>
      <a href="/donate/">Donate</a>
      <a href="/contact/">Contact</a>
      </div>
  </div>
  <div class="footer-small">&copy; Fulani Ministries. All rights reserved.</div>
</footer>
</body>
</html>
"""

REDIRECT = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url={local_target}">
<link rel="canonical" href="https://fulaniministries.org{target}">
<title>Redirecting&hellip;</title>
</head>
<body>
<p>This page has moved to <a href="{local_target}">{target}</a>.</p>
</body>
</html>
"""

import re

def navlinks_html(active):
    parts = []
    for href, label in NAV:
        cls = ' class="active"' if href == active else ""
        parts.append(f'<a href="{href}"{cls}>{label}</a>')
    return "\n      ".join(parts)

def depth_of(path):
    trimmed = path.strip("/")
    return 0 if trimmed == "" else trimmed.count("/") + 1

def relativize(html, path):
    """Rewrite root-relative href="/..." and src="/..." into path-relative
    links, so the site works both at a subpath (e.g. github.io/fulani/) and
    at a domain root. Absolute URLs (https://...) are left untouched."""
    depth = depth_of(path)
    prefix = "../" * depth

    def repl(match):
        attr, target = match.group(1), match.group(2)
        local = prefix + target.lstrip("/") if target != "/" else (prefix or "./")
        return f'{attr}="{local}"'

    return re.sub(r'(href|src)="(/[^"]*)"', repl, html)

def page(path, title, description, body_html, active=None):
    html = BASE.format(
        title=title,
        description=description,
        canonical=path,
        navlinks=navlinks_html(active or path),
        body=body_html,
    )
    html = relativize(html, path)
    out_dir = os.path.join(ROOT, path.strip("/"))
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w") as f:
        f.write(html)

def redirect(path, target):
    depth = depth_of(path)
    prefix = "../" * depth
    local_target = prefix + target.lstrip("/") if target != "/" else (prefix or "./")
    html = REDIRECT.format(target=target, local_target=local_target)
    out_dir = os.path.join(ROOT, path.strip("/"))
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w") as f:
        f.write(html)

# ---------------------------------------------------------------- HOME
page(
    "/",
    "Fulani Ministries | A Fulani Response to God's Grace",
    "Fulani Ministries is an interdenominational ministry bringing the Gospel, relief and education to the Fulani people across Africa.",
    """
<section class="hero">
  <h1>Foofo! Welcome to Fulani Ministries</h1>
  <p>We are Fulani Christians with a vision and mission to reach out to other Fulani
  people with the Gospel of Christ across Africa.</p>
  <a class="cta" href="/donate/">Support Our Work</a>
  <a class="cta secondary" href="/about/">Learn About Us</a>
</section>
<main>
  <p>The Fulani people are the largest unreached people group in the world. They live in
  19 countries across Africa, from the Gambia in the West to Sudan in the East. Over 99%
  have not yet had the chance to hear the Gospel for the first time.</p>
  <p>Fulani Ministries&rsquo; vision and mission is for Fulani Christians to bring the
  Gospel to the hearts of Fulani people across Africa and beyond. As Fulani Christians
  with no cultural barrier to overcome, we are able to readily introduce the Gospel to
  our fellow Fulanis.</p>

  <h2>Our Work</h2>
  <div class="card-grid">
    <div class="card">
      <h3>Church Planting</h3>
      <p>Discipleship and church planting training, radio and video ministry, and music
      recorded by the choirs of the Jam Tan churches.</p>
      <a href="/church-planting/">Read more &rarr;</a>
    </div>
    <div class="card">
      <h3>Education</h3>
      <p>The Jam Tan Primary &amp; Preschools, and skills training in tailoring,
      carpentry, shopkeeping and more.</p>
      <a href="/education/">Read more &rarr;</a>
    </div>
    <div class="card">
      <h3>Relief</h3>
      <p>Business training, agriculture, relief work and accessible healthcare for
      communities across West Africa.</p>
      <a href="/relief/">Read more &rarr;</a>
    </div>
  </div>

  <blockquote>
    &ldquo;How, then, can they call on the one they have not believed in? And how can
    they believe in the one of whom they have not heard? And how can they hear without
    someone preaching to them?&rdquo; &mdash; Romans 10:14
  </blockquote>
</main>
""",
    active="/",
)

# ---------------------------------------------------------------- ABOUT
page(
    "/about/",
    "About Us | Fulani Ministries",
    "Fulani Ministries is an interdenominational ministry giving the Fulani people the opportunity to hear the Good News of Jesus Christ.",
    """
<div class="page-header"><h1>About Us</h1></div>
<main>
  <p>Fulani Ministries is an interdenominational ministry that aims to give an
  opportunity to the Fulani people to hear the Good News of Jesus Christ.</p>
  <p>Our vision as Fulani Christians is to reach out to other Fulanis with the Gospel,
  and to equip them so that they in turn may reach out to other Fulanis. We do not
  fulfil this vision by our own might or strength, but by the grace of God through the
  contribution of many.</p>

  <h2>Our Three-Fold Vision</h2>
  <ul>
    <li>To further the Christian faith among the Fulani people</li>
    <li>To relieve poverty and suffering among the Fulani people</li>
    <li>To promote education among the Fulani people</li>
  </ul>

  <h2>How Fulani Ministries Began</h2>
  <p>Fulani Ministries was born out of the vision God gave to a Fulani Christian,
  Boureima Diallo, in 1997 in Burkina Faso, West Africa. A number of Fulani Christians
  became involved, working alongside Boureima. Fulani Ministries is now involved in
  reaching out to the Fulani people in several countries of Sub-Saharan Africa by
  various means of evangelism (Romans 10:13&ndash;15).</p>
  <p>Boureima, originally from Burkina Faso, was brought up as a Muslim and accepted the
  Lord Jesus Christ as his Saviour in 1985. In 2001 he gained a BA (Hons) in Applied
  Theology and Cross-Cultural Studies from Moorlands College, UK. Read
  <a href="/testimony/">Boureima&rsquo;s full testimony</a> to learn more of his story.</p>

  <div class="card-grid">
    <div class="card"><h3>Fulani People</h3><p>Who are the Fulani?</p><a href="/fulani-people/">Read more &rarr;</a></div>
    <div class="card"><h3>Statement of Faith</h3><p>What we believe.</p><a href="/statement-of-faith/">Read more &rarr;</a></div>
  </div>
</main>
""",
)

# ---------------------------------------------------------------- FULANI PEOPLE
page(
    "/fulani-people/",
    "The Fulani People | Fulani Ministries",
    "The Fulani people are the largest unreached people group in the world, numbering approximately 40 million across Africa.",
    """
<div class="page-header"><h1>The Fulani People</h1></div>
<main>
  <p>The Fulani people are the largest unreached people group in the world. They live
  in 19 countries across Africa, from the Gambia in the West to Sudan in the East. Over
  99% have not had the chance to hear the Gospel for the first time.</p>
  <p>The Fula people, or Fulani, or Fulɓe, are one of the largest ethnolinguistic groups
  in Africa, numbering approximately 40 million people in total. They are one of the
  most widely dispersed and culturally diverse of the peoples of Africa. The Fulani are
  bound together by the common language of Fulfulde, as well as by basic elements of
  Fulɓe culture, such as the Pulaaku, a code of conduct common to all Fulani groups.</p>
  <p>A significant proportion of their number &mdash; an estimated 13 million &mdash;
  are nomadic, making them the largest pastoral nomadic group in the world. Spread over
  many countries, they are found mainly in West Africa and the northern parts of
  Central Africa, but also in Sudan and Egypt.</p>
  <p>The Fulani are traditionally a nomadic, pastoralist trading people. They herd
  cattle, goats and sheep across the vast dry hinterlands of their domain, keeping
  somewhat separate from local agricultural populations. They inhabit territories over
  an area larger in size than the continental United States.</p>
</main>
""",
    active="/about/",
)

# ---------------------------------------------------------------- STATEMENT OF FAITH
SOF_BODY = """
<div class="page-header"><h1>Statement of Faith</h1></div>
<main>
  <p>Fulani Ministries is a member of the Evangelical Alliance, and therefore
  subscribes to the following basis of faith:</p>
  <ol>
    <li>The one true God who lives eternally in three persons &mdash; the Father, the
    Son and the Holy Spirit.</li>
    <li>The love, grace and sovereignty of God in creating, sustaining, ruling,
    redeeming and judging the world.</li>
    <li>The divine inspiration and supreme authority of the Old and New Testament
    Scriptures, which are the written Word of God &mdash; fully trustworthy for faith
    and conduct.</li>
    <li>The dignity of all people, made male and female in God&rsquo;s image to love,
    be holy and care for creation, yet corrupted by sin, which incurs divine wrath and
    judgement.</li>
    <li>The incarnation of God&rsquo;s eternal Son, the Lord Jesus Christ &mdash; born
    of the virgin Mary; truly divine and truly human, yet without sin.</li>
    <li>The atoning sacrifice of Christ on the cross: dying in our place, paying the
    price of sin and defeating evil, so reconciling us with God.</li>
    <li>The bodily resurrection of Christ, the first fruits of our resurrection; his
    ascension to the Father, and his reign and mediation as the only Saviour of the
    world.</li>
    <li>The justification of sinners solely by the grace of God through faith in
    Christ.</li>
    <li>The ministry of God the Holy Spirit, who leads us to repentance, unites us with
    Christ through new birth, empowers our discipleship and enables our witness.</li>
    <li>The Church, the body of Christ both local and universal, the priesthood of all
    believers &mdash; given life by the Spirit and endowed with the Spirit&rsquo;s
    gifts to worship God and proclaim the gospel, promoting justice and love.</li>
    <li>The personal and visible return of Jesus Christ to fulfil the purposes of God,
    who will raise all people to judgement, bring eternal life to the redeemed and
    eternal condemnation to the lost, and establish a new heaven and new earth.</li>
  </ol>
</main>
"""
page(
    "/statement-of-faith/",
    "Statement of Faith | Fulani Ministries",
    "Fulani Ministries is a member of the Evangelical Alliance and subscribes to their basis of faith.",
    SOF_BODY,
    active="/about/",
)

# ---------------------------------------------------------------- TESTIMONY
TESTIMONY_PARAS = """
  <p>Boureima Diallo&rsquo;s Testimony &mdash; From Islam to Jesus (Elim Missionary)</p>
  <p><em>Foofo!!! (Hello!!!)</em></p>
  <p>My name is Boureima, I am Fulani (Pullo) from Burkina Faso in West Africa. I am a
  Fulani person; Fulani is the name of my ethnic group in English &mdash; we call
  ourselves Fulɓe in our own language, Fulfulde. The Fulani people are nomads scattered
  across nineteen countries of Africa, and are statistically considered 99% Muslim. I
  was a Muslim as well. Praise God, Jesus has saved me from the darkness of Islam to
  His wonderful light, and has called and anointed me to bring His Good News of
  salvation by grace through faith to my people.</p>
  <p>The Lord saved me when I was thirteen years old, in 1985. My father employed a man
  named Adama to help with housework &mdash; Adama was not Fulani, but Mossi, and a
  Christian. He was the first person to tell me about Jesus, explaining that Jesus had
  suffered in his place for his sins and had changed his life. He asked me a question
  that struck me deeply: Muslims believe God weighs your good deeds against your bad
  deeds &mdash; but where will you be if they are equal? I had no answer.</p>
  <p>A few weeks later I asked to go to church with Adama. To my surprise, my father
  gave his permission and told me he wanted me to be a good Christian &mdash; even
  though he did not go to church himself. Later I discovered he owned a Bible, bought
  years earlier while studying in France, and he helped me understand my new faith
  better than anyone, explaining it to me in our own language, Fulani.</p>
  <p>I faced strong opposition from my extended family, particularly from an uncle who
  threatened my life after my father&rsquo;s death in 1988. It was often very difficult
  being the only Fulani Christian in my village, but the Lord enabled me through these
  storms to abandon myself to Him. In time, two of my brothers and a sister also came
  to faith in Jesus.</p>
  <p>I heard from my family that when I was three years old I contracted polio and was
  paralysed. When I was five, my mother &mdash; though a Muslim &mdash; took me to an
  evangelistic campaign near our village. When the pastor prayed for me, I started
  walking. I believe the Lord has been working in my life for His glory for a very long
  time.</p>
  <p>Progressively the Lord led me to spread His word among Fulani households, villages
  and provinces, through travel, local Christian radio and preaching tapes. During my
  studies at university, God challenged me to stop my studies and be available for Him
  for the salvation of my people. I fought against the calling &mdash; I wanted to be a
  lawyer, not a full-time evangelist &mdash; and I asked God for a clear sign before I
  would say yes. That same day, in my room at university, God gave me the opportunity
  to lead two students to Him. On 14th May 1997, at about 11am, I said yes to Jesus.</p>
  <p>My decision was not welcomed by all of my family, and the months that followed
  brought a series of hard trials &mdash; including the loss of my mother, though she
  committed her life to the Lord before she passed. Through it all, I have held to
  Romans 8:28.</p>
  <p>The burden the Lord has placed in my heart is the salvation of my people, the
  Fulani. I completed a degree in theology in June 2001 in England, and my wife and I
  now serve God in Africa, leading this pioneering interdenominational evangelism
  ministry among the Fulani people &mdash; Fulani Ministries.</p>
  <p>Having read this testimony: do you want to believe in Jesus, or know Him more? Do
  you want to join us in the task of giving people the chance to hear the Gospel? If
  so, please <a href="/contact/">contact us</a>.</p>
"""
page(
    "/testimony/",
    "Testimony | Fulani Ministries",
    "Boureima Diallo's testimony: from Islam to Jesus, and the calling that led to the founding of Fulani Ministries.",
    f"""
<div class="page-header"><h1>Testimony</h1></div>
<main>
{TESTIMONY_PARAS}
</main>
""",
)

# ---------------------------------------------------------------- CHURCH PLANTING
page(
    "/church-planting/",
    "Church Planting | Fulani Ministries",
    "Discipleship and church planting training that has led to dozens of new churches among the Fulani people.",
    """
<div class="page-header"><h1>Church Planting</h1></div>
<main>
  <h2>Discipleship &amp; Church Planting Training Course</h2>
  <p>We follow Christ&rsquo;s command to make disciples, teaching these disciples to
  make disciples who in turn make disciples that multiply. Our discipleship and church
  planting training course runs for three to six months a year across several
  locations, and includes training in various skills for self-reliance.</p>

  <h2>Milestones</h2>
  <ul>
    <li>58 church planters have been trained and empowered to find people of peace and
    start discovery Bible classes</li>
    <li>40 churches have resulted from discovery Bible groups, with 5&ndash;15 converts
    in each church</li>
    <li>37 further discovery Bible groups are on the path to becoming churches</li>
    <li>A discipleship and training centre has been built in Burkina Faso, named the
    Jam Tan Centre</li>
    <li>At Easter, the church at the Jam Tan Centre baptised 32 people</li>
  </ul>

  <h2>Media</h2>
  <p>Fulani Ministries organises the recording and distribution of audio messages of
  preaching and Bible study for radio, and video messages for TV.</p>

  <h2>Music</h2>
  <p>Listen to Fulani Choir songs and traditional instrumental music, recorded by the
  choirs of the Jam Tan churches.</p>

  <a class="cta" href="/contact/">Get in Touch</a>
</main>
""",
)

# ---------------------------------------------------------------- EDUCATION
page(
    "/education/",
    "Education | Fulani Ministries",
    "The Jam Tan Primary & Preschools, and skills training for self-reliance among the Fulani people.",
    """
<div class="page-header"><h1>Education</h1></div>
<main>
  <h2>The Jam Tan Primary &amp; Preschools</h2>
  <p>Making education accessible, Fulani Ministries pays the school fees of students
  from internally displaced families. Preschool gives children a head-start, giving
  them a boost when they start primary school. Lunch is provided free of charge to all
  students.</p>

  <h2>Training in Skills for Self-Reliance</h2>
  <p>Tailoring, carpentry, shopkeeping, raising animals&hellip; we enable young people
  to gain skills and confidence to support themselves and provide services for their
  communities.</p>

  <h2>Social Cohesion</h2>
  <p>Marathons, cycle races (including women&rsquo;s cycle races), chequers
  competitions, dance competitions and table football. In a context of insecurity and
  inter-community tensions, Fulani Ministries works wherever possible to promote
  community cohesion. At our quarterly health days we hold sports and dance
  competitions to bring together the wider community around the Jam Tan Centre and
  celebrate the talent of local youth.</p>

  <a class="cta" href="/donate/">Make a Donation</a>
</main>
""",
)

# ---------------------------------------------------------------- RELIEF
page(
    "/relief/",
    "Relief | Fulani Ministries",
    "Relieving poverty and making healthcare accessible through business training, agriculture, relief work and healthcare.",
    """
<div class="page-header"><h1>Relief</h1></div>
<main>
  <p><strong>Our Mission:</strong> relieving poverty and making healthcare accessible.</p>

  <h2>Business Training</h2>
  <p>Fulani Ministries provides training in running small businesses for local
  communities of all ethnic backgrounds in several countries of West Africa. This
  training programme provides skills in running a business, including budgeting,
  understanding your market and business planning.</p>

  <h2>Agriculture</h2>
  <p>Our various agricultural projects are part of our aim to be self-sustaining. As
  part of the work of Fulani Ministries, seasonal crops are grown in different parts of
  Burkina Faso, which provide food for trainee church planters and for people in need.</p>

  <h2>Relief Work</h2>
  <p>We work to meet the needs of water, food and clothing in many communities. In
  particular, we assist families during the &lsquo;hungry&rsquo; months before harvest
  with gifts of grain and other food supplies.</p>

  <h2>Accessible Healthcare</h2>
  <p>The Community Health Day at the Jam Tan Centre offers the local population
  affordable consultations from Christian medics and paramedics. Bringing specialist
  doctors to a rural location makes healthcare accessible to a population who would
  normally need to travel to the city, stay overnight and pay high fees for
  consultations. The police are also present at this event to establish national ID
  cards for the local population. In response to the needs of the community, we hope
  to soon open a medical centre.</p>

  <a class="cta" href="/contact/">Get Involved</a>
</main>
""",
)

# ---------------------------------------------------------------- ELIM MISSIONS
page(
    "/elim-missions/",
    "Elim Missions | Fulani Ministries",
    "Fulani Ministries founder Boureima Diallo is an Elim Missionary, supported by Elim Missions for many years.",
    """
<div class="page-header"><h1>Elim Missions</h1></div>
<main>
  <p>Boureima Diallo is an Elim Missionary, and for many years Elim has helped and
  supported Boureima in his mission in Burkina Faso.</p>

  <h2>A Brief History of Elim Missions</h2>
  <p>In 1919, only four years after the founding of the Elim Pentecostal Church in the
  UK by George Jeffreys, one lady, Dollie Phillips, became Elim&rsquo;s first
  missionary overseas, sailing for Mumbai with a steely determination to take the
  gospel to those who had never heard it. It would be a further ten years before anyone
  joined her.</p>
  <p>Nearly a hundred years later, the same three components found on opening day are
  still calling for engagement: a church, a missionary, and the Spirit. Elim Missions
  exists to stand with a sending church, support the empowered missionary, and listen
  to and follow the Spirit.</p>
  <p>Elim Missions currently supports more than 55 missionaries &mdash; around 45
  missionary posts, taking into account couples &mdash; across 27 countries. They aim
  to pastorally care for each missionary: equipping, sustaining and championing them as
  they share the story of Jesus around the world, whether through language learning,
  cultural awareness, biblical studies, or simply telling their story to supporters
  back home.</p>
</main>
""",
)

# ---------------------------------------------------------------- CONTACT
page(
    "/contact/",
    "Contact | Fulani Ministries",
    "Get in touch with Fulani Ministries.",
    """
<div class="page-header"><h1>Contact Us</h1></div>
<main>
  <p>Are you interested in getting involved with Fulani Ministries, or want to know
  more about our work? We would love to hear from you.</p>
  <p><strong>Email:</strong> <a href="mailto:info@fulaniministries.org">info@fulaniministries.org</a></p>
</main>
""",
)

# ---------------------------------------------------------------- DONATE
page(
    "/donate/",
    "Donate | Fulani Ministries",
    "Support the work of Fulani Ministries at the Jam Tan Centre in Burkina Faso.",
    """
<div class="page-header"><h1>Donate</h1></div>
<main>
  <p>Please consider donating to support the work of Fulani Ministries at the Jam Tan
  Centre in Burkina Faso. Every gift helps us grow this ministry.</p>
  <p>You can give via <a href="https://www.stewardship.org.uk" target="_blank" rel="noopener">Stewardship.org.uk</a>,
  or <a href="/contact/">contact us</a> directly for UK bank transfer details.</p>
  <p class="footer-small" style="text-align:left;color:var(--muted)">
    Note: for security, we no longer publish bank account details directly on this
    page &mdash; please contact us to receive current, verified payment details.
  </p>
  <a class="cta" href="/contact/">Contact Us to Donate</a>
</main>
""",
)

# ---------------------------------------------------------------- LEGACY REDIRECTS
redirect("/about/fulani-people/", "/fulani-people/")
redirect("/about/missions/", "/about/")
redirect("/about/statement-of-faith/", "/statement-of-faith/")
redirect("/about/projects/", "/relief/")
redirect("/contact-us/", "/contact/")

print("Site built successfully.")
