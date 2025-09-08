import React from 'react';
import { Link, useLocation } from "react-router-dom";

const links = [
  { to: "/dashboard", label: "Dashboard" },
  { to: "/settings", label: "Configurações" },
  { to: "/audit", label: "Auditorias" }
];

export default function Sidebar() {
  const { pathname } = useLocation();

  return (
    <aside className="w-64 bg-zinc-900 text-white flex flex-col py-8 px-4">
      <img src="/lyzor-logo.svg" alt="Lyzor" className="mb-10 w-14 h-14 self-center" />
      {links.map(link => (
        <Link
          key={link.to}
          to={link.to}
          className={`mb-4 px-3 py-2 rounded font-medium transition ${
            pathname === link.to ? "bg-lyzor text-white" : "hover:bg-zinc-800"
          }`}
        >
          {link.label}
        </Link>
      ))}
    </aside>
  );
}