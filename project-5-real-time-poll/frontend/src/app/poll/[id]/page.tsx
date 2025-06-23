"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

export default function PollPage() {
  const { id } = useParams();
  const [poll, setPoll] = useState<any>(null);
  const [selected, setSelected] = useState<string>("");
  const [voted, setVoted] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Проверка localStorage на повторное голосование
  useEffect(() => {
    if (!id) return;
    const votedKey = `poll_voted_${id}`;
    const votedOption = localStorage.getItem(votedKey);
    if (votedOption) {
      setSelected(votedOption);
      setVoted(true);
    }
  }, [id]);

  // Загрузка опроса
  useEffect(() => {
    if (!id) return;
    setLoading(true);
    fetch(`http://localhost:8000/api/poll/${id}`)
      .then(r => r.json())
      .then(setPoll)
      .catch(() => setError("Опрос не найден"))
      .finally(() => setLoading(false));
  }, [id]);

  const handleVote = async (optionKey: string) => {
    if (voted) return;
    setError("");
    try {
      const res = await fetch(`http://localhost:8000/api/poll/vote/${id}/${optionKey}`, { method: "POST" });
      if (!res.ok) throw new Error();
      const updated = await res.json();
      setPoll(updated);
      setSelected(optionKey);
      setVoted(true);
      localStorage.setItem(`poll_voted_${id}`, optionKey);
    } catch {
      setError("Ошибка голосования");
    }
  };

  if (loading) return <div>Загрузка...</div>;
  if (error) return <div style={{ color: "red" }}>{error}</div>;
  if (!poll) return null;

  return (
    <div style={{ maxWidth: 500, margin: "40px auto" }}>
      <h2>{poll.question}</h2>
      <form onSubmit={e => e.preventDefault()}>
        {Object.entries(poll.options).map(([key, opt]: any) => (
          <div key={key} style={{ marginBottom: 10 }}>
            <label>
              <input
                type="radio"
                name="option"
                value={key}
                disabled={voted}
                checked={selected === key}
                onChange={() => setSelected(key)}
              />
              {opt.label} — {opt.votes} голосов
            </label>
          </div>
        ))}
        {!voted && (
          <button
            type="button"
            disabled={!selected}
            onClick={() => handleVote(selected)}
            style={{ marginTop: 16 }}
          >
            Проголосовать
          </button>
        )}
        {voted && <div style={{ color: "green", marginTop: 16 }}>Спасибо, ваш голос учтён!</div>}
      </form>
    </div>
  );
}

