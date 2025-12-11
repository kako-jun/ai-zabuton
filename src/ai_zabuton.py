from __future__ import annotations

"""シンプルなAIざぶとんの評価モジュール。

MVPの雰囲気をCLIで素早く確認できるよう、
テキストのお題・ボケ・AI判定・ざぶとん反応を模擬する。
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List


class VerdictLabel(Enum):
    FUNNY = "👍おもしろい"
    NOT_FUNNY = "👎おもしろくない"
    UNSURE = "🤷判断不能"


@dataclass
class Prompt:
    content: str


@dataclass
class Joke:
    author: str
    content: str


@dataclass
class Verdict:
    label: VerdictLabel
    reason: str
    confidence: float


@dataclass
class Zabuton:
    voter: str
    stance: str
    comment: str


@dataclass
class JokeWithFeedback:
    prompt: Prompt
    joke: Joke
    verdict: Verdict
    zabutons: List[Zabuton] = field(default_factory=list)

    def summary(self) -> str:
        zabuton_score = len(self.zabutons)
        lines = [
            f"お題: {self.prompt.content}",
            f"ボケ: {self.joke.content} (by {self.joke.author})",
            f"AI判定: {self.verdict.label.value} | 理由: {self.verdict.reason} | 確信度: {self.verdict.confidence:.2f}",
            f"ざぶとん: {zabuton_score}枚",
        ]
        if self.zabutons:
            lines.append("--- ざぶとん明細 ---")
            for z in self.zabutons:
                lines.append(f"{z.voter}: {z.stance} / ツッコミ: {z.comment}")
        return "\n".join(lines)


def judge_joke(joke: Joke) -> Verdict:
    """シンプルなルールベース判定でMVPのUI挙動を再現。"""
    text = joke.content
    score = 0
    if "!" in text or "？" in text or "!" in text:
        score += 1
    if any(word in text for word in ["猫", "AI", "ざぶとん", "寿司", "温泉"]):
        score += 1
    if len(text) <= 12:
        score += 0.5

    if score >= 2:
        label = VerdictLabel.FUNNY
        reason = "勢いと日本っぽいワードが効いています"
        confidence = 0.78
    elif score >= 1:
        label = VerdictLabel.UNSURE
        reason = "発想はあるが、もう一押し欲しいです"
        confidence = 0.52
    else:
        label = VerdictLabel.NOT_FUNNY
        reason = "文脈やフックが見えませんでした"
        confidence = 0.34

    return Verdict(label=label, reason=reason, confidence=confidence)


def add_zabuton(jwf: JokeWithFeedback, zabuton: Zabuton) -> None:
    jwf.zabutons.append(zabuton)
