import React from 'react';
import { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";

export default function Register() {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [nome, setNome] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    try {
      // Alterar url para seu endpoint de registro!
      await axios.post("/api/auth/register", { email, senha, nome });
      navigate("/login");
    } catch (err) {
      setError("Erro ao criar conta");
    }
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-lyzor-dark">
      <img src="/lyzor-logo.svg" alt="Lyzor Logo" className="mb-6 w-16 h-16" />
      <h1 className="text-3xl font-bold mb-2">Criar Conta</h1>
      <form className="bg-zinc-900 rounded-lg p-8 shadow-md w-full max-w-sm" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Nome"
          className="w-full mb-4 p-3 rounded bg-zinc-800 text-white"
          value={nome}
          onChange={e => setNome(e.target.value)}
          required
        />
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
          Criar conta
        </button>
        <div className="mt-4 text-center">
          <Link className="text-lyzor underline" to="/login">
            Já tenho conta
          </Link>
        </div>
      </form>
    </div>
  );
}