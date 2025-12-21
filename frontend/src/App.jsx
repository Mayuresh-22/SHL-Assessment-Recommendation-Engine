import { useState } from "react";

export default function App() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setResults(null);
    setError(null);

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/recommend`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      const data = await res.json();
      setResults(data["recommended_assessments"]);
    } catch (e) {
      setError("An error occurred while fetching recommendations.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen overflow-hidden bg-white font-sans">
      <BackgroundBlobs />

      <main className="relative z-10 flex min-h-screen flex-col items-center justify-center px-6">
        <div
          className={`transition-all duration-500 ${
            results ? "translate-y-[-80px]" : ""
          }`}
        >
          <h1 className="mt-8 mb-8 text-3xl text-center font-medium text-slate-700">
            SHL Assessment Recommendation System
          </h1>
          <QueryInput
            value={query}
            onChange={setQuery}
            onSubmit={handleSubmit}
          />
        </div>

        {loading && (
          <div className="mt-8 flex gap-2">
            <Dot />
            <Dot delay="delay-150" />
            <Dot delay="delay-300" />
          </div>
        )}

        {error && (
          <div className="mt-8 text-red-500">
            {error}
          </div>
        )}

        {results && (
          <div className="mb-8 w-full max-w-4xl animate-fade-in">
            <h2 className="mb-4 text-xl font-medium text-slate-700">
              Recommended SHL's Assessments
            </h2>
            <ResultsTable data={results} />
          </div>
        )}

        <Footer />
      </main>
    </div>
  );
}

function BackgroundBlobs() {
  return (
    <>
      <div className="absolute -top-32 -left-32 h-96 w-96 rounded-full bg-sky-200 opacity-40 blur-3xl" />
      <div className="absolute top-1/3 -right-32 h-96 w-96 rounded-full bg-sky-300 opacity-40 blur-3xl" />
      <div className="absolute bottom-0 left-1/4 h-96 w-96 rounded-full bg-sky-200 opacity-30 blur-3xl" />
    </>
  );
}

function QueryInput({ value, onChange, onSubmit }) {
  return (
    <div className="flex w-[640px] items-end rounded-2xl border border-slate-200 bg-white px-4 py-3 shadow-sm">
      <textarea
        rows={1}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Enter job description or query here..."
        className="max-h-[240px] flex-1 resize-none overflow-y-auto bg-transparent text-slate-700 outline-none"
        onInput={(e) => {
          e.target.style.height = "auto";
          e.target.style.height = Math.min(e.target.scrollHeight, 240) + "px";
        }}
      />
      <button
        onClick={onSubmit}
        className="ml-3 flex h-10 w-10 items-center justify-center rounded-xl bg-sky-500 text-white hover:bg-sky-600 transition"
      >
        ↑
      </button>
    </div>
  );
}

function Dot({ delay = "" }) {
  return (
    <span
      className={`h-2 w-2 rounded-full bg-slate-400 animate-bounce ${delay}`}
    />
  );
}

function ResultsTable({ data }) {
  return (
    <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
      <table className="w-full text-left text-sm">
        <thead className="bg-slate-50 text-slate-600">
          <tr>
            <th className="px-4 py-3">Assessment</th>
            <th className="px-4 py-3">Type</th>
            <th className="px-4 py-3">Duration</th>
            <th className="px-4 py-3">Remote Testing</th>
            <th className="px-4 py-3">Adaptive</th>
            <th className="px-4 py-3">Details</th>
            <th className="px-4 py-3">Test Link</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={i} className="border-t border-slate-100 hover:bg-slate-50">
              <td className="px-4 py-3 font-medium text-slate-700">
                {row.name}
              </td>
              <td className="px-4 py-3">{row.test_type.join(", ")}</td>
              <td className="px-4 py-3">{row.duration == 0 ? "Variable" : `${row.duration} min`}</td>
              <td className="px-4 py-3">{row.remote_support}</td>
              <td className="px-4 py-3">{row.adaptive_support}</td>
              <td className="px-4 py-3 text-slate-600">{row.description.slice(0, 250)}...</td>
              <td className="px-4 py-3">
                <a
                  href={row.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sky-500 hover:underline"
                >
                  Visit
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function Footer() {
  return (
    <footer className="relative z-10 flex items-center justify-center p-4 text-sm text-slate-500">
      <p>
        Developed by Mayuresh Choudhary
      </p>
    </footer>
  );
}
