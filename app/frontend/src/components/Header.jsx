import React from 'react';
export default function Header({ user }) {
  function handleLogout() {
    localStorage.removeItem("token");
    window.location.href = "/login";
  }

  return (
    <header className="w-full bg-zinc-900 flex items-center justify-between px-8 py-4 shadow">
      <span className="text-lg font-bold">Lyzor Dashboard</span>
      <div className="flex items-center gap-4">
        <span className="font-medium">{user?.nome}</span>
        <button
          className="bg-lyzor text-white px-4 py-2 rounded hover:bg-indigo-700 font-semibold"
          onClick={handleLogout}
        >
          Sair
        </button>
      </div>
    </header>
  );
}