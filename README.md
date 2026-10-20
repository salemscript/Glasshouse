# Glasshouse — GitHub Pages edition

This is a complete portable copy of the Glasshouse website, including the latest
Physics II and Calculus Chapter 11 labs. No build tools or paid API are needed.
The website files live in `site/`; the included GitHub workflow publishes that folder.

## Publish using GitHub Desktop

1. Unzip the download. Keep all files and folders together, including the hidden
   `.github` folder. Do not upload the ZIP itself as the website.
2. Open GitHub Desktop. Choose **File → New Repository** and create a new repository
   named `glasshouse`. Use a separate repository from your portfolio.
3. Choose **Repository → Show in Finder**. Copy the **contents** of the extracted
   `glasshouse-github` folder into this repository folder: `site`, `tools`,
   `.github`, the manifest, this README and the other files. On Mac, press
   **Command–Shift–period** to show hidden files when copying `.github`.
   The repository should contain `site/index.html`, not another wrapper folder.
4. In GitHub Desktop, commit the changes and choose **Publish repository**.
   For GitHub Free, choose a public repository to use Pages. Other plans may
   support Pages from private repositories; the website itself is normally public.
5. Open the repository on GitHub. Under **Settings → Pages → Build and deployment**,
   choose **Source: GitHub Actions**.
6. Open **Actions → Publish Glasshouse → Run workflow** on the default branch.
   Wait for a green check. The workflow and Pages settings show the website URL.

After the first setup, pushing changes to the repository's default branch publishes
the site again. There is no scheduled content generation or recurring update job.

GitHub Desktop is preferable to browser drag-and-drop for this export's thousands
of files. If you upload through the browser, preserve the full directory structure
and include `.github/workflows/pages.yml`; upload the extracted files, not the ZIP.

## Put it on your domain

If your portfolio already uses your main domain, use a dedicated subdomain such
as `learn.example.com` or `glasshouse.example.com` for this site.

1. In this repository's **Settings → Pages → Custom domain**, enter your exact
   domain or subdomain and save it **before** changing DNS.
2. At your domain provider, for a subdomain add a **CNAME** record:
   - Host/name: the chosen subdomain, for example `learn`.
   - Target/value: `YOUR-GITHUB-USERNAME.github.io`.
   - Do not include `https://`, a repository name or a path in this target.
3. Allow the DNS check and certificate to complete, then enable **Enforce HTTPS**
   in GitHub's Pages settings. DNS and certificate setup can take up to 24 hours.

If you want this site on the bare domain instead, follow GitHub's apex-domain
instructions. That would replace what the bare domain currently serves. This
download does not change or overwrite any existing domain records or portfolio.

This Actions deployment uses the domain configured in Pages settings; no placeholder
`CNAME` file is included or required. The domain is deliberately left unconfigured
until you choose the exact address.

## What moves with the website

- Labs, question banks, explanations, calculator, diagrams, fonts and linked PDFs.
- Existing credits and license notices remain in the exported website.
- Progress continues to be saved in each visitor's browser. Progress from the
  current `chatgpt.site` address does not automatically move to a new domain.
- The current Sites invite-only access gate does **not** move into this static
  export. Standard GitHub Pages hosting is public; private repository visibility
  alone does not make the published website private.
- This is the current site snapshot, including its existing coverage gaps; it
  does not add new worked textbook solutions.

No credentials, account invitations, `.git` history, internal project records or
Sites hosting identity are included in this export.

## Verify the download

Run `python3 tools/verify_export.py` from this repository folder. It checks the
export manifest, file sizes, SHA-256 hashes, compressed question data and local
HTML/CSS references. GitHub runs the same check before publishing.

After intentionally editing website files, refresh the manifest before committing:

```sh
python3 tools/verify_export.py --refresh
python3 tools/verify_export.py
```

Do not open `site/index.html` by double-clicking it as a full functionality test:
question data is fetched over HTTP and needs a web server. The GitHub Pages URL
is the normal way to use the deployed site.

## Official setup references

Checked October 20, 2026:

- [GitHub Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [GitHub Desktop setup](https://docs.github.com/en/desktop/overview/creating-your-first-repository-using-github-desktop)
- [Custom domains and DNS](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
- [GitHub Pages publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)
