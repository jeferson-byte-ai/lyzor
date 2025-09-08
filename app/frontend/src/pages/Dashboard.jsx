import React from 'react';
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import Card from "../components/Card";

export default function Dashboard() {
  // Simulação de dados (troque por chamada real à API depois)
  const user = { nome: "Jeferson", email: "jeferson@lyzor.ai" };
  const cards = [
    { title: "Usuários", value: 143 },
    { title: "Auditorias", value: 56 },
    { title: "Serviços", value: 12 }
  ];

  return (
    <div className="flex h-screen bg-lyzor-dark">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Header user={user} />
        <main className="p-6 flex gap-6 flex-wrap">
          {cards.map((card, i) => (
            <Card key={i} title={card.title} value={card.value} />
          ))}
        </main>
      </div>
    </div>
  );
}