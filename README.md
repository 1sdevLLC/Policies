# App Developer Website (GitHub Pages)

A ready-to-publish site for an iOS app business: landing page, support page, privacy policy, terms of use / EULA, and an optional consumer health data policy. You fill in one config file, run one script, and push.

> **These are templates, not legal advice.** They are drafted for a California LLC that sells iOS apps through the App Store using Apple In-App Purchase only. A privacy policy that doesn't match what your app really does is worse than none (App Review and regulators both check). Read every page after you generate it, and have a California attorney review the final versions once before launch, especially if you add accounts, a backend, or health data.

## What you get

| File (in `docs/` after you run the script) | What it's for |
|---|---|
| `index.html` | Landing page listing your apps (**Marketing URL** in App Store Connect) |
| `support.html` | Contact, FAQ, restore purchases, cancel/refund instructions (**Support URL**, required) |
| `privacy.html` | Privacy Policy incl. California/CCPA, CalOPPA, GDPR, children (**Privacy Policy URL**, required) |
| `terms.html` | Terms of Use with Apple's required minimum EULA terms, subscription terms, California consumer notice (**License Agreement / EULA link**) |
| `health-privacy.html` | Consumer Health Data Privacy Policy (only generated if you enable it, for the future HealthKit app) |
| `404.html`, `robots.txt`, `sitemap.xml`, `CNAME`, `style.css` | Supporting files (auto-generated) |

Folder layout in this repo:

```
site.config.json   <- the only file you edit
configure.py       <- fills in the templates
_template/         <- page templates (edit only to change wording)
docs/              <- generated site; this is what GitHub publishes
```

Only `docs/` is published. Your config and templates are not on the website.

## Quick start

1. **Edit `site.config.json`.** Replace every `YOUR ...` value with real information (LLC name, domain, emails, mailing address, county, effective date, app details). The script refuses to run until you do, so you can't accidentally publish placeholders.
2. **Set the flags** (see "Flags" below) so the policies match what your app actually does.
3. **Generate the site:**
   ```bash
   python3 configure.py
   ```
   (Requires Python 3, which is preinstalled on macOS.)
