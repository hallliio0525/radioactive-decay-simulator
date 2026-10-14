"""
Radioactive Decay Simulator / 방사성 붕괴 시뮬레이터

Lets the user pick a language (Korean or English), then either choose a
well-known radioactive element (its half-life is filled in automatically)
or enter a custom half-life. Then plots how the amount decays over time.

사용자가 언어(한국어/영어)를 선택한 뒤, 잘 알려진 방사성 원소를 고르면
반감기가 자동으로 채워지고(직접 입력도 가능), 시간에 따라 원자 수가
줄어드는 모습을 그래프로 보여줍니다.
"""

import math
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# Preset elements and their half-lives (in years).
# Source: general nuclear physics references; values are the
# commonly cited half-lives for each isotope.
# ---------------------------------------------------------
ELEMENTS = [
    # (key, name_ko, name_en, half_life_years)
    ("U238", "우라늄-238 (Uranium-238)", "Uranium-238", 4.468e9),
    ("U235", "우라늄-235 (Uranium-235)", "Uranium-235", 7.04e8),
    ("PU239", "플루토늄-239 (Plutonium-239)", "Plutonium-239", 24100),
    ("CS137", "세슘-137 (Cesium-137)", "Cesium-137", 30.17),
    ("C14", "탄소-14 (Carbon-14)", "Carbon-14", 5730),
    ("I131", "요오드-131 (Iodine-131)", "Iodine-131", 0.02195),  # about 8.02 days
]


TEXT = {
    "ko": {
        "choose_lang": "언어를 선택하세요 (ko = 한국어, en = English): ",
        "element_menu_title": "\n원소를 선택하세요:",
        "element_custom": "직접 반감기 입력",
        "element_prompt": "번호를 입력하세요: ",
        "half_life": "반감기를 입력하세요 (단위: 년): ",
        "initial_atoms": "초기 원자 수를 입력하세요: ",
        "time_range": "그래프로 볼 기간을 입력하세요 (단위: 년): ",
        "invalid_number": "숫자를 정확히 입력해주세요. 다시 시도합니다.",
        "invalid_choice": "목록에 있는 번호를 입력해주세요.",
        "must_be_positive": "값은 0보다 커야 합니다. 다시 입력해주세요.",
        "selected_half_life": "선택한 반감기: {:.4g}년\n",
        "plot_title": "방사성 붕괴 시뮬레이션",
        "xlabel": "시간 (년)",
        "ylabel": "남은 원자 수",
        "half_life_label": "반감기 = {:.4g}년",
        "summary": "\n[결과 요약]\n원소: {}\n반감기: {:.4g}년\n초기 원자 수: {:.2e}\n{:.4g}년 후 남은 원자 수: {:.2e}",
    },
    "en": {
        "choose_lang": "Choose language (ko = Korean, en = English): ",
        "element_menu_title": "\nChoose an element:",
        "element_custom": "Enter a custom half-life",
        "element_prompt": "Enter the number: ",
        "half_life": "Enter the half-life (in years): ",
        "initial_atoms": "Enter the initial number of atoms: ",
        "time_range": "Enter how many years to simulate: ",
        "invalid_number": "Please enter a valid number. Try again.",
        "invalid_choice": "Please enter one of the listed numbers.",
        "must_be_positive": "Value must be greater than 0. Try again.",
        "selected_half_life": "Selected half-life: {:.4g} years\n",
        "plot_title": "Radioactive Decay Simulation",
        "xlabel": "Time (years)",
        "ylabel": "Remaining atoms",
        "half_life_label": "Half-life = {:.4g} years",
        "summary": "\n[Summary]\nElement: {}\nHalf-life: {:.4g} years\nInitial atoms: {:.2e}\nAtoms remaining after {:.4g} years: {:.2e}",
    },
}


def choose_language():
    """Ask the user which language they want."""
    while True:
        choice = input(TEXT["ko"]["choose_lang"]).strip().lower()
        if choice in ("ko", "en"):
            return choice
        print("Invalid input. Please type 'ko' or 'en'. / 'ko' 또는 'en'을 입력하세요.")


def ask_positive_float(prompt, t):
    """Keep asking until the user enters a valid positive number."""
    while True:
        raw = input(prompt)
        try:
            value = float(raw)
        except ValueError:
            print(t["invalid_number"])
            continue
        if value <= 0:
            print(t["must_be_positive"])
            continue
        return value


def choose_element(lang, t):
    """
    Show a numbered menu of preset elements plus a 'custom' option.
    Returns (element_name, half_life_years).
    """
    name_index = 1 if lang == "ko" else 2  # which column of ELEMENTS to show

    print(t["element_menu_title"])
    for i, elem in enumerate(ELEMENTS, start=1):
        print(f"  {i}. {elem[name_index]}  ({elem[3]:.4g} {('년' if lang == 'ko' else 'years')})")
    custom_option_num = len(ELEMENTS) + 1
    print(f"  {custom_option_num}. {t['element_custom']}")

    while True:
        raw = input(t["element_prompt"]).strip()
        try:
            choice = int(raw)
        except ValueError:
            print(t["invalid_choice"])
            continue

        if 1 <= choice <= len(ELEMENTS):
            elem = ELEMENTS[choice - 1]
            half_life = elem[3]
            name = elem[name_index]
            print(t["selected_half_life"].format(half_life))
            return name, half_life
        elif choice == custom_option_num:
            half_life = ask_positive_float(t["half_life"], t)
            custom_name = "Custom" if lang == "en" else "직접 입력"
            return custom_name, half_life
        else:
            print(t["invalid_choice"])


def decay_amount(initial_atoms, half_life, t):
    """N(t) = N0 * (1/2)^(t / half_life)"""
    return initial_atoms * math.pow(0.5, t / half_life)


def main():
    lang = choose_language()
    t = TEXT[lang]

    element_name, half_life = choose_element(lang, t)
    initial_atoms = ask_positive_float(t["initial_atoms"], t)
    time_span = ask_positive_float(t["time_range"], t)

    # Build the time points and corresponding remaining-atom counts
    steps = 300
    times = [time_span * i / steps for i in range(steps + 1)]
    amounts = [decay_amount(initial_atoms, half_life, time) for time in times]

    # Print a quick text summary before showing the plot
    final_amount = amounts[-1]
    print(t["summary"].format(element_name, half_life, initial_atoms, time_span, final_amount))

    # Plot
    plt.figure(figsize=(8, 5))
    plt.plot(times, amounts, color="tab:blue", linewidth=2)
    plt.axvline(half_life, color="gray", linestyle="--", label=t["half_life_label"].format(half_life))
    plt.title(f"{t['plot_title']} — {element_name}")
    plt.xlabel(t["xlabel"])
    plt.ylabel(t["ylabel"])
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
