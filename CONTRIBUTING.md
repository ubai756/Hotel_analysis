# Contributing to Hotel Analytics

Thanks for your interest in improving this project. Contributions,
bug reports, and suggestions are all welcome.

---

## How to Contribute

1. **Fork the repository**

2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```

3. **Make your changes**, following the code style notes below.

4. **Commit your changes**
   ```bash
   git commit -m 'Add AmazingFeature'
   ```

5. **Push to your branch**
   ```bash
   git push origin feature/AmazingFeature
   ```

6. **Open a Pull Request** against the `main` branch, with a clear
   description of what changed and why.

---

## Code Style

- Follow existing patterns in the codebase — page logic lives in
  `pages_content/`, reusable UI pieces in `components/`, and data/model
  logic in `data/`.
- Keep chart styling consistent with `components/charts.py`'s shared
  theme (colors, fonts, layout) rather than introducing one-off styles.
- Use the icon system in `components/icons.py` instead of emoji for any
  new UI elements, to stay consistent with the rest of the dashboard.
- Add a short docstring to any new module or non-trivial function.
- Keep file paths `__file__`-based (see `config.py`'s `BASE_DIR`) rather
  than relative to the working directory, so the app keeps working
  correctly when deployed.

---

## Reporting Bugs

When filing an issue, please include:

- What you expected to happen vs. what actually happened
- Steps to reproduce
- Your Python version and OS
- A screenshot, if it's a visual/UI issue

---

## Testing Changes Locally

Before opening a pull request, run the app locally and click through all
five pages (Home, Analytics, AI Insights, Dataset Explorer, Profile) to
confirm nothing is broken:

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Questions

Open an issue, or reach out directly — contact details are in
[README.md](README.md#author).
