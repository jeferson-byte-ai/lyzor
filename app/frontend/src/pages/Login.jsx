import React from 'react';
import { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    try {
      // Alterar url para seu endpoint de login!
      const { data } = await axios.post("/api/auth/login", { email, senha });
      localStorage.setItem("token", data.token);
      navigate("/dashboard");
    } catch (err) {
      setError("Usuário ou senha inválidos");
    }
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-lyzor-dark">
      <img src="/lyzor-logo.svg" alt="Lyzor Logo" className="mb-6 w-16 h-16" />
      <h1 className="text-3xl font-bold mb-2">Entrar no Lyzor</h1>
      <form className="bg-zinc-900 rounded-lg p-8 shadow-md w-full max-w-sm" onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="E-mail"
          className="w-full mb-4 p-3 rounded bg-zinc-800 text-white"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Senha"
          className="w-full mb-4 p-3 rounded bg-zinc-800 text-white"
          value={senha}
          onChange={e => setSenha(e.target.value)}
          required
        />
        {error && <div className="text-red-500 mb-2">{error}</div>}
        <button type="submit" className="w-full bg-lyzor hover:bg-indigo-700 text-white font-bold py-2 rounded">
          Entrar
        </button>
        <div className="mt-4 text-center">
          <Link className="text-lyzor underline" to="/register">
            Criar conta
          </Link>
        </div>
      </form>
    </div>
  );
}