4. **Read the pages in `docs/`.** Open `docs/privacy.html` and `docs/terms.html` in a browser and check every statement against your app.
5. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial site"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
   git push -u origin main
   ```
6. **Turn on Pages:** in the GitHub repo go to **Settings → Pages → Build and deployment → Deploy from a branch → `main` → `/docs` → Save.** The repo must be public on a free plan. Under **Custom domain**, enter your domain (the `CNAME` file in `docs/` already contains it).
7. **Point your domain at GitHub** in Squarespace DNS (four `A` records for the apex and a `www` CNAME; details are in the earlier instructions). Once the site loads, tick **Enforce HTTPS** in Pages settings.

Because the site uses root-relative links (`/style.css`), it must be served from a custom domain at the root, not from `username.github.io/repo`.

## Flags (in `site.config.json`)

Each flag switches sections of the policies on or off. Set them honestly.

| Flag | Set to `true` if... |
|---|---|
| `has_subscriptions` | You sell subscriptions or in-app purchases through Apple (default `true`) |
| `has_accounts` | Users create an account in your app (this also requires in-app **account deletion** for App Review) |
| `has_backend` | Any user data is sent to your own servers or a cloud service. Fill in `service_providers` |
| `has_analytics` | You use any analytics or crash-reporting SDK that sends data off the device. Fill in `analytics_description` and list the SDK in your App Privacy labels |
| `has_user_content` | Users can post/share content with others (requires reporting, blocking, and 24-hour response per App Store Guideline 1.2) |
| `accesses_photos` | The app reads your users' photo library (adds a Photos section; edit `photos_description` so it is exactly true, especially the on-device claim) |
| `has_health_data` | The app reads/writes HealthKit or handles health information |
| `include_health_policy` | You want the separate Consumer Health Data Privacy Policy page and nav link (turn on together with `has_health_data`) |
| `website_analytics` | You add analytics to this website (the default text says you use none) |
| `eu_users` | The app is available in the EU/EEA/UK (default `true`; adds the GDPR section) |
| `hipaa_covered` | Leave `false`. If you work with providers, hospitals, or health plans, HIPAA applies and these templates are **not** enough; the script will stop you. |

These templates assume you **do not** sell or share personal data for advertising and **do not** track users across other companies' apps or sites. If that changes, the privacy policy must be rewritten and you must add the App Tracking Transparency prompt.

## Fill these into App Store Connect

| App Store Connect field | Value |
|---|---|
| Support URL | `https://YOURDOMAIN/support.html` |
| Marketing URL | `https://YOURDOMAIN/` |
| Privacy Policy URL | `https://YOURDOMAIN/privacy.html` |
| License Agreement (EULA) | Choose "Custom" and paste the text of the "Apple-required terms" section, or simply link `https://YOURDOMAIN/terms.html` in the description. (Alternatively, use Apple's standard EULA and skip this section.) |
| Copyright | `2026 YOUR LLC NAME` (no "(c)" required) |
| Privacy Choices URL (optional, in the App Privacy section) | For a health app, `https://YOURDOMAIN/health-privacy.html`; also link it inside the app where health permissions are requested |

Also link the Privacy Policy and Terms **inside the app** (Settings screen and on any paywall).

## Accuracy checklist: verify before you publish

Every sentence in the policies is a promise. Confirm each of these is true for your app:

- [ ] Support emails: the policy says we keep them "up to two years." Either do that or edit the wording.
- [ ] The response times (support `response_time`, privacy requests within 45 days, user-content reports within 24 hours) are ones you can actually meet.
- [ ] Your **App Privacy "nutrition label"** in App Store Connect matches the privacy policy exactly (every SDK included).
- [ ] Your app's privacy manifest (`PrivacyInfo.xcprivacy`) lists every required-reason API you use.
- [ ] If you have accounts: users can delete their account **inside the app** (the Support page and Terms say where; make the path match).
- [ ] The support FAQ names the right menu path for **Restore Purchases**, and the app has that button.
- [ ] The subscription paywall shows price, period, auto-renewal, and links to Terms and Privacy.
- [ ] The mailing address is one you're willing to make public (a commercial address, not your home, if you want privacy).
- [ ] You monitor the three email addresses you list.
- [ ] Health apps: the claims (encryption, no third-party sharing, no iCloud storage of HealthKit data, no geofencing) are technically true.

## Other legal protection to put in place (beyond this website)

1. **LLC hygiene:** sign the Operating Agreement, keep finances separate, file the Statement of Information and pay the $800 tax on time (see the main checklist).
2. **IP assignment:** anything written before the LLC existed, and everything from contractors, should be assigned to the LLC in writing.
3. **Trademark:** consider registering your app/brand name with the USPTO (Class 9 software). A domain or a DBA does not give trademark rights.
4. **Copyright notice:** already in the footer. Registration with the U.S. Copyright Office is optional, but it is required before suing and strengthens your remedies.
5. **Insurance:** general liability plus tech E&O / cyber. Cyber coverage matters more if you hold health data.
6. **Open-source compliance:** keep a list of libraries and their licenses; include required notices in the app (e.g. Settings → Acknowledgements). Avoid GPL/AGPL in the app.
7. **User-generated content:** if you enable `has_user_content`, you need in-app reporting, blocking, and a moderation process. If you host content from others, consider registering a **DMCA designated agent** with the U.S. Copyright Office (small fee) to get safe-harbor protection.
8. **Arbitration / class waiver:** these Terms use California courts. Some developers add an arbitration clause with a class-action waiver. That is a strategic choice for your attorney, and it must be done carefully.
9. **Data breach plan:** know who to call (attorney, cyber insurer) and California's notice rules (Civ. Code 1798.82). Keep a simple data map of what you collect and where it goes.
10. **Health app (future):** before building, review the health section of the main checklist (HIPAA vs. Washington My Health My Data Act, FTC Health Breach Notification Rule, FDA "general wellness" line, Apple Guidelines 5.1.3 and 1.4). Consider a separate LLC, a HIPAA/health-privacy attorney, and a security review.

## Maintaining the site

- Change wording or flags, then re-run `python3 configure.py`, commit, and push. GitHub redeploys automatically.
- Git history is your record of past policy versions; keep it. When you make a material change, update the app's App Privacy labels and tell users (in the app or by email) before it takes effect.
- Review both policies at least once a year, and every time you add an SDK, a data type, a backend, or a new app.
- **Apple badge:** to show the official "Download on the App Store" badge, download it from Apple's marketing resources and follow their usage rules; the template uses a text button so you don't need to.
