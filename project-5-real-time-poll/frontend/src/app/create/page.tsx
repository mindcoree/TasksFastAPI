"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function CreatePollPage() {
  const [question, setQuestion] = useState("");
  const [options, setOptions] = useState(["", ""]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  const handleOptionChange = (idx: number, value: string) => {
    setOptions(opts => opts.map((opt, i) => (i === idx ? value : opt)));
  };

  const addOption = () => setOptions(opts => [...opts, ""]);
  const removeOption = (idx: number) => {
    if (options.length > 2) setOptions(opts => opts.filter((_, i) => i !== idx));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    if (!question.trim() || options.some(opt => !opt.trim())) {
      setError("Заполните вопрос и все варианты.");
      return;
    }
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/poll/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, options }),
      });
      if (!res.ok) throw new Error("Ошибка создания опроса");
      const poll = await res.json();
      router.push(`/poll/${poll.id}`);
    } catch (e) {
      setError("Ошибка создания опроса");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 500, margin: "40px auto" }}>
      <h2>Создать новый опрос</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Вопрос:</label>
          <input
            type="text"
            value={question}
            onChange={e => setQuestion(e.target.value)}
            style={{ width: "100%", marginBottom: 12 }}
            required
          />
        </div>
        <div>
          <label>Варианты:</label>
          {options.map((opt, idx) => (
            <div key={idx} style={{ display: "flex", marginBottom: 8 }}>
              <input
                type="text"
                value={opt}
                onChange={e => handleOptionChange(idx, e.target.value)}
                required
                style={{ flex: 1 }}
              />
              {options.length > 2 && (
                <button type="button" onClick={() => removeOption(idx)} style={{ marginLeft: 8 }}>
                  ×
                </button>
              )}
            </div>
          ))}
          <button type="button" onClick={addOption} style={{ marginTop: 8 }}>
            + Добавить вариант
          </button>
        </div>
        {error && <div style={{ color: "red", marginTop: 10 }}>{error}</div>}
        <button type="submit" disabled={loading} style={{ marginTop: 20 }}>
          {loading ? "Создание..." : "Создать опрос"}
        </button>
      </form>
    </div>
  );
}

