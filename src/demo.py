from __future__ import annotations

"""AIざぶとんのCLIデモ。

お題とボケ、AI判定、ざぶとん投票を一通りシミュレートする。
"""

from ai_zabuton import (
    Joke,
    JokeWithFeedback,
    Prompt,
    Verdict,
    VerdictLabel,
    Zabuton,
    add_zabuton,
    judge_joke,
)


SAMPLE_PROMPTS = [
    "猫が会議に参加している写真",
    "AIが漫才をする未来のニュース",
    "お寿司屋さんの張り紙に書かれていた一言",
]


SAMPLE_JOKES = [
    Joke(author="匿名A", content="AIよ、まず座布団に謝れ！"),
    Joke(author="匿名B", content="猫社長『ニャイデア会議』開催"),
    Joke(author="匿名C", content="寿司屋のWi-Fiはシャリ弱い"),
]


def run_demo() -> None:
    print("=== AIざぶとん CLIデモ ===")
    for prompt_text, joke in zip(SAMPLE_PROMPTS, SAMPLE_JOKES):
        prompt = Prompt(content=prompt_text)
        verdict = judge_joke(joke)
        jwf = JokeWithFeedback(prompt=prompt, joke=joke, verdict=verdict)

        # ざぶとん反応を付与
        add_zabuton(
            jwf,
            Zabuton(voter="観客1", stance="賛成", comment="AIの判定、意外と的確！"),
        )
        add_zabuton(
            jwf,
            Zabuton(voter="観客2", stance="反対", comment="これでダメは厳しいでしょ"),
        )

        print("\n" + jwf.summary())

    print("\n投げられたざぶとんでAIの味覚プロファイルを掴もう！")


if __name__ == "__main__":
    run_demo()
